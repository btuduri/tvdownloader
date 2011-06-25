# -*- coding:Utf-8 -*-

## Interface des classes effectuant le téléchargement de fichiers distant.
#
#
class DownloaderInterface :
	def __init__(self):
		pass
	
	## Démarre le téléchargement
	# Ne doit être appelée qu'une seul fois avant l'utilisation des méthodes read ou stop.
	# @return True en cas de réussite, False en cas d'échec
	def start(self):
		pass
	
	## Arrête le téléchargement
	def stop(self):
		pass
	
	## Lit et renvoie des octets du flux téléchargé.
	#
	# La méthode start doit avoir été appelé avant pour que le téléchargement soit lancé.
	# @param n le nombre d'octet à lire
	# @return une chaîne de charactère de taille maximale n ou de taille 0 en cas d'échec ou de fin du flux
	def read (self, n) :
		# returns byte[]
		pass
	
	## Renvoie la taille du fichier en cours de téléchargement.
	# La valeur renvoyer peut changer en fonction de l'état du téléchargement. Il est préférable de ne l'appeler après start() ou pendant le téléchargement.
	# @return la taille du téléchargement en cour en octets, None si inconnue
	def getSize(self):
		pass

