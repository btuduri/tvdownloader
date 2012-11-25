#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import datetime

from base.qt.qtString import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Classe
#

class FichiersTableModel( QtCore.QAbstractTableModel ):
	"""
	Model pour afficher la liste des fichiers
	"""
	
	def __init__( self, listeFichiers = [], parent = None ):
		QtCore.QAbstractTableModel.__init__( self, parent )
		self.listeFichiers = listeFichiers
		self.header = [ "", "Date", "Emission" ]
	
	def changeFiles( self, listeFichiers ):
		self.listeFichiers = listeFichiers
		self.reset()
	
	def rowCount( self, parent ):
		return len( self.listeFichiers )
		
	def columnCount( self, parent ):
		return len( self.header )
	
	def sort( self, column, order ):
		# Never sort first column
		if( column == 0 ):
			return
		
		# Order
		reverse = False
		if( order == QtCore.Qt.DescendingOrder ):
			reverse = True
		# Sort function
		if( column == 1 ):
			sortFnct = lambda x : x.date
		else:
			sortFnct = lambda x : x.nom
		# Sort
		self.emit( QtCore.SIGNAL( "layoutAboutToBeChanged()" ) )
		self.listeFichiers.sort( key = sortFnct, reverse = reverse )
		self.emit( QtCore.SIGNAL( "layoutChanged()" ) )
	
	def headerData( self, section, orientation, role ):
		if( orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole ):
			return QtCore.QVariant( self.header[ section ] )
		return QtCore.QVariant()
		
	def data( self, index, role ):
		if( not index.isValid() ):
			return QtCore.QVariant()
		elif( role == QtCore.Qt.BackgroundRole ):
			if( index.row() % 2 == 0 ):
				return QtGui.QColor( QtCore.Qt.white )
			else:
				return QtGui.QColor( QtCore.Qt.lightGray )			
		elif( role == QtCore.Qt.DisplayRole ):
			if( index.column() == 0 ):
				return QtCore.QVariant( "" )
			elif( index.column() == 1 ):
				date = self.listeFichiers[ index.row() ].date
				if( isinstance( date, datetime.date ) ):
					dateOk = date.strftime( "%a %d %b" )
				else:
					dateOk = date
				return QtCore.QVariant( stringToQstring( dateOk ) )
			else:
				return QtCore.QVariant( stringToQstring( self.listeFichiers[ index.row() ].nom ) )
		else:
			return QtCore.QVariant()
