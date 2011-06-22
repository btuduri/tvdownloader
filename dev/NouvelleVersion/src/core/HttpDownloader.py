# -*- coding:Utf-8 -*-

import urllib

from DownloaderInterface import *

class HttpDownloader (DownloaderInterface) :
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
	
	def start(self):
		parsed = urlparse.urlparse(self.url)
		httpcon = httplib.HTTPConnection(parsed.netloc)
		httpcon.request("GET", parsed.path+"?"+parsed.query)
		resp.httpcon.getresponse()
		self.stream = resp
	
	def read (self, n) :
		return self.stream.read(n)
	
	def stop(self):
		self.stream.close()
	
	def canDownload (self, url) :
		# returns bool
		pass

