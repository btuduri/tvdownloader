#!/usr/bin/env python
# -*- coding:Utf-8 -*-

import ftplib,socket,re,sys,urlparse,os

import subprocess,shlex,re,ctypes
import fcntl,select
libmms = ctypes.cdll.LoadLibrary("libmms.so.0")
librtmp = ctypes.cdll.LoadLibrary("librtmp.so")

import urllib,httplib

## Interface des classes effectuant le téléchargement de fichiers distant.
#
#
class DownloaderInterface :
	def __init__(self):
		pass
	
	## Démarre le téléchargement
	# Ne doit être appelée qu'une seul fois avant l'utilisation des méthodes read ou stop.
	# @return True en cas de réussite, False en cas d'échec
	def start(self):
		pass
	
	## Arrête le téléchargement
	def stop(self):
		pass
	
	## Lit et renvoie des octets du flux téléchargé.
	#
	# La méthode start doit avoir été appelé avant pour que le téléchargement soit lancé.
	# @param n le nombre d'octet à lire
	# @return une chaîne de charactère de taille maximale n ou de taille 0 en cas de fin du flux ou None en cas d'échec
	def read (self, n) :
		# returns byte[]
		pass
	
	## Renvoie la taille du fichier en cours de téléchargement.
	# La valeur renvoyer peut changer en fonction de l'état du téléchargement. Il est préférable de ne l'appeler après start() ou pendant le téléchargement.
	# @return la taille du téléchargement en cour en octets, None si inconnue
	def getSize(self):
		pass

class FtpDownloader (DownloaderInterface) :
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
		self.ftpconn = None
		self.size = None
		self.stream = None
	
	def start(self):
		try:
			parsed = urlparse.urlparse(self.url)
			
			ftpconn = ftplib.FTP(parsed.netloc)
			ftpconn.login()
			
			self.stream,self.size = ftpconn.ntransfercmd("RETR "+parsed.path)
			
			self.ftpconn = ftpconn
		except BaseException as e:
			import traceback
			traceback.print_exc(e)
			if self.stream != None:
				self.stream.close()
			return False
		return True
	
	def getSize(self):
		return self.size
	
	def read (self, n) :
		return self.stream.recv(n)
	
	def stop(self):
		self.stream.close()
		self.ftpconn.close()
	
	@staticmethod
	def canDownload (url) :
		return url[:4] == "ftp:"

class MsdlDownloader (DownloaderInterface) :
	
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
		self.size = None
	
	def start(self):
		try:
			self.mmscon = libmms.mmsx_connect(None, None, self.url, int(5000))
			if self.mmscon == 0:
				return False
			self.size = libmms.mmsx_get_length(self.mmscon)
		except Exception as e:
			import traceback
			traceback.print_exc(e)
			return False
		return True
	
	def read (self, n):
		buffer = ctypes.create_string_buffer(n)
		libmms.mmsx_read(0, self.mmscon, buffer, n)
		return buffer.value
	
	def stop(self):
		libmms.mmsx_close(self.mmscon)
	
	def getSize(self):
		return self.size
	
	@staticmethod
	def canDownload (url) :
		return url[:4] == "mms:"

class HttpDownloader (DownloaderInterface) :
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
		self.size = None
	
	def start(self):
		parsed = urlparse.urlparse(self.url)
		httpcon = httplib.HTTPConnection(parsed.netloc)
		try:
			if parsed.query != "":
				httpcon.request("GET", parsed.path+"?"+parsed.query)
			else:
				httpcon.request("GET", parsed.path)
		except:
			return false
		resp = httpcon.getresponse()
		if resp.status != 200:
			httpcon.close()
			return False
		self.stream = resp
		if isinstance(resp.getheader("Content-Length"), str):
			self.size = int(resp.getheader("Content-Length"))
		return True
	
	def getSize(self):
		return self.size
	
	def read (self, n) :
		return self.stream.read(n)
	
	def stop(self):
		self.stream.close()
	
	@staticmethod
	def canDownload (url) :
		return url[:5] == "http:"

class RtmpDownloader(DownloaderInterface):
	RTMP_URL_PATTERN = re.compile("(?P<scheme>[^:]*)://(?P<host>[^/^:]*):{0,1}(?P<port>[^/]*)/(?P<app>.*?)/(?P<playpath>\w*?\:.*)", re.DOTALL)
	LENGHT_PATTERN = re.compile("length[^0-9]*([0-9]*.[0-9]*)")
	PROGRESS_PATTERN = re.compile("\(([0-9]+[.]?[0-9]*)%\)")
	
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.command = RtmpDownloader.urlToRtmpdump(url)
		print self.command
		self.size = 0
		self.dled = 0
		self.process = None
	
	def start(self):
		arguments = shlex.split(self.command)
		self.process = subprocess.Popen( arguments, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		if self.process != None:
			fno = self.process.stderr.fileno()
			fcntl.fcntl( fno, fcntl.F_SETFL, fcntl.fcntl( fno, fcntl.F_GETFL ) | os.O_NDELAY )
			select.select([fno],[],[], 0.2)#Attente le temps de la connexion au serveur
			try:
				descriptionFound = False
				while len(select.select([fno],[],[], 0.5)[0]) > 0:#Recherche de la description du fichier
					line = self.process.stderr.readline()
					if "sampledescription:" in line:
						descriptionFound = True
						break
				if descriptionFound:
					while len(select.select([fno],[],[], 0.5)[0]) > 0:#Recherche de la taille du fichier
						line = self.process.stderr.readline()
						match = re.search(RtmpDownloader.LENGHT_PATTERN, line)
						if match != None:
							self.size = float(match.group(1))
							break
				while len(select.select([fno],[],[], 0.01)[0]) > 0:#On vide le pipe
					line = self.process.stderr.readline()
			except Exception, e:
				print e
			return True
		else:
			return False
	
	def getSize(self):
		return self.size
	
	def read (self, n) :
		try:
			line = ""
			while len(select.select([self.process.stderr.fileno()],[],[], 0.05)[0]) > 0:#On vide le pipe
				line = self.process.stderr.readline()
			#Récupération de la progression pour estimation de la taille
			match = re.search(RtmpDownloader.PROGRESS_PATTERN, line)
			if match != None:
				self.size = (float(match.group(1))/100)*self.dled
		except:
			pass
		if len(select.select([self.process.stdout.fileno()],[],[], 0.2)[0]) > 0:
			data = self.process.stdout.read(n)
			self.dled = self.dled+len(data)
			return data
		else:
			return ""
	
	def stop(self):
		try:
			self.process.terminate()
		except:
			pass
	
	@staticmethod
	def canDownload (url) :
		return url[:4] == "rtmp"
	
	@staticmethod
	def urlToRtmpdump( url ):
		match = re.match( RtmpDownloader.RTMP_URL_PATTERN, url )
		comand = ""
		if match != None:
			comand = "rtmpdump --host %host% --port %port% --protocol %scheme% --app %app% --playpath %playpath% -o -"
			comand = comand.replace( "%scheme%", match.group( "scheme" ) ).replace( "%host%", match.group( "host" ) ).replace( "%app%", match.group( "app" ) ).replace( "%playpath%", match.group( "playpath" ) )
			if( match.group( "port" ) != "" ):
				comand = comand.replace( "%port%", match.group( "port" ) )
			elif( url[ :6 ] == "rtmpte" ):
				comand = comand.replace( "%port%", "80" )
			elif( url[ :5 ] == "rtmpe" ):
				comand = comand.replace( "%port%", "1935" )
			elif( url[ :5 ] == "rtmps" ):
				comand = comand.replace( "%port%", "443" )
			elif( url[ :5 ] == "rtmpt" ):
				comand = comand.replace( "%port%", "80" )
			else:
				comand = comand.replace( "%port%", "1935" )
		else:
			comand = "rtmpdump -r " + url + " -o -"
		return comand
