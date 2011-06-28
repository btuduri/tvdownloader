#!/usr/bin/env python

import ftplib,socket,re,sys,urlparse

from DownloaderInterface import *

class HttpDownloader (DownloaderInterface) :
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
		self.ftpconn = None
		self.size = None
	
	def start(self):
		try:
			parsed = urlparse.urlparse(self.url)
		
			ftpconn = ftplib.FTP(parsed.netloc)
			self.size = ftpconn.size(parsed.path)
			res = re.findall("[0-9]+", ftpconn.sendcmd("PASV"))
			if len(res) != 7:
				self.size = 0
				return False
			ip = res[1]+"."+res[2]+"."+res[3]+"."+res[4]
			port = int(res[5])*256 + int(res[6])

			sockconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sockconn.connect((ip, port))
			self.stream = sockconn
			
			ftpconn.sendcmd("RETR "+parsed.path)
			self.ftpconn = ftpconn
		except:
			if self.ftpconn != None:
				self.ftpconn.close()
			if self.stream != None:
				self.stream.close()
			return False
		return True
	
	def getSize(self):
		return self.size
	
	def read (self, n) :
		return self.stream.read(n)
	
	def stop(self):
		self.stream.close()
		self.ftpconn.close()
	
	def canDownload (self, url) :
		# returns bool
		pass
