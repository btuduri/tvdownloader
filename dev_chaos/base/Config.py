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

CONFIG_FILE = "toto.cfg"

class Config( object ):
	__metaclass__ = Singleton
	
	def __init__( self ):
		# Create ConfigParser instance
		self.configParser = ConfigParser.ConfigParser()
		# Create mutex
		self.mutex = threading.Lock()
		# Open config file
		self.open()
	
	@synchronized( self.mutex )
	def open( self ):
		if( os.path.exists( CONFIG_FILE ) ):
			self.configParser.read( CONFIG_FILE )
	
	@synchronized( self.mutex )
	def save( self ):
		# N.B. : only one thread has to call this function
		with open( CONFIG_FILE, "w" ) as configFile:
			self.configParser.write( configFile )
	
	@synchronized( self.mutex )
	def get( self, section, option ):
		if( self.configParser.has_option( section, option ) ):
			return self.configParser.get( section, option )
		else:
			return None
	
	@synchronized( self.mutex )
	def set( self, section, option, value ):
		if( not self.configParser.has_section( section ) ):
			self.configParser.add_section( section )
		self.configParser.set( section, option, value )
