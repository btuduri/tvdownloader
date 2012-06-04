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
	# { Nom emission, id de l'emission sur le site }
	listeEmissions = { r"A l'heure du choix"       : 270,
					   r"A nous le Sénat"          : 281,
					   r"Attention grands travaux" : 271
					 }
	
	def __init__( self ):
		Plugin.__init__( self, "Public Senat", "http://www.publicsenat.fr", 7 )
	
	def rafraichir( self ):
		pass
		
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
		
		if( self.listeEmissions.has_key( emission ) ):
			# Recupere la page qui liste les fichiers disponibles
			pageFichiers = BeautifulSoup.BeautifulSoup( self.API.getPage( "http://www.publicsenat.fr/zp/templates/emission/JX_video.php", { "idP" : self.listeEmissions[ emission ], "page" : 1 } ) )
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
