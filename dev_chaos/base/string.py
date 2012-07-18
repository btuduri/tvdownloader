#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import unicodedata
import re
import string

import logging
logger = logging.getLogger( "base.string" )

#
# Functions
#

def removeAccents( myStr ):
	"""
	Removes all accents
	"""
	if( isinstance( myStr, str ) ):
		myStr = unicode( myStr, "utf8", "replace" )
	myStr = unicodedata.normalize( 'NFD', myStr )
	myStr = myStr.encode( 'ascii', 'ignore' )
	return myStr

def toFileName( myStr ):
	"""
	Transform string to usable filename
	"""
	myStr = removeAccents( myStr )
	myStr = "".join( [ char for char in myStr if char in string.ascii_letters or char in string.digits or char == " " or char == "." ] )
	myStr = re.sub( r"\s+", "_", myStr )
	return myStr
