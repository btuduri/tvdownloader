#!/usr/bin/env python

import ftplib,socket,re,sys,urlparse,os

from DownloaderInterface import *

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
			
			
			
#			res = re.findall("[0-9]+", ftpconn.sendcmd("PASV"))
#			if len(res) != 7:
#				self.size = 0
#				return False
#			ip = res[1]+"."+res[2]+"."+res[3]+"."+res[4]
#			port = int(res[5])*256 + int(res[6])
#			sockconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#			ftpconn.sendcmd("LIST "+parsed.path)
#			sockconn.connect((ip, port))
#			ftplist = sockconn.recv(800)
#			sockconn.close()
#			self.size = int(re.match("[^\t ]+[\t ]+[^\t ]+[\t ]+[^\t ]+[\t ]+[^\t ]+[\t ]+([0-9]+)", ftplist).group(1))
#			print "taille:",self.size
#			
#			ftpconn.sock.recv(800)
#			s = ftpconn.sendcmd("PASV")
#			res = re.findall("[0-9]+", s)
#			if len(res) != 7:
#				print s
#				self.size = 0
#				return False
#			ip = res[1]+"."+res[2]+"."+res[3]+"."+res[4]
#			port = int(res[5])*256 + int(res[6])
#			sockconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#			sockconn.connect((ip, port))
#			print sockconn.fileno()
#			self.stream = os.fdopen(sockconn.fileno())
#			
#			ftpconn.sendcmd("RETR "+parsed.path)
			
			self.stream,self.size = ftpconn.ntransfercmd("RETR "+parsed.path)
			
			self.ftpconn = ftpconn
		except BaseException as e:
			import traceback
			traceback.print_exc(e)
			if self.ftpconn != None:
				self.ftpconn.close()
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
	
	def canDownload (self, url) :
		# returns bool
		pass
