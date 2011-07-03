# -*- coding:Utf-8 -*-

from AbstractDownloaderFactory import *
from HttpDownloader import *
from FtpDownloader import *

## Fabrique concrète des DownloaderInterface
class DownloaderFactory (AbstractDownloaderFactory) :
	def __init__(self) :
		pass
	
	## Crée un DownloaderInterface
	# @param url l'url du fichier à télécharger
	# @return un DownloaderInterface permettant le téléchargement du fichier distant ou None si aucun compatible
	def create (self, url) :
		if url[:4] == "ftp:":
			return FtpDownloader(url)
		elif url[:5] == "http:":
			return HttpDownloader(url)
		else:
			return None

