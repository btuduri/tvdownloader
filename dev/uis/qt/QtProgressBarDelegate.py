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

class QtProgressBarDelegate( QtGui.QItemDelegate ):
	"""
	Delegate for a QProgressBar
	"""
	
	def __init__( self, parent = None ):
		QtGui.QItemDelegate.__init__( self, parent )
		
		self.percent = 0
	
	def paint( self, painter, option, index ):
		"""
		
		"""
		opts = QtGui.QStyleOptionProgressBarV2()
		opts.rect = option.rect
		opts.minimum = 1
		opts.maximum = 100
		opts.progress = self.percent
		opts.textVisible = True
		opts.text = QtCore.QString( "%d%%" %( self.percent ) )
		QtGui.QApplication.style().drawControl( QtGui.QStyle.CE_ProgressBar, opts, painter )
