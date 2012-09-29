#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import ConfigParser
import os
import sys
import threading

from base.decorators import synchronized
from base.Patterns   import Singleton

import core.Constantes as Constantes

import logging
logger = logging.getLogger( "TVDownloader.Configuration" )

#
# Classe
#

# Create mutex
mutex = threading.Lock()

class Configuration( object ):
	__metaclass__ = Singleton
	
	TVD_REPERTOIRE_TELECHARGEMENT = ( "Telechargements", "dossier" )
	NAVIGATEUR_TIMEOUT            = ( "Navigateur", "timeout" )
	NAVIGATEUR_THREADS            = ( "Navigateur", "threads" )
	
	def __init__( self, configFileName = Constantes.FICHIER_CONFIGURATION_TVD, configFileNameDefaut = Constantes.FICHIER_CONFIGURATION_DEFAUT_TVD ):
		self.configFileName       = configFileName
		self.configFileNameDefaut = configFileNameDefaut
		
		# Create ConfigParser instances
		self.configParser       = ConfigParser.ConfigParser()
		self.configParserDefaut = ConfigParser.ConfigParser()
		# Open config files
		self.open()
	
	@synchronized( mutex )
	def open( self ):
		if( os.path.exists( self.configFileNameDefaut ) ):
			self.configParser.read( self.configFileNameDefaut )
		else:
			logger.warning( "Pas de fichier de configuration par defaut" )
		if( os.path.exists( self.configFileName ) ):
			self.configParser.read( self.configFileName )
		else:
			logger.info( "Pas de fichier de configuration par defaut ; creation" )
	
	@synchronized( mutex )
	def save( self ):
		# N.B. : only one thread has to call this function
		with open( self.configFileName, "w" ) as configFile:
			self.configParser.write( configFile )
	
	@synchronized( mutex )
	def get( self, elmt ):
		( section, option ) = elmt
		if( self.configParser.has_option( section, option ) ):
			return self.configParser.get( section, option )
		else:
			if( self.configParserDefaut.has_option( section, option ) ):
				logger.warning( "Utilisation de l'option par defaut pour %s [%s]" %( option, section ) )
				return self.configParserDefaut.get( section, option )
			else:
				logger.critical( "Impossible de trouver l'option %s [%s]" %( option, section ) )
				return None

	@synchronized( mutex )
	def set( self, elmt, value ):
		( section, option ) = elmt
		if( not self.configParser.has_section( section ) ):
			self.configParser.add_section( section )
		self.configParser.set( section, option, value )
