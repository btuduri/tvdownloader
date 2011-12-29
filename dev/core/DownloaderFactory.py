# -*- coding:Utf-8 -*-

from AbstractDownloaderFactory import *
from HttpDownloader import *
from FtpDownloader import *
from MsdlDownloader import *
from DownloaderInterface import *

## Fabrique concrète des DownloaderInterface
class DownloaderFactory (AbstractDownloaderFactory) :
	def __init__(self) :
		pass
	
	## Crée un DownloaderInterface
	# @param url l'url du fichier à télécharger
	# @return un DownloaderInterface permettant le téléchargement du fichier distant ou None si aucun compatible
	def create (self, url) :
		if FtpDownloader.canDownload(url):
			return FtpDownloader(url)
		elif HttpDownloader.canDownload(url):
			return HttpDownloader(url)
		elif MsdlDownloader.canDownload(url):
			return MsdlDownloader(url)
		else:
			return None

