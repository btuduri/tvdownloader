# -*- coding:Utf-8 -*-

import thread,threading,traceback,time
from util import Synchronized,SynchronizedWith,CallbackGroup

from DownloaderFactory import *
from TVDContext import TVDContext

import logging
logger = logging.getLogger( "TVDownloader" )
dmlogger = logger

class DownloadManager(threading.Thread):
	BUFFER_SIZE = 8000
	
	# Instance de la classe (singleton)
	__instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__(typ, *args, **kwargs):
		# On vérifie qu'on peut instancier
		context = TVDContext()
		if not(context.isInitialized()):
			logger.error("Le context n'est pas initialisé, impossible d'instancier")
			return None
		
		if DownloadManager.__instance == None:#Décorateur ?
			return super(DownloadManager, typ).__new__(typ, *args, **kwargs)
		else:
			return DownloadManager.__instance
	
	def __init__(self, start=False) :
		if DownloadManager.__instance != None:#Décorateur ?
			return
		threading.Thread.__init__(self)
		DownloadManager.__instance = self
		
		self.downloads = []
		self.downloadsToStop = []
		self.downloadsToPause = []
		self.downloadsToResume = []
		self.callbackGroup = CallbackGroup("downloadStatus")
		self.maxDownloads = 3
		self.maxSpeed = 0
		self.stopped = False
		self.nextNumDownload = 0

	def getMaxDownloads(self):
		return self.maxDownloads
	def setMaxDownloads(self, maxDownloads):
		self.maxDownloads = maxDownloads

	def getMaxSpeed(self):
		return self.maxSpeed
	def setMaxSpeed(self, maxSpeed):
		self.maxSpeed = maxSpeed
	
	@Synchronized
	def addDownloadCallback(self, callback):
		self.callbackGroup.add(callback)
	
	@Synchronized
	def removeDownloadCallback(self, callback):
		self.callbackGroup.remove(callback)
	
	def start(self):
		threading.Thread.start(self)
	
	def stop(self):
		self.stopped = True
	
	@Synchronized
	def pauseDownload(self, num):
		self.downloadsToPause.append(num)
	
	@Synchronized
	def resumeDownload(self, num):
		self.downloadsToResume.append(num)
	
	@Synchronized
	def stopDownload(self, num):
		self.downloadsToStop.append(num)
	
	@Synchronized
	def getDownloads(self):
		dls = []
		for dl in self.downloads:
			dls.append(
				dl.getStatus()
			)
		return dls
	
	@Synchronized
	def getActiveDownloads(self):
		res = []
		for dl in self.downloads:
			if dl.getStatus().status in [DownloadStatus.PAUSED, DownloadStatus.DOWN, DownloadStatus.QUEUED]:
				res.append(dl.getNum())
		return res
	
	def run(self):
		@SynchronizedWith(self)
		def retrieveDls():
			activeDls = []
			for dl in self.downloads:
				st = dl.getStatus().getStatus()
				if st == DownloadStatus.DOWN or st == DownloadStatus.PAUSED:
					#logger.debug("téléchargement actif: "+str(dl.getNum()))
					activeDls.append(dl)
			for newDl in self.downloads:
				if len(activeDls) >= self.maxDownloads:
					return activeDls
				if newDl.getStatus().getStatus() != DownloadStatus.QUEUED:
					continue
				logger.debug("démarrage du téléchargement: "+str(newDl.getNum()))
				newDl.start()
				if newDl.getStatus().getStatus() == DownloadStatus.DOWN:
					logger.debug("téléchargement en cours: "+str(newDl.getNum()))
					activeDls.append(newDl)
				else:
					logger.warning("Echec de lancement du téléchargement "+str(newDl.getNum()))
					newDl.getStatus().status = DownloadStatus.FAILED
				self.callbackGroup(newDl.getStatus())
			return activeDls
		@SynchronizedWith(self)
		def refreshStatuses():
			for num in self.downloadsToStop:
				stopDl(num)
			for num in self.downloadsToPause:
				pauseDl(num)
			for num in self.downloadsToResume:
				resumeDl(num)
		@SynchronizedWith(self)
		def stopDl(num):
			for dl in self.downloads:
				if dl.getStatus().getNum() == num:
					if dl.isDownloading() or dl.isPaused():
						logger.debug("arrêt téléchargement: "+str(dl.getNum()))
						dl.interrupt()
					elif dl.isQueued():
						logger.debug("annulation téléchargement: "+str(dl.getNum()))
						dl.cancel()
					self.callbackGroup(dl.getStatus())
					return
		@SynchronizedWith(self)
		def pauseDl(num):
			for dl in self.downloads:
				if dl.getStatus().getNum() == num:
					logger.debug("pause téléchargement: "+str(dl.getNum()))
					dl.pause()
					self.callbackGroup(dl.getStatus())
					return
		@SynchronizedWith(self)
		def resumeDl(num):
			for dl in self.downloads:
				if dl.getStatus().getNum() == num:
					logger.debug("reprise téléchargement: "+str(dl.getNum()))
					dl.resume()
					self.callbackGroup(dl.getStatus())
					return
		pause = 0
		while not(self.stopped):
			dmlogger.debug("Téléchargement...")
			activeDls = retrieveDls()
			if len(activeDls) == 0:
				dmlogger.debug("Pause, rien a dl")
				time.sleep(0.5)#Utiliser les cond...
			else:
				for dl in activeDls:
					if dl.isPaused():
						dmlogger.debug("téléchargement en pause: "+str(dl.getNum()))
					elif self.maxSpeed <= 0:
						dmlogger.debug("step sur téléchargement: "+str(dl.getNum()))
						dl.step()
						self.callbackGroup(dl.getStatus())
					else:
						before = time.time()
						success = dl.step()
						after = time.time()
						stepLength = dl.getLastStepLength()
						dmlogger.debug("step sur téléchargement "+str(dl.getNum())+": "+str(stepLength))
						if self.maxSpeed > 0:
							stepDelta = (after-before)#Temps de téléchargement du step
							stepSpeed = stepLength/stepDelta#Vitesse de téléchargement du step
							stepMinDelta = (1.0*stepLength)/(1.0*self.maxSpeed)#Temps de téléchargement avec maxSpeed
							pause = (stepMinDelta-stepDelta)#Ajout de la différence
							dmlogger.debug("pause: "+str(pause))
							if pause > 0:
								time.sleep(pause)
						self.callbackGroup(dl.getStatus())
				#if self.maxSpeed > 0 and pause > 0:
				#	dmlogger.debug("pause: "+str(pause))
				#	time.sleep(pause)
				#	pause = 0
			refreshStatuses()
		#Arrêt de tout les téléchargements
		for dl in self.downloads:
			stopDl(dl.getStatus().getNum())

	
	@Synchronized
	def download (self, fichier) :
		logger.debug("téléchargement "+str(self.nextNumDownload))
		logger.debug(fichier.lien)
		logger.debug(fichier.nomFichierSortie)
		dl = Download(fichier, self.nextNumDownload)
		self.downloads.append(dl)
		self.callbackGroup(dl.getStatus())
		res = self.nextNumDownload
		self.nextNumDownload = self.nextNumDownload+1
		return res

#TODO Différencier arrêt en cour et fin de dl
class Download :
	STEP_SIZE = 32000
	def __init__(self, fichier, num):
		self.fichier = fichier
		self.dler = fichier.getDownloader()
		self.num = num
		self.status = DownloadStatus(num, DownloadStatus.QUEUED, fichier.nom, 0)
		self.outfile = None
		self.lastStepLength = 0
	
	def start(self):
		if self.dler == None:
			return False
		try:
			self.outfile = open(self.fichier.nomFichierSortie, "w")#TODO Dossier de téléchargement !!
		except Exception:
			self.status.status = DownloadStatus.FAILED
			return False
		if not(self.dler.start()):
			self.outfile.close()
			self.status.status = DownloadStatus.FAILED
			return False
		self.status.status = DownloadStatus.DOWN
		self.status.size = self.dler.getSize()
		return True
	
	def interrupt(self):
		self.outfile.close()
		self.dler.stop()
		if self.status.status != DownloadStatus.COMPLETED:
			self.status.status = DownloadStatus.STOPPED
	
	def isQueued(self):
		return self.status.status == DownloadStatus.QUEUED
	
	def isPaused(self):
		return self.status.status == DownloadStatus.PAUSED
	
	def isDownloading(self):
		return self.status.status == DownloadStatus.DOWN
	
	def pause(self):
		if self.status.status == DownloadStatus.DOWN:
			self.status.status = DownloadStatus.PAUSED
	
	def cancel(self):
		if self.status.status == DownloadStatus.QUEUED:
			self.status.status = DownloadStatus.STOPPED
	
	def resume(self):
		if self.status.status == DownloadStatus.PAUSED:
			self.status.status = DownloadStatus.DOWN
	
	def getLastStepLength(self):
		return self.lastStepLength
	
	## Télécharge un bout du fichier.
	# @return True si réussit, False en cas d'échec, None en cas de fin de flux
	def step(self):
		self.lastStepLength = 0
		data = self.dler.read(Download.STEP_SIZE)
		if data == None:
			logger.debug("echec de step téléchargement "+str(self.num))
			self.status.status = DownloadStatus.FAILED
			return False
		dled = len(data)
		if dled == 0:
			logger.debug("dernière step téléchargement "+str(self.num))
			self.status.status = DownloadStatus.COMPLETED
			historique = TVDContext().historique
			if historique != None:
				historique.ajouterHistorique(self.fichier)
			else:
				logger.warning("erreur d'ajout à l'historique du téléchargement "+str(self.num))
			self.dler.stop()
			return None
		else:
			self.lastStepLength = dled
			logger.debug(str(dled)+" octets dans step téléchargement "+str(self.num))
			self.status.status = DownloadStatus.DOWN
			self.status.size = self.dler.getSize()
			self.outfile.write(data)
			self.status.downloaded = self.status.downloaded+dled
	
	def getStatus(self):
		return self.status
		
	def getNum(self):
		return self.status.getNum()

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
	def getStatusText(self):
		if self.status == DownloadStatus.QUEUED:
			return "QUEUED"
		elif self.status == DownloadStatus.PAUSED:
			return "PAUSED"
		elif self.status == DownloadStatus.DOWN:
			return "DOWN"
		elif self.status == DownloadStatus.STOPPED:
			return "STOPPED"
		elif self.status == DownloadStatus.FAILED:
			return "FAILED"
		elif self.status == DownloadStatus.COMPLETED:
			return "COMPLETED"
		else:
			return "INVALIDE"
	
	## Renvoie le nom du téléchargement, ce nom n'est pas unique et ne
	# peut pas servir d'identifiant
	# @return le nom du téléchargement
	def getName(self):
		return self.name
	
	def getNum(self):
		return self.num


