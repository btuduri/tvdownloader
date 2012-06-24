#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import logging
import os
import re
import sys
sys.path.append( ".." ) 
import threading

from PyQt4 import QtCore
from PyQt4 import QtGui

from PluzzDL import PluzzDL

from QtLogHandler import QtLogHandler
from QtLogWidget  import QtLogWidget
from QtString     import stringToQstring
from QtString     import qstringToString

#
# Class
#

class MainWindow( QtGui.QMainWindow ):
	
	def __init__( self, pluzzdlVersion ):
		QtGui.QMainWindow.__init__( self )
		
		# App icons
		self.tvdIcon    = QtGui.QIcon( "ico/tvdownloader.png" )
		self.startIcon  = QtGui.QIcon( "ico/gtk-media-play-ltr.png" )
		self.stopIcon   = QtGui.QIcon( "ico/gtk-media-stop.png" )
		self.folderIcon = QtGui.QIcon( "ico/gtk-folder.png" )
		
		# Main window properties
		self.setWindowTitle( "pluzzdl %s" %( pluzzdlVersion ) )
		self.setWindowIcon( self.tvdIcon )
		self.resize( 570, 210 )
		
		# Central widget
		self.centralWidget = QtGui.QWidget( self )
		# URL label
		self.urlLabel   = QtGui.QLabel( "Entrer une URL valide :", self.centralWidget )
		# Line edit
		self.urlLineEdit = QtGui.QLineEdit( self.centralWidget )
		# Progress bar
		self.downloadProgressBar = QtGui.QProgressBar( self.centralWidget )
		self.downloadProgressBar.setValue( 0 )
		self.downloadProgressBar.setMaximum( 100 )
		# self.downloadProgressBar.setTextVisible( False )
		# Start/stop button
		self.startStopPushButton = QtGui.QPushButton( self.startIcon, "Start", self.centralWidget )
		self.startStopPushButton.setEnabled( False )
		self.downloadInProgress  = False
		# Open video folder button
		self.videoPushButton     = QtGui.QPushButton( self.folderIcon, "Ouvrir", self.centralWidget )
		# Logger
		self.logWidget = QtLogWidget( self )
		
		# Add all widgets to a grid layout
		self.gridLayout = QtGui.QGridLayout( self.centralWidget )
		self.gridLayout.addWidget( self.urlLabel, 0, 0, 1, 1 )
		self.gridLayout.addWidget( self.urlLineEdit, 0, 1, 1, 3 )
		self.gridLayout.addWidget( self.downloadProgressBar, 1, 0, 1, 2 )
		self.gridLayout.addWidget( self.startStopPushButton, 1, 2, 1, 1 )
		self.gridLayout.addWidget( self.videoPushButton, 1, 3, 1, 1 )
		self.gridLayout.addWidget( self.logWidget, 2, 0, 1, 4 )
		
		# Set central widget
		self.setCentralWidget( self.centralWidget )
		
		# Set logger
		logger  = logging.getLogger( "pluzzdl" )
		logger.setLevel( logging.INFO )
		self.logHandler = QtLogHandler( self.logWidget )
		logger.addHandler( self.logHandler )

		# Signals
		QtCore.QObject.connect( self.urlLineEdit,
								QtCore.SIGNAL( "textChanged(QString)" ),
								self.checkUrl )		
		QtCore.QObject.connect( self.startStopPushButton,
								QtCore.SIGNAL( "clicked()" ),
								self.startStopDownload )		
		QtCore.QObject.connect( self.videoPushButton,
								QtCore.SIGNAL( "clicked()" ),
								self.openVideoFolder )
		QtCore.QObject.connect( self, 
								QtCore.SIGNAL( "updateProgressBar(int)" ),
								self.downloadProgressBar.setValue )
		QtCore.QObject.connect( self, 
								QtCore.SIGNAL( "stopDownload()" ),
								self.stopDownload )
		
		self.downloadThread    = None 
		self.stopDownloadEvent = threading.Event()
		if( os.name == "nt" ):
			self.downloadDir = "."
		else:
			self.downloadDir = os.path.join( os.path.expanduser( "~" ), "pluzzdl" )

	def closeEvent( self, evt ):
		if( self.downloadInProgress is True ):
			self.stopDownload()
		evt.accept()

	def checkUrl( self, url ):
		if( re.match( "http://www.pluzz.fr/[^\.]+?\.html", url ) is None 
		and re.match( "http://www.francetv.fr/[^\.]+?", url ) is None ):
			self.startStopPushButton.setEnabled( False )
		else:
			self.startStopPushButton.setEnabled( True )		

	def startStopDownload( self ):
		if( self.downloadInProgress is True ):
			self.stopDownload()
		else:
			self.startDownload()
	
	def startDownload( self ):

		def dlVideo( url ):
			try:
				PluzzDL( url          = url,
						 useFragments = True,
						 proxy        = None,
						 resume    	  = True,
						 progressFnct = self.updateProgressBar,
						 stopDownloadEvent = self.stopDownloadEvent,
						 outDir = self.downloadDir )
			except:
				pass
			self.emit( QtCore.SIGNAL( "stopDownload()" ) )

		self.stopDownloadEvent.clear()
		self.downloadThread = threading.Thread( target = dlVideo, args = ( qstringToString( self.urlLineEdit.text() ), ) )
		self.downloadThread.start()
		self.downloadInProgress = True
		self.updateButtons()
	
	def stopDownload( self ):
		self.stopDownloadEvent.set()
		self.downloadThread.join()
		self.downloadInProgress = False
		self.updateButtons()

	def updateButtons( self ):
		if( self.downloadInProgress ):
			self.startStopPushButton.setIcon( self.stopIcon )
			self.startStopPushButton.setText( "Stop" )
		else:
			self.startStopPushButton.setIcon( self.startIcon )
			self.startStopPushButton.setText( "Start" )	
	
	def openVideoFolder( self ):
		QtGui.QDesktopServices.openUrl( QtCore.QUrl.fromLocalFile( self.downloadDir ) )
		
	def updateProgressBar( self, value ):
		self.emit( QtCore.SIGNAL( "updateProgressBar(int)" ), value )
