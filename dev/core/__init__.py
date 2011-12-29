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
STATUS_DAEMON_NOT_FOUND = "démon introuvable"

STATUS = STATUS_NOT_INITIALIZED

ARG_SHARED_OBJECT = "--client"

PLUGIN_MANAGER = None
DOWNLOAD_MANAGER = None
HISTORIQUE = None

def initialiser():
	if ARG_SHARED_OBJECT in sys.argv[1:]:
		#TODO Récupérer les stubs
		a = 0
	else:
		PLUGIN_MANAGER = PluginManager()
		DOWNLOAD_MANAGER = DownloadManager()
		#TODO FICHIER_HISTORIQUE_TVD -> HISTORIQUE = Historique()
		#TODO Instancier les classes
		
		STATUS = STATUS_INITIALIZED
	return STATUS


