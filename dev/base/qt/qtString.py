#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

from PyQt4 import QtCore

import unicodedata

#
# Functions
#

def stringToQstring( text ):
	"""
	Convert a Python string to a Qt string
	"""
	if( isinstance( text, str ) ):
		return QtCore.QString( unicode( text, "utf-8", "replace" ) )
	else:
		return QtCore.QString( text )


def qstringToString( text ):
	"""
	Convert a Qt string to a Python string
	"""
	return unicode( text.toUtf8(), "utf-8" )
	# try:
		# return str( text.toUtf8() )
	# except UnicodeDecodeError:
		# return unicode( text.toUtf8(), "utf-8" )
