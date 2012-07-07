#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import logging

from base.qt.qtString import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Class
#

class QtLogHandler( logging.Handler ):
	"""
	Display Python logging messages with Qt ; use it with a QTableWidget widget
	"""
	
	# Colors
	red    = QtGui.QColor( 255, 0, 0, 127 )
	yellow = QtGui.QColor( 255, 255, 0, 127 )
	green  = QtGui.QColor( 0, 255, 0, 127 )
	white  = QtGui.QColor( 255, 255, 255, 127 )
	# Color levels
	colorLevel = { "ERROR" : red, "WARNING" : yellow, "CRITICAL" : red, "INFO" : green, "DEBUG" : white }
	
	def __init__( self, widget ):
		logging.Handler.__init__( self )
		self.widget   = widget
		self.formater = logging.Formatter( "%(levelname)s;%(filename)s;%(message)s" )
	
	def createItem( self, text, color ):
		"""
		Create new item to display
		"""
		item = QtGui.QTableWidgetItem( stringToQstring( text ) )
		item.setBackground( color )
		item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
		return item
	
	def emit( self, record ):
		"""
		Parse log message and display it
		"""
		typeMsg, fileMsg, msg =  self.formater.format( record ).split( ";" )
		color = self.colorLevel[ typeMsg ]
		self.widget.insertRow( 0 )
		self.widget.setItem( 0, 0, self.createItem( typeMsg, color ) )
		self.widget.setItem( 0, 1, self.createItem( fileMsg, color ) )
		self.widget.setItem( 0, 2, self.createItem( msg, color ) )		

	def createLock( self ):
		self.mutex = QtCore.QMutex()
	
	def acquire( self ):
		self.mutex.lock()
	
	def release( self ):
		self.mutex.unlock()
