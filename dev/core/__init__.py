#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from AbstractDownloaderFactory import *
from Constantes                import *
from DownloadCallback          import *
from DownloaderFactory         import *
from DownloaderInterface       import *
from DownloadManager           import *
from DownloadStatus            import *
from Historique                import *
from HttpDownloader            import *
from Fichier                   import *
from FtpDownloader             import *
from MsdlDownloader            import *
from Navigateur                import *
from Option                    import *
from PluginCache               import *
from PluginCallback            import *
from Plugin                    import *
from PluginManager             import *
from PluginStatus              import *

import sys

STATUS_NOT_INITIALIZED = "non initialisé"
STATUS_INITIALIZED = "initialisé"
STATUS_SHARED_OBJECT_ERROR = "erreur avec les objets distribués"

STATUS = STATUS_NOT_INITIALIZED

ARG_SHARED_OBJECT = "--shared"
SHARED_OBJECT_AUTHKEY = "tvd"
SHARED_OBJECT_ADDRESS = ('', 5096)

PLUGIN_MANAGER = None
DOWNLOAD_MANAGER = None
HISTORIQUE = None

def initialiser():
	global STATUS,PLUGIN_MANAGER,DOWNLOAD_MANAGER,HISTORIQUE
	if ARG_SHARED_OBJECT in sys.argv[1:]:
		#TODO Récupérer les stubs
		import multiprocessing
		from multiprocessing.managers import BaseManager

		BaseManager.register('pluginManager')
		BaseManager.register('downloadManager')
		BaseManager.register('historique')

		manager = BaseManager(SHARED_OBJECT_ADDRESS, SHARED_OBJECT_AUTHKEY)
		try:
			manager.connect()
			
			PLUGIN_MANAGER = manager.pluginManager()
			DOWNLOAD_MANAGER = manager.downloadManager()
			HISTORIQUE = manager.historique()
			STATUS = STATUS_INITIALIZED
		except Exception as e:
			print e
			STATUS = STATUS_SHARED_OBJECT_ERROR
	else:
		PLUGIN_MANAGER = PluginManager()
		DOWNLOAD_MANAGER = DownloadManager()
		#TODO FICHIER_HISTORIQUE_TVD -> HISTORIQUE = Historique()
		#TODO Instancier les classes
		
		STATUS = STATUS_INITIALIZED
	return STATUS


