# -*- coding:Utf-8 -*-

import urllib,urlparse,httplib

from DownloaderInterface import *

class HttpDownloader (DownloaderInterface) :
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
		self.size = None
	
	def start(self):
		parsed = urlparse.urlparse(self.url)
		httpcon = httplib.HTTPConnection(parsed.netloc)
		print parsed.netloc
		print parsed.path+"?"+parsed.query
		try:
			if parsed.query != "":
				httpcon.request("GET", parsed.path+"?"+parsed.query)
			else:
				httpcon.request("GET", parsed.path)
		except:
			return false
		resp = httpcon.getresponse()
		self.stream = resp
		self.size = int(resp.getheader("Content-Length"))
		print resp.getheader("Content-Length")
		return True
	
	def getSize(self):
		return self.size
	
	def read (self, n) :
		return self.stream.read(n)
	
	def stop(self):
		self.stream.close()
	
	def canDownload (self, url) :
		# returns bool
		pass

