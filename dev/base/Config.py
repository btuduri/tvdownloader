#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import ConfigParser
import os
import threading

from base.decorators import synchronized
from base.Patterns   import Singleton

import logging
logger = logging.getLogger( "base.Config" )

#
# Classe
#

# Create mutex
mutex = threading.Lock()

class Config( object ):
	__metaclass__ = Singleton
	
	def __init__( self, configFileName ):
		self.configFileName = configFileName
		
		# Create ConfigParser instance
		self.configParser = ConfigParser.ConfigParser()
		# Open config file
		self.open()
	
	@synchronized( mutex )
	def open( self ):
		if( os.path.exists( self.configFileName ) ):
			self.configParser.read( self.configFileName )
	
	@synchronized( mutex )
	def save( self ):
		# N.B. : only one thread has to call this function
		with open( self.configFileName, "w" ) as configFile:
			self.configParser.write( configFile )
	
	@synchronized( mutex )
	def get( self, section, option ):
		if( self.configParser.has_option( section, option ) ):
			return self.configParser.get( section, option )
		else:
			return None
	
	@synchronized( mutex )
	def set( self, section, option, value ):
		if( not self.configParser.has_section( section ) ):
			self.configParser.add_section( section )
		self.configParser.set( section, option, value )
