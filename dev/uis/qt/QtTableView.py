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

class QtTableView( QtGui.QTableView ):
	"""
	Custom version of QTableView
	"""
	
	def __init__( self, parent = None ):
		QtGui.QTableView.__init__( self, parent )
		
		# No line number
		self.verticalHeader().setVisible( False )
		# No grid
		self.setShowGrid( False )
		# Always select only one line
		self.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
		self.setSelectionMode( QtGui.QAbstractItemView.SingleSelection )
		# Alternate colors
		self.setAlternatingRowColors( True )
		# Enable sorting
		self.setSortingEnabled( True )
	
	def resizeColumnsToContents( self ):
		"""
		Resize all columns
		"""
		QtGui.QTableView.resizeColumnsToContents( self )
		if( not self.horizontalScrollBar().isVisible() ):
			self.horizontalHeader().setStretchLastSection( True )
