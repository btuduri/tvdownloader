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
	# @param s l'état dans lequel se trouve le téléchargement (QUEUED,PAUSED,DOWN,STOPPED,FAILED,COMPLETED)
	# @param sz la taille en octet du fichier téléchargé
	def __init__(self, p, s, sz=0):
		self.progress = p
		self.status = s
		self.size = sz
	
	## Renvoie la progression du téléchargement en %
	# @return un nombre entre 0 et 100 ou None si inconnue
	def getProgression(self):
		return self.progress
	
	## Renvoie la taille du fichier en cour de téléchargement.
	# @return la taille en octet ou 0 si inconnue
	def getSize(self):
		return self.size
	
	## Renvoie l'état dans lequel se trouve le téléchargement.
	# @return l'état parmis QUEUED,PAUSED,DOWN,STOPPED,FAILED,COMPLETED
	def getStatus(self):
		return self.status

