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
		if os.path.exists( self.fichierConfiguration ): # Si le fichier existe, on le charge
			fichier = open( self.fichierConfiguration, "r" )
			self.preferences = pickle.load( fichier )
			fichier.close()
		else: # Sinon, on utilise les parametres par defaut
			self.preferences = { "repertoireTelechargement" : self.home + "/TVDownloader",
								 "pluginsActifs"            : [] 
							   }
		# On active les plugins qui doivent etre actifs
		for plugin in self.preferences[ "pluginsActifs" ]:
			self.pluginManager.activerPlugin( plugin )
	
	## Methode qui sauvegarde les preferences du logiciel		
	def sauvegarderConfiguration( self ):
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
			print "Preferences.getPreference : preference %s inconnue" %( nomPreference )
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
