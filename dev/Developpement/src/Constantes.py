#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier COPYING #
#########################################

# Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
# Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
# Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

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
REPERTOIRE_HOME                  = os.path.expanduser( "~" )
REPERTOIRE_TELECHARGEMENT_DEFAUT = os.path.join( REPERTOIRE_HOME, "TVDownloader" )
REPERTOIRE_CACHE                 = os.path.join( REPERTOIRE_HOME, ".tvdownloader", "cache" )
REPERTOIRE_CONFIGURATION         = os.path.join( REPERTOIRE_HOME, ".tvdownloader", "conf" )
REPERTOIRE_LOGS                  = os.path.join( REPERTOIRE_HOME, ".tvdownloader", "logs" )
REPERTOIRE_PLUGIN_PERSO          = os.path.join( REPERTOIRE_HOME, ".tvdownloader", "plugins" )

# des plugins
REPERTOIRES_PLUGINS = [ REPERTOIRE_PLUGIN_PERSO,
						"plugins" ]

# des fichiers
FICHIER_CONFIGURATION_TVD = os.path.join( REPERTOIRE_CONFIGURATION, "tvdownloader" )
