#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import os
import sys

#############
# Variables #
#############

# du programme
TVD_NOM     = "TVDownloader"
TVD_VERSION = "0.8"

# du systeme
OS_UNIX    = False
OS_WINDOWS = False
if( sys.platform.lower()[ : 3 ] == "win" ):
	OS_WINDOWS = True
else:
	OS_UNIX    = True

# des chemins
if( "TVDOWNLOADER_HOME" in os.environ ):
	REPERTOIRE_HOME                  = os.path.join( os.environ[ "TVDOWNLOADER_HOME" ] )
	REPERTOIRE_CACHE                 = os.path.join( REPERTOIRE_HOME, "cache" )
	REPERTOIRE_CONFIGURATION         = os.path.join( REPERTOIRE_HOME, "config" )	
elif( "APPDATA" in os.environ ):
	REPERTOIRE_HOME                  = os.path.join( os.environ[ "APPDATA" ], "tvdownloader" )
	REPERTOIRE_CACHE                 = os.path.join( REPERTOIRE_HOME, "cache" )
	REPERTOIRE_CONFIGURATION         = os.path.join( REPERTOIRE_HOME, "config" )
else:
	REPERTOIRE_HOME                  = os.path.expanduser( "~" )
	REPERTOIRE_CACHE                 = os.path.join( REPERTOIRE_HOME, ".cache", "tvdownloader" )
	REPERTOIRE_CONFIGURATION         = os.path.join( REPERTOIRE_HOME, ".config", "tvdownloader" )
REPERTOIRE_LOGS                      = os.path.join( REPERTOIRE_CONFIGURATION, "logs" )
REPERTOIRE_PLUGIN_PERSO              = os.path.join( REPERTOIRE_CONFIGURATION, "plugins" )		
REPERTOIRE_TELECHARGEMENT_DEFAUT     = os.path.join( os.path.expanduser( "~" ), "Videos_TVDownloader" )

# des plugins
REPERTOIRES_PLUGINS = [ REPERTOIRE_PLUGIN_PERSO,
						"plugins" ]

# des fichiers
FICHIER_CONFIGURATION_TVD = os.path.join( REPERTOIRE_CONFIGURATION, "tvdownloader" )

# des caches
TAILLE_CACHE_IMAGE = 25
