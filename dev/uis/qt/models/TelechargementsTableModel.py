#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

from base.qt.qtString import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Classe
#

class TelechargementsTableModel( QtCore.QAbstractTableModel ):
	"""
	Model pour afficher la liste des telechargements
	"""
	
	def __init__( self, listeTelechargements = [], parent = None ):
		QtCore.QAbstractTableModel.__init__( self, parent )
		self.listeTelechargements = listeTelechargements
		self.header = [ "Nom", "Avancement", "Vitesse", "Stopper" ]

	def addFile( self, file ):
		if( file not in self.listeTelechargements ):
			self.listeTelechargements.append( file )
			self.reset()
					
	def rowCount( self, parent ):
		return len( self.listeTelechargements )
		
	def columnCount( self, parent ):
		return len( self.header )
	
	def headerData( self, section, orientation, role ):
		if( orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole ):
			return QtCore.QVariant( self.header[ section ] )
		return QtCore.QVariant()
		
	def data( self, index, role ):
		if( not index.isValid ):
			return QtCore.QVariant()
		elif( role == QtCore.Qt.BackgroundRole ):
			if( index.row() % 2 == 0 ):
				return QtGui.QColor( QtCore.Qt.white )
			else:
				return QtGui.QColor( QtCore.Qt.lightGray )			
		elif( role == QtCore.Qt.DisplayRole ):
			if( index.column() == 0 ):
				return QtCore.QVariant( stringToQstring( self.listeTelechargements[ index.row() ].nom ) )
			elif( index.column() == 1 ):
				return QtCore.QVariant()
			elif( index.column() == 2 ):
				return QtCore.QVariant()
			elif( index.column() == 3 ):
				return QtCore.QVariant()
		else:
			return QtCore.QVariant()

