#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import functools

import logging
logger = logging.getLogger( "base.decorators" )

#
# Decorators
#

def deprecated( fnct ):
	"""
	Decorator to mark deprecated function
	"""
	@functools.wraps( fnct )
	def logDeprecated( *args, **kwargs ):
		logger.warning( "Deprecated function %s ; don't use it !" %( fnct.__name__ ) )
		return fnct( *args, **kwargs )
	return logDeprecated

def synchronized( lock ):
	"""
	Decorator to synchronize several methods with a given lock
	"""
	def wrapper( fnct ):
		@functools.wraps( fnct )
		def sync( *args, **kwargs ):
			with lock:
				return fnct( *args, **kwargs )
		return sync
	return wrapper
