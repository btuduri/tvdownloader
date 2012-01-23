# -*- coding:Utf-8 -*-

import thread,threading,traceback
from util import SynchronizedMethod

from DownloaderFactory import *

#TODO Utiliser une structure de données dans le tableau de téléchargements
#TODO Gérer les callbacks de manière globale plutôt que par téléchargement (le garder en option ?)
#FIXME Gérer le nom du téléchargement (pas le nom du fichier de sortie)
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
			dlParam[2].downloadStatus(
				DownloadStatus(dlParam[3], DownloadStatus.STOPPED, dlParam[1])
			)
		self.toDl = []
		self.cond_toDl.notifyAll()
		self.mutex_toDl.release()
	
	@SynchronizedMethod
	def stopDownload(self, num):
		self.mutex_toDl.acquire()
		found = False
		for dlParam in self.toDl:
			if dlParam[3] == num:
				dlParam[2].downloadStatus(
					DownloadStatus(dlParam[3], DownloadStatus.STOPPED, dlParam[1])
				)
				found = True
				break
		if not(found):
			self.stpDl.append(num)
		self.mutex_toDl.release()
	
	@SynchronizedMethod
	def getActiveDownloads(self):
		dls = []
		self.mutex_toDl.acquire()
		for dlParam in self.toDl:
			dls.append(
				DownloadStatus(dlParam[3], DownloadStatus.STOPPED, dlParam[1])
			)
		self.mutex_toDl.release()
		return dls
	
	def run(self):
		while True:
			if self.mutex_toDl.locked():
				print "run: Mutex verrouillé, attention au dead lock !"
			self.mutex_toDl.acquire()
			while len(self.toDl) <= 0:
				if len(self.stpDl) > 0:
					for dlParam in self.toDl:
						if dlParam[3] in self.stpDl:
							dlParam[2].downloadStatus(
								DownloadStatus(dlParam[3], DownloadStatus.STOPPED, dlParam[1], 0)
							)
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
				dlParam[2].downloadStatus(
					DownloadStatus(dlParam[3], DownloadStatus.FAILED, dlParam[1], 0)
				)
				continue
			try:
				outfile = open(dlParam[1], "w")
				if dler.start():
					carac = dler.read(DownloadManager.BUFFER_SIZE)
					dled = len(carac)
					while len(carac) > 0:
						if dlParam[3] in self.stpDl:
							dlParam[2].downloadStatus(
								DownloadStatus(dlParam[3], DownloadStatus.STOPPED, dlParam[1], dled, dler.getSize())
							)
							break
						if self.stopped:
							dlParam[2].downloadStatus(
								DownloadStatus(dlParam[3], DownloadStatus.STOPPED, dlParam[1], dled, dler.getSize())
							)
							print "Arrêt!"
							return
						outfile.write(carac)
						carac = dler.read(DownloadManager.BUFFER_SIZE)
						dled = dled+len(carac)
						
						dlParam[2].downloadStatus(
							DownloadStatus(dlParam[3], DownloadStatus.DOWN, dlParam[1], dled, dler.getSize())
						)
					outfile.close()
					dler.stop()
					if not(self.stopped) and not(dlParam[3] in self.stpDl):
						dlParam[2].downloadStatus(
							DownloadStatus(dlParam[3], DownloadStatus.COMPLETED, dlParam[1], dled, dler.getSize())
						)
				else:
					print "Echec de téléchargement !"
					dlParam[2].downloadStatus(
						DownloadStatus(dlParam[3], DownloadStatus.FAILED, dlParam[1], 0)
					)
			except BaseException as e:
				print "Erreur de téléchargement !"
				dlParam[2].downloadStatus(
					DownloadStatus(dlParam[3], DownloadStatus.FAILED, dlParam[1], 0)
				)
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
	def download (self, name, url, outFile, callback) :
		if self.mutex_toDl.locked():
			print "down: Mutex verrouillé, attention au dead lock !"
		self.mutex_toDl.acquire()
		self.toDl.append([url, outFile, callback, self.nextNumDownload, outFile])
		self.cond_toDl.notifyAll()
		self.mutex_toDl.release()
		self.nextNumDownload = self.nextNumDownload+1
		#Appel au callback reporté pour appeler le callback après le return
		threading.Timer(0.01,
			callback.downloadStatus,
			(DownloadStatus(self.nextNumDownload, DownloadStatus.QUEUED, outFile, 0),)
		).start()
		#callback.downloadStatus(self.nextNumDownload, DownloadStatus(0, DownloadStatus.QUEUED, outFile))
		return self.nextNumDownload-1


## Interface des callbacks de DownloaderManager;
#
# Un DownloadCallback est informé de l'état d'un téléchargement (progression, cas d'erreur) par le downloadManager. Voir DownloadManager.download.
class DownloadCallback :
	def __init__(self) :
		pass
	
	## Appelée lors d'un changement de l'état d'un téléchargement.
	# @param status le status d'un téléchargement (voir classe DownloadStatus)
	def downloadStatus (self, status) :
		# returns 
		pass


## Représente l'état d'un téléchargement
class DownloadStatus :
	QUEUED = 0
	PAUSED = 1
	DOWN = 2
	STOPPED = 3
	FAILED = 4
	COMPLETED = 5
	
	## Constructeur
	# @param num le numéro du téléchargement
	# @param status l'état dans lequel se trouve le téléchargement
	# (QUEUED,PAUSED,DOWN,STOPPED,FAILED,COMPLETED)
	# @param name le nom du téléchargement (pour l'affichage)
	# @param downloaded la taille des données téléchargées (en octet)
	# @param size la taille en octet du fichier, None si inconnue
	# @param name le nom du téléchargement (pour l'affichage)
	def __init__(self, num, status, name, downloaded=0, size=None):
		self.num = num
		self.status = status
		self.name = name
		self.downloaded = downloaded
		self.size = size
	
	## Renvoie la taille des données téléchargées
	# @return le nombre d'octets téléchargés
	def getDownloaded(self):
		return self.downloaded
	
	## Renvoie la taille du fichier en cour de téléchargement.
	# @return la taille en octet ou None si inconnue
	def getSize(self):
		return self.size
	
	## Renvoie l'état dans lequel se trouve le téléchargement.
	# @return l'état parmis QUEUED,PAUSED,DOWN,STOPPED,FAILED,COMPLETED
	def getStatus(self):
		return self.status
	
	## Renvoie le nom du téléchargement, ce nom n'est pas unique et ne
	# peut pas servir d'identifiant
	# @return le nom du téléchargement
	def getName(self):
		return self.name


