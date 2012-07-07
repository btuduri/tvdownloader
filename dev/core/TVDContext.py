#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from lockfile import FileLock
import logging
logger = logging.getLogger( "TVDownloader" )
#import Constantes

import tvdcore

#{ Context de TVD.
# S'assure qu'aucun autre programme n'utilise actuellement le module de TVDownloader et instancie les plugins.
# Permet également de verrouiller les ressources qui doivent être libérées à la fin du programme
# et donne accès aux instances des classes principales de tvdcore.
class TVDContext(object):
	
	__FILE_LOCK = FileLock(tvdcore.REPERTOIRE_CONFIGURATION)
	
	## @var pluginManager
	# L'instance du gestionnaire de plugins
	
	## @var downloadManager
	# L'instance du gestionnaire de téléchargements
	
	## @var historique
	# L'instance de l'historique
	
	# Instance de la classe (singleton)
	__instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__(typ, *args, **kwargs):
		if TVDContext.__instance == None:
			#return super(object, typ).__new__(typ, *args, **kwargs)
			return object.__new__(typ, *args, **kwargs)
		else:
			return TVDContext.__instance
	
	def __init__(self, start=False) :
		if TVDContext.__instance != None:
			return
		object.__init__(self)
		TVDContext.__instance = self
		
		self.initialized = False
		
		self.downloadManager = None
		self.pluginManager = None
		self.historique = None
	
	## Indique si le context est initialisé.
	# A tester systématiquement avant d'éventuellement initialiser.
	# @return True si oui, False sinon
	def isInitialized(self):
		return self.initialized
	
	## Initialise le context et verrouille les ressources.
	# Instancie les classes principales (les 3 attributs) si aucun programme n'utilise actuellement le module tvdcore.
	# @return True en cas de réussite, False sinon
	def initialize(self):
		if TVDContext.__FILE_LOCK.is_locked():
			logger.error("Une autre instance de TVDownloader ou un programme utilisant tvdcore est lancé")
			return False
		try:
			TVDContext.__FILE_LOCK.acquire(20)
		except Exception as e:
			logger.error("Impossible de verrouiller les fichiers de configuration")
			return False
			
		self.initialized = True
		
		self.downloadManager = tvdcore.DownloadManager()
		self.pluginManager = tvdcore.PluginManager()
		self.historique = tvdcore.Historique()
		
		return True
	
	## Libère les ressourses.
	# Libère les fichiers de configuration de TVD pour le prochain lancement.
	# Doit être appelée avant la fin du programme mais pas par les UIs.
	def release(self):
		try:
			TVDContext.__FILE_LOCK.release()
		except Exception as e:
			logger.warn("Erreur de déverrouillage les fichiers de configuration")
			return
		
		self.initialized = False
		
		self.downloadManager = None
		self.pluginManager = None
		self.historique = None
	
	## Force la libération des ressourses.
	# Libèration forcée des fichiers de configuration de TVD.
	# Cela doit être utilisé uniquement dans le cas où les ressources
	# sont verrouillées et où aucune instance de TVD n'est lancée.
	def clean(self):
		try:
			TVDContext.__FILE_LOCK.break_lock()
		except Exception as e:
			logger.warn("Erreur de déverrouillage les fichiers de configuration")
			return

