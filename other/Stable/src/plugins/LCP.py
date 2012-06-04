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

class LCP( Plugin ):
	
	pageEmissions  = "http://www.lcp.fr/videos/emissions"
	listeEmissions = {} # { Nom emission, id de l'emission sur le site }
	
	def __init__( self ):
		Plugin.__init__( self, "La Chaine Parlementaire", "http://www.lcp.fr/", 7 )
		
		if( os.path.exists( self.fichierCache ) ):
			self.listeEmissions = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		# RAZ
		self.listeEmissions.clear()
		# Recupere la page principale
		page = BeautifulSoup.BeautifulSoup( self.API.getPage( self.pageEmissions ) )
		try:
			# Extrait le block qui contient les emissions
			emissionsBlock = page.findAll( "div", { "class" : "unit_int" } )
			# Extrait les emissions
			for elmt in emissionsBlock[ 3 : ]:
				try:
					emissionBlock = BeautifulSoup.BeautifulSoup( str( elmt.contents[ 1 ] ) )
					nomEmission = emissionBlock.findAll( "a", { "class" : "emission" } )[ 0 ][ "title" ]
					idEmission  =  emissionBlock.findAll( "input", { "name" : "rubrique" } )[ 0 ][ "value" ]
					self.listeEmissions[ nomEmission ] = idEmission
				except:
					continue
				self.sauvegarderCache( self.listeEmissions )
				self.afficher( u"Liste des émissions sauvegardées" )
		except:
			pass
		
	def listerChaines( self ):
		self.ajouterChaine( self.nom )
	
	def listerEmissions( self, chaine ):
		for emission in self.listeEmissions.keys():
			self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		if( self.listeEmissions.has_key( emission ) ):
			# Recupere la page qui liste les fichiers
			pageFichiers = BeautifulSoup.BeautifulSoup( self.API.getPage( "http://www.lcp.fr/spip.php?page=lcp_page_videos_ajax&parent=%s" %( self.listeEmissions[ emission ] ) ) )
			# Extrait les fichiers
			fichiersData = pageFichiers.findAll( "strong", { "class" : "titre" } )
			for elmt in fichiersData:
				try:
					fichierBlock =  BeautifulSoup.BeautifulSoup( str( elmt.contents[ 1 ] ) )
					nomEmission = fichierBlock.findAll( "a" )[ 0 ].contents[ -1 ].replace( "\n", "" )
					urlImage = "http://www.lcp.fr/%s" %( fichierBlock.findAll( "img" )[ 0 ][ "src" ] )
					urlPage = "http://www.lcp.fr/%s" %( fichierBlock.findAll( "a" )[ 0 ][ "href" ] )
					# Recupere la page contenant le lien vers le fichier
					soup = BeautifulSoup.BeautifulSoup( self.API.getPage( urlPage ) )
					
					#
					# Code k3c
					#
					
					nom = urlPage.split('/')[-1:][0]
					player = soup.find('param', {'name': 'movie'})['value']
					info_video = soup.find('param', attrs={'name' : 'flashvars' })['value']
					host = info_video.split('rtmp://')[1].split('/')[0]
					app = info_video.split('rtmp://')[1].split('/')[1]
					s2 = host+"/"+app+"/"
					playpath = info_video.split(s2)[1].split('/mp4')[0]
					playpath = playpath[:-4]
					cmds = "rtmpdump"+" --resume  --live 0 --host "+host+" --swfVfy "+ player+" --swfAge 0 -v --app "+app+" --playpath "+playpath+" -e -k 1 --flv "+str(nom)+".mp4"
					
					#
					# Fin code k3c
					#
							
					# Ajouter le fichier
					self.ajouterFichier( emission, Fichier( nom = nomEmission, lien = cmds, urlImage = urlImage ) )
				except:
					continue
			
