# -*- coding:Utf-8 -*-

import subprocess,shlex,re,ctypes

libmms = ctypes.cdll.LoadLibrary("libmms.so.0")

from DownloaderInterface import *

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

