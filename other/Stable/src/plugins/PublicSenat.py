#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import BeautifulSoup
import os
import unicodedata 

from Fichier import Fichier
from Plugin import Plugin

#
# Classe
#

class PublicSenat( Plugin ):
	
	pageEmissions  = "http://www.publicsenat.fr/cms/video-a-la-demande/vod.html"
	listeEmissions = {} # { Nom emission, id de l'emission sur le site }
	
	def __init__( self ):
		Plugin.__init__( self, "Public Senat", "http://www.publicsenat.fr", 7 )
		
		if( os.path.exists( self.fichierCache ) ):
			self.listeEmissions = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		# RAZ
		self.listeEmissions.clear()
		# Recupere la page principale
		page         = self.API.getPage( self.pageEmissions )
		soupStrainer = BeautifulSoup.SoupStrainer( "option", { "value" : True } )
		pageSoup     = BeautifulSoup.BeautifulSoup( page, parseOnlyThese = soupStrainer )
		# Extrait les emissions
		for emissionBlock in pageSoup.contents[ 1 : ]:
			try:
				nomEmission = unicodedata.normalize( 'NFKD', emissionBlock.string.title() ).encode( 'ASCII', 'ignore' )
				idEmission  = emissionBlock[ "value" ]
				self.listeEmissions[ nomEmission ] = idEmission
			except:
				continue
		self.sauvegarderCache( self.listeEmissions )
		self.afficher( u"Liste des émissions sauvegardées" )
		
	def listerChaines( self ):
		self.ajouterChaine( self.nom )
	
	def listerEmissions( self, chaine ):
		for emission in self.listeEmissions.keys():
			self.ajouterEmission( chaine, emission )

	def listerFichiers( self, emission ):
		
		#
		# TODO : parcourir toutes les pages
		#
		
		if( self.listeEmissions.has_key( emission ) ):
			# Recupere la page qui liste les fichiers
			pageFichiers     = self.API.getPage( "http://www.publicsenat.fr/zp/templates/emission/JX_video.php", { "idP" : self.listeEmissions[ emission ], "page" : 1 } )
			pageFichiersSoup = BeautifulSoup.BeautifulSoup( pageFichiers )
			# Fichiers
			fichiersBlock = pageFichiersSoup.findAll( "div", { "class" : "box-bg" } )
			# Extrait d'abord tous les liens vers les pages qui contienent les fichiers
			listeUrls = map( lambda x : "http://www.publicsenat.fr%s" %( x.div.a[ "href" ] ), fichiersBlock )
			# Recupere toutes les pages
			dicoPageFichier = self.API.getPages( listeUrls )
			# Extrait les fichiers
			for fichier in fichiersBlock:
				try:
					urlPageFichier = "http://www.publicsenat.fr%s" %( fichier.div.a[ "href" ] )
					urlImage       = "http://www.publicsenat.fr%s" %( fichier.div.a.img[ "src" ] )
					descriptif     = fichier.h3.a.string
					pageFichier    = dicoPageFichier[ urlPageFichier ]
					if( pageFichier == "" ):
						continue
					# Extrait le lien vers la video
					fichierSoup = BeautifulSoup.BeautifulSoup( pageFichier )
					lienVideo   = fichierSoup.find( "input", { "id" : "flvEmissionSelect" } )[ "value" ]
					# Ajouter le fichier
					self.ajouterFichier( emission, Fichier( nom = descriptif, lien = lienVideo, urlImage = urlImage, descriptif = descriptif ) )
				except:
					continue
