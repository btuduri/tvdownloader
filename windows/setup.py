#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Lancer : python setup.py py2exe
#

###########
# Modules #
###########

import os

from distutils.core import setup
import py2exe

########
# Code #
########

#
# Liste des fichiers à inclure au programme
#

# Icones
listeIcones = []
for fichier in os.listdir( "ico" ):
	if( fichier[ -4 : ] == ".png" ):
		listeIcones.append( "ico/" + fichier )

# Images
listeImages = []
for fichier in os.listdir( "img" ):
	if( fichier[ -4 : ] == ".png" ):
		listeImages.append( "img/" + fichier )

# Plugins
listePlugins = []
for fichier in os.listdir( "plugins" ):
	if( fichier[ -3 : ] == ".py" ):
		listePlugins.append( "plugins/" + fichier )

setup( name = "TVDownloader",
	   version = "0.7",
	   author = "Chaoswizard",
	   url = "http://code.google.com/p/tvdownloader/",
	   license = "GNU General Public License 2(GPL 2)",
	   options = { "py2exe" : { "includes" : [ "mechanize", "sip" ] } },
	   data_files = [ ( "", [ "COPYING" ] ),
					  ( "ico", listeIcones ), 
					  ( "img", listeImages ),
					  ( "plugins", listePlugins )
					],
	   scripts = [ "main.py" ],
	   windows = [ { "script" : 'main.py' } ] )
