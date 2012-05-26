#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import collections
import functools
import mimetypes
import sys

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Classes
#

class CacheDict( collections.OrderedDict ):
	"""
	Custom ordered dict for Cache
	"""
	
	def __init__( self, *args, **kwargs ):
		collections.OrderedDict.__init__( self )
		self.update( *args, **kwargs )
	
	def __setitem__( self, key, value ):
		"""
		Set item ; item always go to the end of the dict
		"""
		if( self.has_key( key ) ):
			del self[ key ]
		collections.OrderedDict.__setitem__( self, key, value )
		
class Cache( object ):
	"""
	Cache decorator for browser methods
	"""
	
	def __init__( self, *decargs, **deckwargs ):
		# Max size of cache (default = 1 Mio)
		self.maxSize       = deckwargs.get( "maxSize", 1 * 1024 * 1024 )
		# Types accepted by cache (default = text)
		self.acceptedTypes = deckwargs.get( "acceptedTypes", [ "text" ] )
		# Cache dictionnary
		self.cacheDict     = CacheDict()
		# Number of calls since last cache clean
		self.lastClean     = 0
	
	def __call__( self, fnct ):
		"""
		Decorator
		"""
		@functools.wraps( fnct )
		def fnctCall( inst, url, *args, **kwargs ):
			if( self.cacheDict.has_key( url ) ):
				logger.debug( "GET %s" %( url ) )
				data = self.cacheDict[ url ]
				self.cacheDict[ url ] = data
				return data
			else:
				result = fnct( inst, url, *args, **kwargs )
				size   = sys.getsizeof( result )
				if( self.isAccepted( url, size ) ):
					self.cacheDict[ url ] = result
					self.clean()
				return result
		return fnctCall
	
	def isAccepted( self, url, size ):
		"""
		Check if this file can be added to cache
		"""
		# Check file size : can't be exceeded 10% of max size
		if( size > ( self.maxSize / 10 ) ):
			return False
		# Check file type
		urlType = mimetypes.guess_type( url )
		if( ( urlType is None ) or ( urlType[ 0 ] is None ) or ( urlType[ 0 ].split( "/" )[ 0 ] not in self.acceptedTypes ) ):
			return False
		# Ok
		return True
	
	def clean( self ):
		"""
		Clean the cache
		"""
		# Clean the cache after 10 adds
		if( self.lastClean >= 10 ):
			# Cache max size is exceeded
			if( sys.getsizeof( self.cacheDict ) > self.maxSize ):
				# Remove some elements
				self.cacheDict = CacheDict( list( self.cacheDict.iteritems() )[ -( len( self.cacheDict ) / 2 ) : ] )				
			self.lastClean = 0
		self.lastClean += 1
