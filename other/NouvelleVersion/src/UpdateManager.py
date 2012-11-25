#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import hashlib
import os
import os.path
import xml.sax
from xml.sax.handler import ContentHandler

from Navigateur import Navigateur

import logging
logger = logging.getLogger( __name__ )

#############
# Variables #
#############

# Repertoires qui contiennent des plugins
repPlugins = [ os.path.expanduser( "~" ) + "/.tvdownloader/plugins",
		       "plugins" ]

##########
# Classe #
##########

## Classe qui gere les plugins
class UpdateManager( object ):
	
	# Liste des sites qui disposent des mises a jour
	listeSites = [ "http://tvdownloader.googlecode.com/hg/plugins" ]

	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( UpdateManager, self ).__new__( self )
		return self.instance
	
	## Constructeur
	def __init__( self ):
		self.navigateur = Navigateur()
	
	## Methode pour generer le fichier XML de description des plugins
	@staticmethod
	def creerXML():
		# On ouvre le fichier XML
		try:
			fichierXML = open( "versionsPlugins.xml", "wt" )
		except:
			logger.error( "impossible d'ouvrir le fichier XML en ecriture" )
			return
		fichierXML.write( '<?xml version="1.0" encoding="UTF-8"?>\n' )
		fichierXML.write( "<plugins>\n" )
		
		# Pour chaque fichier de plugin
		for fichier in os.listdir( "plugins" ): 
			# Tous les fichiers .py autre que __init__.py sont des plugins
			if( fichier [ -3 : ] == ".py" and fichier.find( "__init__.py" ) == -1 ):
				fichierCheminComplet = "plugins/%s" %( fichier )
				# Nom du fichier
				nom  = fichier
				# Date de la derniere modification
				date = os.stat( fichierCheminComplet ).st_mtime
				# Somme de controle SHA1
				fichierPlugin = open( fichierCheminComplet, "rt" )
				sha1 = hashlib.sha1( fichierPlugin.read() ).hexdigest()
				fichierPlugin.close()
				# On ajoute l'element au fichier XML
				fichierXML.write( '\t<plugin nom="%s" dateModification="%s" sha1="%s"></plugin>\n' %( nom, date, sha1 ) )
		
		# On ferme le fichier XML
		fichierXML.write( "</plugins>\n" )
		fichierXML.close()
		
	## Methode qui verifie si les plugins disposent d'une mise a jour
	# @param site Sites sur lesquel aller chercher la mise a jour
	# @return     Liste des plugins a mettre a jour [ Nom du plugin, URL ou charger le plugin, SHA1 du plugin ]
	def verifierMiseAjour( self, site ):
		listePluginsXML         = [] # [ Nom, date derniere modification, SHA1 ]
		listePluginAMettreAJour = [] # [ Nom du plugin, URL ou charger le plugin, SHA1 du plugin ]
		handler                 = UpdateManagerHandler( listePluginsXML )
		
		# On recupere le fichier XML de description des plugins
		fichierXML = self.navigateur.getPage( "%s/versionsPlugins.xml" %( site ) )
		if( fichierXML == "" ): # Si on n'a rien recupere, on essaye un autre site
			logger.warn( "aucune information disponible sur le site %s" %( site ) )
			return []
		# On vide la liste
		del listePluginsXML[ : ]
		# On parse le fichier XML
		try:
			xml.sax.parseString( fichierXML, handler )
		except:
			logger.error( "impossible de parser le fichier XML du site %s" %( site ) )
			return []
		# Pour chaque plugin decrit dans le fichier XML
		for( nom, dateModification, sha1 ) in listePluginsXML:
			# On n'a pas une nouvelle version du plugin
			nouvelleVersion = False
			# Dans chacun des repertoires qui contiennent des plugins
			for rep in repPlugins:
				pluginCheminComplet = "%s/%s" %( rep, nom )
				# Si le plugin est present
				if( os.path.isfile( pluginCheminComplet ) ):
					# Si la version dont l'on dispose est moins recente que celle du site
					if( os.stat( pluginCheminComplet ).st_mtime < dateModification ):
						nouvelleVersion = True
					else:
						nouvelleVersion = False
						break # On peut arrete de chercher, on a deja le plus recent
			# S'il y a une nouvelle version
			if( nouvelleVersion ):
				listePluginAMettreAJour.append( [ nom, "%s/%s" %( site, nom ), sha1 ] )
		
		# On a fini de lire les infos sur ce site, pas besoin de parcourir les autres	
		return listePluginAMettreAJour
	
	# Methode pour installer la mise a jour d'un plugin
	# @param nomPlugin Nom du fichier du plugin a mettre a jour
	# @param urlPlugin URL ou charger le plugin
	# @param sha1      Somme de controle SHA1 du plugin
	# @return Si le plugin a ete correctement installe
	def mettreAJourPlugin( self, nomPlugin, urlPlugin, sha1 ):
		logger.info( "mise a jour du plugin %s" %( nomPlugin ) )
		# On telecharge le plugin
		codePlugin = self.navigateur.getPage( urlPlugin )
		if( codePlugin == "" ):
			return False
		# On verifie la somme de controle du plugin
		if( hashlib.sha1( codePlugin ).hexdigest() != sha1 ):
			logger.warn( "somme de controle incorrecte pour le fichier %s" %( urlPlugin ) )
			return False
		# On met en place le plugin
		fichier = open( "%s/%s" %( repPlugins[ 0 ], nomPlugin ), 'wt' )
		fichier.write( codePlugin )
		fichier.close()
		
		return True
			
#
# Parser XML pour le fichier versionsPlugins.xml
#

## Classe qui permet de lire le fichier XML versionsPlugins.xml
class UpdateManagerHandler( ContentHandler ):

	# Constructeur
	# @param listePluginsXML Liste des plugins que l'on va remplir 
	def __init__( self, listePluginsXML ):
		self.listePluginsXML = listePluginsXML # [ Nom, date derniere modification, SHA1 ]

	## Methode appelee lors de l'ouverture d'une balise
	# @param name  Nom de la balise
	# @param attrs Attributs de cette balise
	def startElement( self, name, attrs ):
		if( name == "plugin" ):
			nom              = attrs.get( "nom", "" )
			dateModification = attrs.get( "dateModification", "" )
			sha1             = attrs.get( "sha1", "" )
			self.listePluginsXML.append( [ nom, float( dateModification ), sha1 ] )

	## Methode qui renvoie les donnees d'une balise
	# @param data Donnees d'une balise
	def characters( self, data ):
		pass

	## Methode appelee lors de la fermeture d'une balise
	# @param name  Nom de la balise
	def endElement( self, name ):
		pass
	
