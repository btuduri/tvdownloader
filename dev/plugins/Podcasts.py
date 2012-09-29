#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import collections
import dateutil.parser
import os
import xml.sax

import tvdcore

#
# Classes
#

Podcast = collections.namedtuple( "Podcast", [ "nom", "urlImage" ] )

class Podcasts( tvdcore.Plugin ):
	"""
	Classe generique pour charger des podcasts
	Pour ajouter le support d'un podcast, il suffit de l'ajouter a la liste ci dessous
	"""
	
	listePodcasts = { Podcast( nom = "Allo Cine", urlImage = "http://images.allocine.fr/commons/logos/rss/allocine.png" )                                  : { "Bandes Annonces" : "http://rss.allocine.fr/bandesannonces/ipod" },
					  Podcast( nom = "Casse Croute", urlImage = "http://www.casse-croute.fr/rw_common/themes/cassecroute/images/stripe/header_bg850.jpg" ) : { "Recettes" : "http://www.casse-croute.fr/media/cassecroute.xml" },
					  Podcast( nom = "Gameone", urlImage = "http://gameone-net.mtvnimages.com/Images/logo-g1-programmes-scenic-updated.jpg" )              : { "JT E-NEWS" : "http://podcast13.streamakaci.com/xml/GAMEONE2.xml",
																																							   "JT REPORTAGE & DOSSIERS" : "http://podcast13.streamakaci.com/xml/GAMEONE6.xml",
																																							   "PLAY HIT" : "http://podcast13.streamakaci.com/xml/GAMEONE9.xml",
																																							   "Funky Web" : "http://podcast13.streamakaci.com/xml/GAMEONE26.xml",
																																							   "JT LE TEST" : "http://podcast13.streamakaci.com/xml/GAMEONE3.xml"
																																							 },
					  Podcast( nom = "i>TELE", urlImage = "http://podcast123.streamakaci.com/iTELE/images/iTele_Triangle_rouge.gif" )                      : { "Le Journal" : "http://podcast12.streamakaci.com/iTELE/iTELElejournal.xml" }
					}
	
	def __init__( self ):
		tvdcore.Plugin.__init__( self, nom = "Podcasts", url = "", frequence = 0, logo = None )
		
		self.derniereChaine = Podcast( nom = None, urlImage = None )
		self.listeFichiers  = []

	def rafraichir( self ):
		pass
	
	def listerChaines( self ):
		listeChaines = self.listePodcasts.keys()
		listeChaines.sort( key = lambda x : x.nom )
		map( self.ajouterChaine, listeChaines )
	
	def listerEmissions( self, chaine ):
		chaineTupleList = [ x for x in self.listePodcasts if x.nom == chaine ]
		if( len( chaineTupleList ) == 1 ):
			self.derniereChaine = chaineTupleList[ 0 ] 
			listeEmissions = self.listePodcasts[ self.derniereChaine ].keys()
			listeEmissions.sort()
			map( lambda x : self.ajouterEmission( chaine, x ), listeEmissions )
	
	def listerFichiers( self, emission ):
		if( self.listePodcasts.has_key( self.derniereChaine ) ):
			listeEmission = self.listePodcasts[ self.derniereChaine ]
			if( listeEmission.has_key( emission ) ):
				# RAZ de la liste des fichiers
				del self.listeFichiers[ : ]
				# Recupere la page de l'emission
				page = self.getPage( listeEmission[ emission ] )
				# Handler
				handler = PodcastsHandler( self.listeFichiers )
				# Parse le fichier xml
				xml.sax.parseString( page, handler )
				# Ajoute les fichiers
				map( lambda x : self.ajouterFichier( emission, x ), self.listeFichiers )

class PodcastsHandler( xml.sax.handler.ContentHandler ):
	"""
	Classe pour parser les fichiers XML de description des podcasts
	Ces fichiers sont generiques et fonctionnent pour un grand nombre de sites
	"""
	
	def __init__( self, listeFichiers ):
		# Liste des fichiers
		self.listeFichiers   = listeFichiers
		# Url de l'image globale
		self.urlImageGlobale = ""
		# Initialisation des variables a Faux
		self.isItem          = False
		self.isTitle         = False
		self.isDescription   = False
		self.isPubDate       = False
		self.isGuid          = False

	def startElement( self, name, attrs ):
		if( name == "item" ):
			self.isItem          = True
			self.titre           = ""
			self.date            = ""
			self.urlFichier      = ""
			self.urlImage        = ""
			self.description     = ""
		elif( name == "title" and self.isItem ):
			self.isTitle = True
		elif( name == "description" and self.isItem ):
			self.isDescription = True
		elif( name == "pubDate" and self.isItem ):
			self.isPubDate = True
		elif( name == "media:thumbnail" and self.isItem ):
			self.urlImage = attrs.get( "url", "" )
		elif( name == "media:content" and self.isItem ):
			self.urlFichier = attrs.get( "url", "" )
		elif( name == "guid" and self.isItem ):
			self.isGuid = True
		elif( name == "itunes:image" and not self.isItem ):
			self.urlImageGlobale = attrs.get( "href", "" )	
		
	def characters( self, data ):
		if( self.isTitle ):
			self.titre += data
		elif( self.isDescription ):
			if( data.find( "<" ) == -1 ):
				self.description  += data
			else:
				self.isDescription = False
		elif( self.isPubDate ):
			self.date      = data
			self.isPubDate = False
		elif( self.isGuid ):
			self.urlFichier = data
			self.isGuid     = False		

	def endElement( self, name ):
		if( name == "item" ):
			# Extrait l'extension du fichier
			basename, extension = os.path.splitext( self.urlFichier )
			# Convertit la date
			try:
				self.dateOk = dateutil.parser.parse( self.date )
			except:
				self.dateOk = self.date
			# Si le fichier n'a pas d'image, utilise l'image globale
			if( self.urlImage == "" ):
				self.urlImage = self.urlImageGlobale
			# Ajoute le fichier
			self.listeFichiers.append( tvdcore.Fichier ( self.titre, self.dateOk, self.urlFichier, self.titre + extension, self.urlImage, self.description ) )
			self.isTitle = False
		elif( name == "description" ):
			self.isDescription = False
		elif( name == "title" ):
			self.isTitle = False
