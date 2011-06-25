# -*- coding:Utf-8 -*-

## Représente l'état d'un téléchargement
class DownloadStatus :
	QUEUED = 0
	PAUSED = 1
	DOWN = 2
	STOPPED = 3
	FAILED = 4
	COMPLETED = 5
	
	## Constructeur
	# @param p la progession du téléchargement en %
	# @param s l'état dans lequel se trouve le téléchargement (QUEUE,PAUSED,DOWN,STOPPED,FAILED,COMPLETED)
	def __init__(self, p, s) :
		self.progress = p
		self.status = s
	
	## Renvoie la progression du téléchargement en %
	# @return un nombre entre 0 et 100 ou None si inconnue
	def getProgression(self):
		return self.progress
	
	## Renvoie l'état dans lequel se trouve le téléchargement.
	# @return l'état parmis QUEUE,PAUSED,DOWN,STOPPED,FAILED,COMPLETED
	def getStatus(self):
		return self.status

