#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Lancer : python setup.py py2exe
#

#
# Modules
#

import os

from distutils.core import setup
import py2exe

#
# Code
#

# Icones
listeIcones = []
for fichier in os.listdir( "ico" ):
	if( fichier[ -4 : ] == ".png" or fichier[ -4 : ] == ".ico" ):
		listeIcones.append( "ico/" + fichier )

setup( name = "pluzzdl",
	   version = "0.8.5",
	   author = "Chaoswizard",
	   url = "http://code.google.com/p/tvdownloader/",
	   license = "GNU General Public License 2(GPL 2)",
	   options = { "py2exe" : { "includes" : [ "sip" ] } },
	   data_files = [ ( "", [ "COPYING", "pluzzdl_default.cfg" ] ),
					  ( "ico", listeIcones )
					],
	   scripts = [ "mainGui.py" ],
	   windows = [ { "script" : "mainGui.py" } ] )
