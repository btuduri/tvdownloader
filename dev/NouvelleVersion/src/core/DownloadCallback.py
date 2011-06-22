# -*- coding:Utf-8 -*-

## Interface des callbacks de DownloaderManager;
#
# Un DownloadCallback est informé de l'état d'un téléchargement (progression, cas d'erreur) par le downloadManager. Voir DownloadManager.download.
class DownloadCallback :
	def __init__(self) :
		pass
	
	## Appelée lors d'un changement de l'état du téléchargement.
	# @param downloadNum le numéro du téléchargement
	# @param status le status du téléchargement (voir classe DownloadStatus)
	def downloadStatus (self, downloadNum, status) :
		# returns 
		pass

