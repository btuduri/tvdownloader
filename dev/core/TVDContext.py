#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from lockfile import FileLock
import logging
logger = logging.getLogger( "TVDownloader" )
#import Constantes

import tvdcore

#{ Context de TVD.
# S'assure qu'aucun autre programme n'utilise actuellement le module de TVDownloader et instancie les plugins.
# Permet également de verrouiller les ressources qui doivent être libérées à la fin du programme.
class TVDContext(object):
	
	__FILE_LOCK = FileLock(tvdcore.REPERTOIRE_CONFIGURATION)
	
	## @var PluginManager
	# L'instance du gestionnaire de plugins
	
	## @var DownloadManager
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
	
	def isInitialized(self):
		return self.initialized
	
	## Initialise le context.
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
	# Doit être appelée avant la fin du programme.
	def release(self):
		try:
			TVDContext.__FILE_LOCK.release()
		except Exception as e:
			logger.warn("Erreur de déverrouillage les fichiers de configuration")
			return

