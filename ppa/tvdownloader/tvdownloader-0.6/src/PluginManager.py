#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier COPYING #
#########################################

# Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
# Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
# Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

# N.B. :
# 	La gestion des plugins s'appuie sur cet article :
# 	http://lucumr.pocoo.org/2006/7/3/python-plugin-system

###########
# Modules #
###########

import sys
import os.path
from string import find
import logging
logger = logging.getLogger( __name__ )

from API import API
from Plugin import Plugin

#############
# Variables #
#############

# Repertoires qui contiennent des plugins
repPlugins = [ "plugins",
				os.path.expanduser( "~" ) + "/.tvdownloader/plugins" ]

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
		self.api            = API.getInstance()
		
		self.listePlugins   = {} # Clef : nomPlugin ; Valeur : classe du plugin (!= de son instance)
		self.listeInstances = {} # Clef : nomPlugin ; Valeur : son instance
		
		# On importe tous les plugins
		for rep in repPlugins:
			# On verifie que le repertoire des plugins existe bien
			if( not os.path.isdir( rep ) ):
				logger.warn( "le repertoire %s des plugins n'existe pas..." %( rep ) )
			# On l'ajoute au path si necessaire
			if not( rep in sys.path ):
				sys.path.insert( 0, rep )
			# On importe les plugins
			self.importPlugins( rep )
		# On liste les plugins
		self.listerPlugins()
	
	## Methode qui importe les plugins
	# @param rep Repertoire dans lequel se trouvent les plugins a importer
	def importPlugins( self, rep ):
		for root, dirs, files in os.walk( rep ): 
			for fichier in files: 
				# Tous les fichiers autre que __init__.py et des fichiers .pyc sont des plugins a ajouter au programme
				if( fichier [ -3 : ] == ".py" and fichier.find( "__init__.py" ) == -1 ):
					try :
						__import__( fichier.replace( ".py", "" ), None, None, [ '' ] )
					except ImportError :
						logger.error( "impossible d'importer le fichier %s" %( fichier ) )
						continue

	## Methode qui retourne la liste des sites/plugins
	# N.B. : On doit d'abord importer les plugins
	# @return La liste des noms des plugins
	def getListeSites( self ):
		return self.listePlugins.keys()
	
	## Methode qui liste les plugins
	def listerPlugins( self ):
		for plugin in Plugin.__subclasses__(): # Pour tous les plugins
			# On l'instancie
			inst = plugin()
			# On recupere son nom
			nom = getattr( inst, "nom" ) 
			# On ajoute le plugin a la liste des plugins existants
			self.listePlugins[ nom ] = plugin
	
	## Methode pour activer un plugin
	# @param nomPlugin Nom du plugin a activer
	def activerPlugin( self, nomPlugin ):
		if( self.listePlugins.has_key( nomPlugin ) ):
			instance = self.listePlugins[ nomPlugin ]()
			# On l'ajoute a la liste des instances
			self.listeInstances[ nomPlugin ] = instance
			# On l'ajoute a l'API
			self.api.ajouterPlugin( instance )
			self.api.activerPlugin( nomPlugin )
		else:
			logger.warn( "impossible d'activer le plugin %s" %( nomPlugin ) )
	
	## Methode qui desactive un plugin
	# @param nomPlugin Nom du plugin a desactiver
	def desactiverPlugin( self, nomPlugin ):
		# On le desactive dand l'API
		self.api.desactiverPlugin( nomPlugin )
		# On le supprime de la liste des instances
		if( self.listeInstances.has_key( nomPlugin ) ):
			self.listeInstances.pop( nomPlugin )
		else:
			logger.warn( "impossible de desactiver le plugin %s" %( nomPlugin ) )
		