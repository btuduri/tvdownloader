# -*- coding:Utf-8 -*-

from Downloaders import *


class AbstractDownloaderFactory :
	def __init__(self) :
		pass
	def create (self, url) :
		# returns DownloaderInterface
		pass


## Fabrique concrète des DownloaderInterface
class DownloaderFactory (AbstractDownloaderFactory) :
	def __init__(self) :
		AbstractDownloaderFactory.__init__(self)
	
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
		elif RtmpDownloader.canDownload(url):
			return RtmpDownloader(url)
		else:
			return None

