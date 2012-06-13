#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Infos
#

__author__  = "Chaoswizard"
__license__ = "GPL 2"
__version__ = "0.8.5"
__url__     = "http://code.google.com/p/tvdownloader/"

#
# Modules
#

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

from MainWindow import MainWindow

#
# Main
#

if( __name__ == "__main__" ) :
	app = QtGui.QApplication( sys.argv )
	window = MainWindow( __version__ )
	window.show()
	sys.exit( app.exec_() )
