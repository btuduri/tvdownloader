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
		page         = self.API.getPage( self.pageEmissions )
		soupStrainer = BeautifulSoup.SoupStrainer( "div", { "class" : "unit size1of5" } )
		pageSoup     = BeautifulSoup.BeautifulSoup( page, parseOnlyThese = soupStrainer )
		# Extrait les emissions
		for emissionBlock in pageSoup.contents:
			try:
				nomEmission = unicodedata.normalize( 'NFKD', emissionBlock.div.p.a[ "title" ] ).encode( 'ASCII', 'ignore' )
				idEmission  = emissionBlock.div.p.input[ "value" ]
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
		if( self.listeEmissions.has_key( emission ) ):
			# Recupere la page qui liste les fichiers
			pageFichiers     = self.API.getPage( "http://www.lcp.fr/spip.php?page=lcp_page_videos_ajax&parent=%s" %( self.listeEmissions[ emission ] ) )
			soupStrainer     = BeautifulSoup.SoupStrainer( "div", { "class" : "video-item" } )
			pageFichiersSoup = BeautifulSoup.BeautifulSoup( pageFichiers, parseOnlyThese = soupStrainer )
			# Extrait d'abord tous les liens vers les pages qui contienent les fichiers
			listeUrls = map( lambda x : "http://www.lcp.fr/%s" %( x[ "href" ] ), pageFichiersSoup.findAll( "a" ) )
			# Recupere toutes les pages
			dicoPageFichier = self.API.getPages( listeUrls )
			# Extrait les fichiers
			for fichiersBlock in pageFichiersSoup.contents:
				try:
					urlPageFichier = "http://www.lcp.fr/%s" %( fichiersBlock.strong.a[ "href" ] )
					urlImage       = "http://www.lcp.fr/%s" %( fichiersBlock.strong.img[ "src" ] )
					descriptif     = fichiersBlock.p.contents[ 0 ].replace( "\n", "" ).replace( "\t", "" )
					pageFichier    = dicoPageFichier[ urlPageFichier ]
					if( pageFichier == "" ):
						continue
					soup = BeautifulSoup.BeautifulSoup( pageFichier )
					
					#
					# Code k3c
					#
					
					nom = urlPageFichier.split('/')[-1:][0]
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
					self.ajouterFichier( emission, Fichier( nom = "%s - %s" %( emission, descriptif ), lien = cmds, nomFichierSortie = "%s %s.mp4" %( emission, descriptif ), urlImage = urlImage, descriptif = descriptif ) )
				except:
					continue
