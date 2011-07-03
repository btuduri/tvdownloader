# -*- coding:Utf-8 -*-

import subprocess,shlex,re

from DownloaderInterface import *

class MsdlDownloader (DownloaderInterface) :
	def __init__(self, url) :
		DownloaderInterface.__init__(self)
		self.url = url
		self.size = None
		self.stream = None
		self.process = None
	
	def start(self):
		commande = "msdl \"" + self.url + "\" -o -"
		arguments = shlex.split( commande )
		
		try:
			self.process = subprocess.Popen( arguments, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
			self.stream = self.process.stdout
			line = self.process.stderr.readline()
			tries = 10
			while line != "" and tries > 0:
				print line
				found = pourcentListe = re.findall( "DL: [0-9]+/([0-9]+) B[^%]+?%", line)
				if len(found) > 0:
					self.size = int(found[0])
					break;
				line = self.process.stderr.readline()
				tries = tries-1
			if self.size == None:
				self.process.kill()
				return False
		except Exception as e:
			import traceback
			traceback.print_exc(e)
			if self.process != None:
				self.process.kill()
			return False
		return True
	
	def read (self, n) :
		return self.process.stdout.read(n)
	
	def stop(self):
		self.process.kill()
	
	def getSize(self):
		return self.size
	
	def canDownload (self, url) :
		# returns bool
		pass

