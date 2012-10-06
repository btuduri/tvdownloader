#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import BeautifulSoup
import dateutil.parser
import logging
logger = logging.getLogger( "TVDownloader" )
import os
import re
import unicodedata
import xml.sax

import tvdcore
from Podcasts import PodcastsHandler

#
# Classe
#

class FranceInter( tvdcore.Plugin ):
	
	listeChaines = { "Emissions"  : "http://www.franceinter.fr/emissions/liste-des-emissions",
					 "Chroniques" : "http://www.franceinter.fr/emissions/liste-des-chroniques"
				   }
	
	def __init__( self ):
		tvdcore.Plugin.__init__( self, "France Inter", "http://www.franceinter.fr", 14 )
		
		self.listeEmissions = {} # { Nom chaine : { Nom emission : URL fichier XML } }
		self.derniereChaine = {}
		
		if( os.path.exists( self.fichierCache ) ):
			self.listeEmissions = self.chargerCache()
		
	def rafraichir( self ):
		# RAZ de la liste des emissions
		self.listeEmissions.clear()
		
		# Recupere le XML de description de toutes les emissions
		for ( chaine, urlChaine ) in self.listeChaines.items():
			self.listeEmissions[ chaine ] = {}
			pageHtml     = self.getPage( urlChaine )
			soupStrainer = BeautifulSoup.SoupStrainer( "a", { "class" : "visuel" } )
			pageSoup     = BeautifulSoup.BeautifulSoup( pageHtml, parseOnlyThese = soupStrainer )
			# Liste des pages des emissions
			listePagesUrl = map( lambda x : "%s%s" %( "http://www.franceinter.fr" , x[ "href" ] ), pageSoup.contents )
			# Recupere toutes les pages
			listePagesData = self.getPages( listePagesUrl )
			for emission in pageSoup.contents:
				try:
					nomEmission = unicodedata.normalize( 'NFKD', emission[ "title" ] ).encode( 'ASCII', 'ignore' )
					urlPageEmission = "%s%s" %( "http://www.franceinter.fr" , emission[ "href" ] )
					# Extrait le lien XML de la page de l'emission
					urlXml = re.findall( "http://radiofrance-podcast.net/podcast09/rss_\d+?.xml", listePagesData[ urlPageEmission ] )[ 0 ]
					# Ajoute l'emission a la liste
					self.listeEmissions[ chaine][ nomEmission ] = urlXml
				except:
					continue
		
		# Sauvegarde la liste dans le cache
		self.sauvegarderCache( self.listeEmissions )
		
	def listerChaines( self ):
		map( lambda x : self.ajouterChaine( ( x, None ) ), self.listeEmissions.keys() )
	
	def listerEmissions( self, chaine ):
		if( self.listeEmissions.has_key( chaine ) ):
			self.derniereChaine = self.listeEmissions[ chaine ]
			map( lambda x : self.ajouterEmission( chaine, x ), self.derniereChaine.keys() )
				
	def listerFichiers( self, emission ):
		if( self.derniereChaine.has_key( emission ) ):
			urlXmlEmission = self.derniereChaine[ emission ]
			xmlEmission    = self.getPage( urlXmlEmission )
			# Extrait les fichiers
			listeFichiers = []
			handler = PodcastsHandler( listeFichiers )
			try:
				xml.sax.parseString( xmlEmission, handler )
			except:
				logger.error( "Impossible de parser le fichier XML %s" %( urlXmlEmission ) )
				return
			# Ajoute les fichiers
			map( lambda x : self.ajouterFichier( emission, x ), listeFichiers )
				
