# -*- coding:Utf-8 -*-

import thread,threading

from DownloaderFactory import *

class DownloadManager(threading.Thread):
	BUFFER_SIZE = 8000
	
	def __init__(self) :
		threading.Thread.__init__(self)
		self.nextNumDownload = 0 # int
		
		self.dlFactory = DownloaderFactory();
		
		self.toDl = []
		self.mutex_toDl = thread.allocate_lock()
		self.cond_toDl = threading.Condition(self.mutex_toDl)
		
		self.start()
	
	def run(self):
		while True:
			if self.mutex_toDl.locked():
				print "Mutex verrouillé, attention au dead lock !"
			self.mutex_toDl.acquire()
			while len(self.toDl) <= 0:
				self.cond_toDl.wait();
				if self.mutex_toDl.locked():
					print "Mutex verrouillé, attention au dead lock !"
				self.mutex_toDl.acquire()
			dlParam = self.toDl.pop(0)
			self.mutex_toDl.release()
			
			print "Téléchargement de 3"+dlParam[0]+"..."
			dler = self.getDownloader()
			try:
				outfile = open(dlParam[1], "w")
				dler.start()
				carac = dler.read(DownloadManager.BUFFER_SIZE)
				while len(carac) > 0:
					oufile.write(carac)
					carac = dler.read(DownloadManager.BUFFER_SIZE)
				outfile.close()
				dler.stop()
			except:
				print "Erreur de téléchargement !"
	
	def getDownloader(self, url):
		#return self.dlFactory.create(....)
		return HttpDownloader(url);
	
	## Lance ou met en attente un téléchargement.
	# @param url l'url du fichier distant
	# @param outfile le chemin du fichier de sauvegarde
	# @param callback le DownloadCallback à tenir informé de l'état du téléchargement
	# @return le numéro du téléchargement
	def download (self, url, outFile, callback) :
		if self.mutex_toDl.locked():
			print "Mutex verrouillé, attention au dead lock !"
		self.mutex_toDl.acquire()
		self.toDl.append([url, outFile, callback])
		self.cond_toDl.notifyAll()
		self.mutex_toDl.release()
		pass

