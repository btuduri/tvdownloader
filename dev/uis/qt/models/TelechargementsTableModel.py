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
	
	def __init__( self, listeStatus = [], parent = None ):
		QtCore.QAbstractTableModel.__init__( self, parent )
		self.listeStatus = listeStatus
		self.header = [ "Nom", "Avancement", "Taille", "Etat", "Stopper" ]

	def addStatus( self, status ):
		if( status not in self.listeStatus ):
			self.listeStatus.append( status )
		else:
			self.listeStatus[ self.listeStatus.index( status ) ] = status
		self.reset()
					
	def rowCount( self, parent ):
		return len( self.listeStatus )
		
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
			if( index.column() == 0 ): # Nom
				return QtCore.QVariant( stringToQstring( self.listeStatus[ index.row() ].name ) )
			elif( index.column() == 1 ): # Avancement
				taille       = self.listeStatus[ index.row() ].downloaded
				tailleTotale = self.listeStatus[ index.row() ].size
				if( tailleTotale is None or tailleTotale <= 0 ):
					pourcent = "???"
				else:
					pourcent = "%.2f %%" %( 100 * taille / float( tailleTotale ) )
				return QtCore.QVariant( stringToQstring( pourcent ) )
			elif( index.column() == 2 ): # Taille
				taille = self.listeStatus[ index.row() ].downloaded
				if( taille < 1024 ):
					tailleString = "%.2f o" %( taille )
				elif( taille < 1024 * 1024 ):
					tailleString = "%.2f  Kio" %( taille / 1024.0 )
				else:
					tailleString = "%.2f  Mio" %( taille / ( 1024.0 * 1024.0 ) )
				return QtCore.QVariant( stringToQstring( tailleString ) )
			elif( index.column() == 3 ): # Etat
				return QtCore.QVariant( stringToQstring( self.listeStatus[ index.row() ].getStatusText().title() ) )
			elif( index.column() == 4 ): # Stopper
				return QtCore.QVariant( stringToQstring( "Pas encore..." ) )
		else:
			return QtCore.QVariant()

