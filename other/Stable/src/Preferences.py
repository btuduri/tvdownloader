#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier COPYING #
#########################################

# Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
# Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
# Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import os
import pickle
import logging
logger = logging.getLogger( __name__ )

from Navigateur import Navigateur
from PluginManager import PluginManager 

##########
# Classe #
##########

## Classe qui gere les preferences du logiciel
class Preferences( object ):

	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( Preferences, self ).__new__( self )
		return self.instance
	
	## Constructeur
	def __init__( self ):
		self.pluginManager = PluginManager()
		
		self.home = os.path.expanduser( "~" )
		self.fichierConfiguration = self.home + "/.tvdownloader/conf/tvdownloader"
		self.chargerConfiguration()

	## Methode qui charge les preferences du logiciel
	def chargerConfiguration( self ):
		# Parametres par defaut
		self.preferencesParDefault = { "repertoireTelechargement" : self.home + "/TVDownloader",
									   "pluginsActifs"            : [],
									   "pluginParDefaut"          : "",
									   "tailleFenetre"            : [ 500, 500 ],
									   "timeOut"                  : 5,
									   "nbThreadMax"              : 20
									 }		
		
		if os.path.exists( self.fichierConfiguration ): # Si le fichier existe, on le charge
			# On recupere les preferences dans le fichier
			fichier = open( self.fichierConfiguration, "r" )
			self.preferences = pickle.load( fichier )
			fichier.close()
			# On verifie qu'il ne nous manque pas une preference
			# Si c'est le cas, on prend sa valeur par defaut
			for elmt in self.preferencesParDefault.keys():
				if not self.preferences.has_key( elmt ):
					self.preferences[ elmt ] = self.preferencesParDefault[ elmt ]
		else: # Sinon, on utilise les parametres par defaut
			self.preferences = self.preferencesParDefault
		# On active les plugins qui doivent etre actifs
		for plugin in self.preferences[ "pluginsActifs" ]:
			self.pluginManager.activerPlugin( plugin )
			
		# On cree le repertoire de telechargement s'il n'existe pas
		if( not os.path.isdir( self.preferences[ "repertoireTelechargement" ] ) ):
			os.makedirs( self.preferences[ "repertoireTelechargement" ] )
		
		# On applique les preferences
		self.appliquerPreferences()
	
	## Methode qui applique certaines preferences du logiciel
	# Seuls les preferences des classes qui utilise le singleton sont applquees
	def appliquerPreferences( self ):
		Navigateur.timeOut     = self.preferences[ "timeOut" ]
		Navigateur.maxThread   = self.preferences[ "nbThreadMax" ]
	
	## Methode qui sauvegarde les preferences du logiciel		
	def sauvegarderConfiguration( self ):
		# On applique les preferences
		self.appliquerPreferences()
		
		# On sauvegarde les preferences dans le fichier de configuration
		fichier = open( self.fichierConfiguration, "w" )
		pickle.dump( self.preferences, fichier )
		fichier.close()
	
	## Methode qui renvoit une preference du logiciel
	# @param nomPreference Nom de la preference a renvoyer
	# @return Valeur de cette preference
	def getPreference( self, nomPreference ):
		try:
			return self.preferences[ nomPreference ]
		except KeyError:
			logger.warn( "preference %s inconnue" %( nomPreference ) )
			return None
	
	## Methode qui met en place la valeur d'une preference
	# @param nomPreference Nom de la preference dont on va mettre en place la valeur
	# @param valeur        Valeur a mettre en place
	def setPreference( self, nomPreference, valeur ):
		
		# Si on sauvegarde une nouvelle liste de plugin
		if( nomPreference == "pluginsActifs" ):
			nouvelleListe = valeur
			ancienneListe = self.preferences[ "pluginsActifs" ]
			# Pour chaque element dans l'union des 2 listes
			for elmt in ( set( nouvelleListe ).union( set( ancienneListe ) ) ):
				if( ( elmt in ancienneListe ) and not ( elmt in nouvelleListe ) ):
					self.pluginManager.desactiverPlugin( elmt )
				elif( ( elmt in nouvelleListe ) and not ( elmt in ancienneListe ) ):
					self.pluginManager.activerPlugin( elmt )
		
		# Dans tous les cas, on sauvegarde la preference
		self.preferences[ nomPreference ] = valeur
