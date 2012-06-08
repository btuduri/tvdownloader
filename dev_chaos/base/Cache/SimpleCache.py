#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import functools

import logging
logger = logging.getLogger( "base.Cache.SimpleCache" )

#
# Class
#

class SimpleCache( object ):
	"""
	Very simple cache decorator for class functions
	N.B : all function arguments must be hashable
	"""
	def __init__( self ):
		# Cache dictionnary
		self.cacheDict = {} # { fnctArgs : result }
	
	def __call__( self, fnct ):
		"""
		Decorator
		"""
		@functools.wraps( fnct )
		def fnctCall( inst, *args, **kwargs ):
			fkwargs = frozenset( kwargs.items() )
			if( self.cacheDict.has_key( ( args, fkwargs ) ) ):
				result = self.cacheDict[ ( args, fkwargs ) ]
				log.warning( "Found in cache" )
			else:
				result = fnct( inst, *args, **kwargs )
				self.cacheDict[ ( args, fkwargs ) ] = result
			return result
		return fnctCall
