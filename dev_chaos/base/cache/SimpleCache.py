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
	N.B : all function arguments must be hashable and kwards musn't be used
	"""
	def __init__( self ):
		# Cache dictionnary
		self.cacheDict = {} # { fnctArgs : result }
	
	def __call__( self, fnct ):
		"""
		Decorator
		"""
		@functools.wraps( fnct )
		def fnctCall( inst, *args ):
			if( self.cacheDict.has_key( args ):
				result = self.cacheDict[ args ]
			else:
				result = fnct( inst )
				self.cacheDict[ args ] = result
			return result
		return fnctCall
