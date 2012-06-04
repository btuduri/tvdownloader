#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import BeautifulSoup
import os

from Fichier import Fichier
from Plugin import Plugin

#
# Classe
#

class PublicSenat( Plugin ):
	
	pagePrincipale = "http://www.publicsenat.fr"
	listeEmissions = {} # { Nom emission, URL page HTML }
	
	def __init__( self ):
		Plugin.__init__( self, "Public Senat", "http://www.publicsenat.fr", 7 )
		
		if( os.path.exists( self.fichierCache ) ):
			self.listeEmissions = self.chargerCache()
	
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		# RAZ
		self.listeEmissions.clear()
		# Recupere la page principale
		page = BeautifulSoup.BeautifulSoup( self.API.getPage( self.pagePrincipale ) )
		try:
			# Extrait le block qui contient les emissions
			emissionsBlock = BeautifulSoup.BeautifulSoup( str( page.findAll( "ul", { "class" : "emissions-level2" } )[ 0 ].contents[ 1 ] ) )
			# Extrait les emissions
			emissions = emissionsBlock.findAll( "div", { "class" : "field-item" } )
			# Creer le dictionnaire
			self.listeEmissions = dict( zip( map( lambda x : x.contents[ 0 ][ "title" ], emissions ), map( lambda x : x.contents[ 0 ][ "href" ], emissions ) ) )
		
			self.sauvegarderCache( self.listeEmissions )
			self.afficher( u"Liste des émissions sauvegardées" )
		except:
			return
		
	def listerChaines( self ):
		pass
		self.ajouterChaine( self.nom )
	
	def listerEmissions( self, chaine ):
		for emission in self.listeEmissions.keys():
			self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		
		#
		# TODO : parcourir toutes les pages, recuperer la date et la description
		#
		
		# Recupere la page qui liste les fichiers disponibles
		pageFichiers = BeautifulSoup.BeautifulSoup( self.API.getPage( "http://www.publicsenat.fr/zp/templates/emission/JX_video.php", { "idP" : 108, "page" : 1 } ) )
		# Recupere les fichiers disponibles
		emissionsData = pageFichiers.findAll( "h3" )
		for emissionData in emissionsData:
			try:
				nom     = emissionData.contents[ 0 ].contents[ 0 ]
				urlPage = "http://www.publicsenat.fr%s" %( emissionData.contents[ 0 ][ "href" ] )
				# Recupere des infos sur la page du fichier
				page = BeautifulSoup.BeautifulSoup( self.API.getPage( urlPage ) )
				# Extrait les donnees
				urlPhoto  = "http://www.publicsenat.fr%s" %( page.findAll( "input", { "id" : "imgEmissionSelect" } )[ 0 ][ "value" ] )
				lienVideo = page.findAll( "input", { "id" : "flvEmissionSelect" } )[ 0 ][ "value" ]
				# Ajouter le fichier
				self.ajouterFichier( emission, Fichier( nom = nom, lien = lienVideo, urlImage = urlPhoto ) )
			except:
				continue
