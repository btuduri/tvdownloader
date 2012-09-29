#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

from base.qt.qtString import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Class
#

class QtTable( QtGui.QTableWidget ):
	"""
	Custom version of QTableWidget
	"""
	
	def __init__( self, parent = None ):
		QtGui.QTableWidget.__init__( self, parent )
		
		# No line number
		self.verticalHeader().setVisible( False )
		# No grid
		self.setShowGrid( False )
		# Always select only one line
		self.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
		self.setSelectionMode( QtGui.QAbstractItemView.SingleSelection )
		# Alternate colors
		self.setAlternatingRowColors( True )
	
	def resizeColumnsToContents( self ):
		"""
		Resize all columns
		"""
		QtGui.QTableWidget.resizeColumnsToContents( self )
		if( not self.isHorizontalScrollBarVisible() ):
			self.horizontalHeader().setStretchLastSection( True )

	def clear( self ):
		"""
		Clear contents
		"""
		for i in range( self.rowCount() - 1, -1, -1 ): # [ nbLignes - 1, nbLignes - 2, ..., 1, 0 ]
			self.removeRow( i )
		self.resizeColumnsToContents()

	def isHorizontalScrollBarVisible( self ):
		"""
		Is horizontal scroll bar visible ?
		"""
		isVisible = False
		
		columnSize = 0
		for i in range( self.columnCount() ):
			columnSize += self.columnWidth( i )
			
		widgetSize = self.width()
		
		if( columnSize > widgetSize ):
			isVisible = True
			
		return isVisible
	
	def createItem( self, text, editable = False, checkBox = False, checked = False ):
		"""
		Return a new item for QtTable
		"""
		item = QtGui.QTableWidgetItem( stringToQstring( text ) )
		item.setTextAlignment( QtCore.Qt.AlignCenter )
		if( not editable ):
			item.setFlags( item.flags() & ~QtCore.Qt.ItemIsEditable )
		if( checkBox ):
			if( checked ):
				item.setCheckState( QtCore.Qt.Checked )
			else:
				item.setCheckState( QtCore.Qt.Unchecked )
		return item
		
	def getLine( self, row ):
		"""
		Get a line (use it with setLine)
		"""
		line = []
		for i in range( self.columnCount() ):
			line.append( self.takeItem( row, i ) )
		return line		
	
	def copyLine( self, row ):
		"""
		Get a line (use it with setLine)
		"""
		line = []
		for i in range( self.columnCount() ):
			line.append( self.item( row, i ).clone() )
		return line				
	
	def setLine( self, row, line ):
		"""
		Set a line (use it with getLine and copyLine)
		"""
		columnNum = self.columnCount()
		if( len( line ) == columnNum ):
			for i in range( columnNum ):
				self.setItem( row, i, line[ i ] )
	
	def swapLines( self, row1, row2 ):
		"""
		Swap two lines
		"""
		if( row1 != row2 ):
			line1 = self.getLine( row1 )
			self.setLine( row1, self.getLine( row2 ) )
			self.setLine( row2, line1 )
