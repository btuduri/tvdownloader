#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#



import logging
logger = logging.getLogger( "base.Patterns" )

#
# Classes
#

class Singleton( type ):
	"""
	Singleton pattern
	Use "__metaclass__ = Patterns.Singleton" to use it in our classes
	"""
	def __init__( cls, name, bases, dict ):
		super( Singleton, cls ).__init__( name, bases, dict )
		cls.instance = None 

	def __call__( cls, *args, **kwargs ):
		if( cls.instance is None ):
			cls.instance = super( Singleton, cls ).__call__( *args, **kwargs )
		return cls.instance
