#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Infos
#

__author__  = "Chaoswizard"
__license__ = "GPL 2"
__version__ = "0.9.2"
__url__     = "http://code.google.com/p/tvdownloader/"

#
# Modules
#

import os
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

from MainWindow import MainWindow

#
# Main
#

if( __name__ == "__main__" ) :
	
	# Creation des repertoires de travail
	if( os.name == "nt" ):
		pluzzdlDirs = [ "Videos" ]
	else:
		pluzzdlDirs = [ os.path.join( os.path.expanduser( "~" ), "pluzzdl" ) ]
	for pluzzdlDir in pluzzdlDirs:
		if( not os.path.isdir( pluzzdlDir ) ):
			os.makedirs( pluzzdlDir )
	
	# Lancement de la GUI
	app = QtGui.QApplication( sys.argv )
	window = MainWindow( __version__ )
	window.show()
	sys.exit( app.exec_() )
