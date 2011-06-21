
## Interface des classes effectuant le téléchargement de fichiers distant.
#
#
class DownloaderInterface :
	## Démarre le téléchargement
	# Ne doit être appelée qu'une seul fois avant l'utilisation des méthodes read ou stop.
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

