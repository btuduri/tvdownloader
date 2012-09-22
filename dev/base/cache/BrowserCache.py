#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import functools
import mimetypes
import sys

from base.cache.CacheDict import CacheDict

import logging
logger = logging.getLogger( "base.Cache.BrowserCache" )

#
# Class
#

class BrowserCache( object ):
	"""
	Cache decorator for browser's functions
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
		def fnctCall( inst, url, data = None ):
			# Transform data to frozenset
			if( data is None ):
				fdata = None
			else:
				fdata = frozenset( data.items() )
			# Get page
			if( self.cacheDict.has_key( ( url, fdata ) ) ):
				logger.debug( "GET %s" %( url ) )
				page = self.cacheDict[ ( url, fdata ) ]
				self.cacheDict[ ( url, fdata ) ] = page
			else:
				page = fnct( inst, url, data )
				size = sys.getsizeof( page )
				if( self.isAccepted( url, size ) ):
					self.cacheDict[ ( url, fdata ) ] = page
					self.clean()
			return page
		return fnctCall
	
	def isAccepted( self, url, size ):
		"""
		Check if this file can be added to cache
		"""
		# Check bad url
		if( url is None or len( url ) == 0 ):
			return False
		# Check file size : can't be exceeded 10% of max size
		if( size > ( self.maxSize / 10 ) ):
			return False
		# Check if it's an accepted extension
		if( url[ -4 : ] in [ ".php", ".xml" ] ):
			return True
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
