#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import os
import sys

from Plugin import Plugin

import Constantes

import logging
logger = logging.getLogger( __name__ )

##########
# Classe #
##########

## Classe qui gere les plugins
class PluginManager( object ):
	
	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( PluginManager, self ).__new__( self )
		return self.instance
	
	## Constructeur
	def __init__( self ):
		self.listeInstances = {} # nomPlugin : son instance
		
		# Import de tous les plugins
		for rep in Constantes.REPERTOIRES_PLUGINS:
			# Verifie que le repertoire des plugins existe bien
			if( not os.path.isdir( rep ) ):
				logger.warn( "le repertoire %s des plugins n'existe pas..." %( rep ) )
			# Ajout du repertoire au path si necessaire
			if not( rep in sys.path ):
				sys.path.insert( 0, rep )
			# Importe les plugins
			self.importerPlugins( rep )
		# Instancie les plugins
		self.instancierPlugins()
		
	## Methode qui importe les plugins
	# @param rep Repertoire dans lequel se trouvent les plugins a importer
	def importerPlugins( self, rep ):
		for fichier in os.listdir( rep ): 
			# Tous les fichiers py autre que __init__.py sont des plugins a ajouter au programme
			if( fichier [ -3 : ] == ".py" and fichier.find( "__init__.py" ) == -1 ):
				# On suppose que c'est la derniere version du plugin
				derniereVersion = True
				# Pour les autres repertoires de plugins
				for autreRep in ( set( Constantes.REPERTOIRES_PLUGINS ).difference( set( [ rep ] ) ) ):
					# Si le fichier existe dans l'autre repertoire
					if( fichier in os.listdir( autreRep ) ):
						# Si la version du plugin de l'autre repertoire est plus recente
						if( os.stat( "%s/%s" %( autreRep, fichier ) ).st_mtime > os.stat( "%s/%s" %( rep, fichier ) ).st_mtime ):
							derniereVersion = False
							break # On arrete le parcourt des repertoires
				# Si ce n'est pas la derniere version
				if( not derniereVersion ):
					continue # Fichier suivant
				try :
					__import__( fichier.replace( ".py", "" ), None, None, [ '' ] )
				except ImportError :
					logger.error( "impossible d'importer le fichier %s" %( fichier ) )
					continue

	## Methode qui instancie les plugins
	# N.B. : doit etre lancee apres importerPlugins
	def instancierPlugins( self ):
		for plugin in Plugin.__subclasses__(): # Pour tous les plugins
			try:
				# Instance du plugin
				inst = plugin()
			except:
				logger.error( "impossible d'instancier le plugin %s" %( plugin ) )
				continue
			# Nom du plugin
			nom = inst.nomComplet
			# Ajout du plugin
			self.listeInstances[ nom ] = inst
	
	## Methode qui retourne la liste des sites/plugins
	# N.B. : doit etre lancee apres listerPlugins
	# @return La liste des noms des plugins
	def getListeSites( self ):
		return self.listeInstances.keys()
	
	## Methode qui retourne l'instance d'un plugin
	# @param nom Nom du plugin dont il faut recuperer l'instance
	# @return    Instance du plugin ou None s'il n'existe pas
	def getInstance( self, nom ):
		return self.listeInstances.get( nom, None )

	def addCallback( self, callback ) :
		pass
	
	def removeCallback( self, callback ) :
		pass
