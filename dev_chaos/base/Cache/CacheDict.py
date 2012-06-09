#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import collections

import logging
logger = logging.getLogger( "base.Cache.CacheDict" )

#
# Class
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
