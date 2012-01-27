#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import HTMLParser
# import datetime
# import os.path
import re
# import xml.sax

import tvdcore

import logging
logger = logging.getLogger( "TVDownloader" )

#
# Filtre Wireshark :
#    http.host contains "tf1" or http.host contains "wat"
#

#
# Classe
#

class TF1( tvdcore.Plugin ):
	
	listeChaines = { u"Séries étrangères"   : "/series-etrangeres/", 
					 u"Fictions françaises" : "/fictions-francaises/", 
					 u"Téléréalités"        : "/telerealites/", 
					 u"Magazine"            : "/magazine/", 
					 u"Divertissement"      : "/divertissement/", 
					 u"Info"                : "/programmes-tv-info/", 
					 u"Sport"               : "/sport/", 
					 u"Jeux tv"             : "/jeux-tv/" }
	
	def __init__( self ):
		tvdcore.Plugin.__init__( self, "TF1", "http://videos.tf1.fr", 1, "TF1.jpg" )
		
	def rafraichir( self ):
		pass
		
	def listerChaines( self ):
		for chaine in self.listeChaines.keys():
			self.ajouterChaine( chaine )
	
	def listerEmissions( self, chaine ):
		if( self.listeChaines.has_key( chaine ) ):
			urlChaine  = "http://videos.tf1.fr%s" %( self.listeChaines[ chaine ] )
			self.listeEmissions = {} # Clefs = nom de l'emission, Valeurs = {} avec clefs = nom du programme, valeurs = lien de la page
			# Recupere la premiere page
			page = self.getPage( urlChaine )
			# Extrait le nombre max de pages
			try :
				pageMax = re.findall( "<li>(\d+?) pages :", page )[ 0 ]
				# Le programme ne charge pour l'instant que les 10 premieres pages
				# TODO : Ajouter une option
				if( pageMax > 10 ):
					pageMax = 10
			except :
				pageMax = 10
				logger.debug( "impossible de trouver le nombre max de pages de %s, il est fixé à 10" %( urlChaine ) )
			# Recupere une par une les pages et en extrait les infos
			for i in range( 2, pageMax + 1 ):
				# Charge la page
				page = self.getPage( "%s%d/" %( urlChaine, i ) )
				# Extrait les infos des vidéos
				parser = TF1ProgrammesParser()
				parser.feed(page)
				return		
		else:
			logger.warning( 'chaine "%s" introuvable' %( chaine ) )
				
	def listerFichiers( self, emission ):
		pass

class TF1ProgrammesParser( HTMLParser.HTMLParser ):
	
	## Constructeur
	def __init__( self ):
		HTMLParser.HTMLParser.__init__( self )
		
		self.isDate        = False
		self.isNomEmission = False
		self.isTitre       = False
		
	## Methode appelee lors de l'ouverture d'une balise
	# @param tag   Tag de la balise
	# @param attrs Attributs de la balise
	def handle_starttag( self, tag, attrs ):
		if( tag == "div" and attrs == [ ( 'class', 'date t3 c5' ) ] ):
			self.isDate = True
		elif( tag == "div" and attrs == [ ( 'class', 'prog t4 c5' ) ] ):
			self.isNomEmission = True
		elif( tag == "h3" and attrs == [ ( 'class', 'titre t4' ) ] ):
			self.isTitre = True
			self.titre   = ""
		elif( self.isTitre and tag == "a" and attrs[ 0 ][ 0 ] == "href" ):
			print "Lien page = %s" %( attrs[ 0 ][ 1 ] )
		
	## Methode qui renvoit les donnees d'une balise
	# @param data Donnees de la balise
	def handle_data( self, data ):
		if( self.isDate ):
			print "Date = %s" %( data )
			self.isDate = False
		elif( self.isNomEmission ):
			print "Nome emission = %s" %( data )
			self.isNomEmission = False
		elif( self.isTitre ):
			self.titre += data
		
	## Methode appelee lors de la fermeture d'une balise
	# @param tag Tag de la balise
	def handle_endtag( self, tag ):
		if( self.isTitre and tag == "a" ):
			print "Titre = %s" %( self.titre )
			self.isTitre = False
