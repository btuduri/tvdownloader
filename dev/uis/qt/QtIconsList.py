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

class QtIconsList( QtGui.QScrollArea ):
	"""
	Widget to display a list of icons (QIcon)
	"""
	
	iconsSize = QtCore.QSize( 100, 100 )
	
	def __init__( self, parent = None ):
		QtGui.QScrollArea.__init__( self )
		self.setWidgetResizable( True )
		self.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
		self.setMinimumHeight( 125 )
		self.setMinimumWidth( 150 )
		# Widget
		self.widget = QtGui.QWidget( parent )
		self.setWidget( self.widget )
		# Vertical layout
		self.layout = QtGui.QVBoxLayout( self.widget )
		# Array to store icons names
		self.buttonsNames = []
		# Button group
		self.buttonGroup = QtGui.QButtonGroup( self.widget )
		self.buttonGroup.setExclusive( True )
		QtCore.QObject.connect( self.buttonGroup,
								QtCore.SIGNAL( "buttonClicked(int)" ),
								self.buttonClicked )
	
	def clear( self ):
		"""
		Clear icons list
		"""
		self.buttonsNames = []
		for button in self.buttonGroup.buttons():
			self.buttonGroup.removeButton( button )
			self.layout.removeWidget( button )
			button.close()
		
	def addIcon( self, name, icon = None ):
		"""
		Add an icon to the list
		icon must be a QIcon
		"""
		if( icon ):
			button = QtGui.QPushButton( icon, "", self.widget )
			button.setIconSize( self.iconsSize )
		else:
			button = QtGui.QPushButton( stringToQstring( name ), self.widget )
		button.setFlat( True )
		button.setCheckable( True )
		button.setToolTip( stringToQstring( name ) )
		self.layout.addWidget( button )
		self.buttonGroup.addButton( button, len( self.buttonsNames ) - 1 )
		self.buttonsNames.append( name )
	
	def buttonClicked( self, buttonId ):
		"""
		When a button is clicked, a signal is emitted with button name
		"""
		self.emit( QtCore.SIGNAL( "buttonClicked(PyQt_PyObject)" ), self.buttonsNames[ buttonId ] )
