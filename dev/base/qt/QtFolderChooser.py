#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import os

from base.qt.qtString import qstringToString
from base.qt.qtString import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Class
#

class QtFolderChooser( QtGui.QWidget ):
	"""
	Widget to choose a folder
	"""
	
	def __init__( self, parent = None, icon = None ):
		QtGui.QWidget.__init__( self, parent )
		# Layout
		self.folderChooserLayout = QtGui.QHBoxLayout()
		self.setLayout( self.folderChooserLayout )
		# Line edit
		self.folderChooserLineEdit = QtGui.QLineEdit( parent )
		self.folderChooserLayout.addWidget( self.folderChooserLineEdit )
		# Push button
		self.folderChooserPushButton = QtGui.QPushButton( parent )
		if( icon ):
			self.folderChooserPushButton.setIcon( icon )
		QtCore.QObject.connect( self.folderChooserPushButton,
								QtCore.SIGNAL( "clicked()" ),
								self.folderChooser )		
		self.folderChooserLayout.addWidget( self.folderChooserPushButton )

	def folderChooser( self ):
		"""
		Open window
		"""
		currenDir = QtGui.QFileDialog.getExistingDirectory( None,
															u"",
															self.folderChooserLineEdit.text(),
															QtGui.QFileDialog.ShowDirsOnly 
													)
		if( os.path.isdir( currenDir ) ):
			self.folderChooserLineEdit.setText( currenDir )
			self.emit( QtCore.SIGNAL( "valueChanged(PyQt_PyObject)" ), currenDir )
	
	def getDir( self ):
		"""
		Get dir
		"""
		return qstringToString( self.folderChooserLineEdit.text() )
	
	def setDir( self, dirPath ):
		"""
		Set dir
		"""
		self.folderChooserLineEdit.setText( stringToQstring( dirPath ) )
