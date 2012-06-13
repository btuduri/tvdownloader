#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Class
#

class QtLogWidget( QtGui.QTableWidget ):
	"""
	Widget to display Python log messages
	"""
	def __init__( self, parent = None ):
		# 0 rown 3 columns
		QtGui.QTableWidget.__init__( self, parent )
		self.setColumnCount( 3 )
		# Change columns names
		self.setHorizontalHeaderItem( 0, QtGui.QTableWidgetItem( "Type" ) )
		self.setHorizontalHeaderItem( 1, QtGui.QTableWidgetItem( "Fichier" ) )
		self.setHorizontalHeaderItem( 2, QtGui.QTableWidgetItem( "Message" ) )
		# Hide rows names
		self.verticalHeader().setVisible( False )
		# Always select all the line
		self.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
	
