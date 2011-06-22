# -*- coding:Utf-8 -*-

from AbstractDownloaderFactory import *

## Fabrique concrète des DownloaderInterface
class DownloaderFactory (AbstractDownloaderFactory) :
	def __init__(self) :
		pass
	
	## Crée un DownloaderInterface
	# @param url l'url du fichier à télécharger
	# @return un DownloaderInterface permettant le téléchargement du fichier distant
	def create (self, url) :
		# returns 
		pass

