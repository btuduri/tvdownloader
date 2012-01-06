# -*- coding:Utf-8 -*-

import thread,threading,traceback
from util import SynchronizedMethod

from DownloaderFactory import *
from HttpDownloader import *
from FtpDownloader import *
from MsdlDownloader import *
from DownloadStatus import *

class DownloadManager(threading.Thread):
	BUFFER_SIZE = 8000
	
	# Instance de la classe (singleton)
	__instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__(typ, *args, **kwargs):
		if DownloadManager.__instance == None:
			return super(DownloadManager, typ).__new__(typ, *args, **kwargs)
		else:
			return DownloadManager.__instance
	
	def __init__(self, start=False) :
		if DownloadManager.__instance != None:
			return
		threading.Thread.__init__(self)
		DownloadManager.__instance = self
		self.RLOCK = threading.RLock()
		
		self.RLOCK = threading.RLock()
		
		self.nextNumDownload = 0 # int
		
		self.dlFactory = DownloaderFactory();
		
		self.toDl = []
		self.stpDl = []
		self.mutex_toDl = thread.allocate_lock()
		self.cond_toDl = threading.Condition(self.mutex_toDl)
		
		self.stopped = True
		if start:
			self.start()
	
	@SynchronizedMethod
	def start(self):
		self.stopped = False
		threading.Thread.start(self)
	
	@SynchronizedMethod
	def stop(self):
		self.mutex_toDl.acquire()
		self.stopped = True
		for dlParam in self.toDl:
			dlParam[2].downloadStatus(dlParam[3], DownloadStatus(0, DownloadStatus.STOPPED))
		self.toDl = []
		self.cond_toDl.notifyAll()
		self.mutex_toDl.release()
	
	@SynchronizedMethod
	def stopDownload(self, num):
		self.mutex_toDl.acquire()
		found = False
		for dlParam in self.toDl:
			if dlParam[3] == num:
				dlParam[2].downloadStatus(dlParam[3], DownloadStatus(0, DownloadStatus.STOPPED))
				found = True
				break
		if not(found):
			self.stpDl.append(num)
		self.mutex_toDl.release()
	
	def run(self):
		while True:
			if self.mutex_toDl.locked():
				print "run: Mutex verrouillé, attention au dead lock !"
			self.mutex_toDl.acquire()
			while len(self.toDl) <= 0:
				if len(self.stpDl) > 0:
					for dlParam in self.toDl:
						if dlParam[3] in self.stpDl:
							dlParam[2].downloadStatus(dlParam[3], DownloadStatus(0, DownloadStatus.STOPPED))
					self.stpDl = []
				if self.stopped:
					print "Arrêt!"
					self.mutex_toDl.release()
					return
				print "En attente..."
				self.cond_toDl.wait();
			dlParam = self.toDl.pop(0)
			self.mutex_toDl.release()
			
			print "Téléchargement de "+dlParam[0]+"..."
			dler = self.getDownloader(dlParam[0])
			if dler == None:
				dlParam[2].downloadStatus(dlParam[3], DownloadStatus(0, DownloadStatus.FAILED))
				continue
			try:
				outfile = open(dlParam[1], "w")
				if dler.start():
					carac = dler.read(DownloadManager.BUFFER_SIZE)
					dled = len(carac)
					last_perc = 0
					while len(carac) > 0:
						if dlParam[3] in self.stpDl:
							dlParam[2].downloadStatus(dlParam[3], DownloadStatus(last_perc, DownloadStatus.STOPPED))
							break
						if self.stopped:
							dlParam[2].downloadStatus(dlParam[3], DownloadStatus(last_perc, DownloadStatus.STOPPED))
							print "Arrêt!"
							return
						outfile.write(carac)
						carac = dler.read(DownloadManager.BUFFER_SIZE)
						dled = dled+len(carac)
						
						size = dler.getSize()
						new_perc = (100.0*dled)/size
						if size == None:
							dlParam[2].downloadStatus(dlParam[3], DownloadStatus(None, DownloadStatus.DOWN))
						elif new_perc > last_perc:
							dlParam[2].downloadStatus(dlParam[3], DownloadStatus(new_perc, DownloadStatus.DOWN))
						last_perc = new_perc
					outfile.close()
					dler.stop()
					if not(self.stopped) and not(dlParam[3] in self.stpDl):
						dlParam[2].downloadStatus(dlParam[3], DownloadStatus(last_perc, DownloadStatus.COMPLETED))
				else:
					print "Echec de téléchargement !"
					dlParam[2].downloadStatus(dlParam[3], DownloadStatus(0, DownloadStatus.FAILED))
			except BaseException as e:
				print "Erreur de téléchargement !"
				dlParam[2].downloadStatus(dlParam[3], DownloadStatus(0, DownloadStatus.FAILED))
				traceback.print_exc(e)
		print "Arrêt anormal!"
	
	# Renvoie None si aucun downloader trouvé
	def getDownloader(self, url):
		return self.dlFactory.create(url)
	
	## Lance ou met en attente un téléchargement.
	# @param url l'url du fichier distant
	# @param outfile le chemin du fichier de sauvegarde
	# @param callback le DownloadCallback à tenir informé de l'état du téléchargement
	# @return le numéro du téléchargement
	@SynchronizedMethod
	def download (self, url, outFile, callback) :
		if self.mutex_toDl.locked():
			print "down: Mutex verrouillé, attention au dead lock !"
		self.mutex_toDl.acquire()
		self.toDl.append([url, outFile, callback, self.nextNumDownload])
		callback.downloadStatus(self.nextNumDownload, DownloadStatus(0, DownloadStatus.QUEUED))
		self.cond_toDl.notifyAll()
		self.mutex_toDl.release()
		self.nextNumDownload = self.nextNumDownload+1

