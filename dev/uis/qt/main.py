#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import sys

import tvdcore

from PyQt4 import QtGui

from uis.qt.MainWindow import MainWindow

#
# Code
#

ctx = tvdcore.TVDContext()
if not( ctx.isInitialized() ) and not( ctx.initialize() ):
	logger.error( "Impossible d'initialiser le context" )
else:
	app = QtGui.QApplication( sys.argv )
	window = MainWindow( "1.0" )
	window.show()
	print app.exec_()
	# sys.exit( app.exec_() )
