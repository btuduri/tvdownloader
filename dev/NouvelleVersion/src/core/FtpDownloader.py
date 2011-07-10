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
