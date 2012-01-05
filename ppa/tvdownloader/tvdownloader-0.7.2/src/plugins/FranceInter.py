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

import re
import os
import os.path
#~ import pickle
import xml.sax

from Podcasts import PodcastsHandler

from Fichier import Fichier
from Plugin import Plugin

###########
# Classes #
###########

class FranceInter( Plugin ):
	
	urlListesEmissions = [ [ "Du lundi au vendredi", "http://sites.radiofrance.fr/franceinter/pod/index.php?page=chrono&jd=sem" ],
						   [ "Le samedi", "http://sites.radiofrance.fr/franceinter/pod/index.php?page=chrono&jd=sam" ],
						   [ "Le dimanche", "http://sites.radiofrance.fr/franceinter/pod/index.php?page=chrono&jd=dim" ]
						 ]
	listeEmissions       = {} # { Nom chaine : { Nom emission : URL fichier XML } }
	urlPageDescriptive   = "http://sites.radiofrance.fr/_c/php/popcast.php?chaine=1&cid="
	pageDescriptiveRegEx = re.compile( '<h2>(.+?)</h2>.+?<p class="rssLink">(.+?)</p>' , re.DOTALL ) 
	derniereChaine = ""
	
	def __init__( self ):
		Plugin.__init__( self, "France Inter", "http://sites.radiofrance.fr/franceinter/accueil/", 30 )
		
		if os.path.exists( self.fichierCache ):
			self.listeEmissions = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		
		# On remet a 0 la liste des emissions
		self.listeEmissions.clear()
		
		# Pour chaque page
		for ( nom, urlPage ) in self.urlListesEmissions:
			# On cree la chaine dans la liste des programmes
			self.listeEmissions[ nom ] = {}
			# On recupere la page web
			page = self.API.getPage( urlPage )
			# On extrait les numeros de chacune des pages des podcasts
			listeNumeros = re.findall( '<h6><a href="javascript:popcast\(([0-9]+?), 1\);"', page )
			# On cree la liste de toutes les pages que l'on doit recuperer
			listeURL = []
			for numero in listeNumeros:
				listeURL.append( self.urlPageDescriptive + numero )
			# On recupere toutes ces pages
			listePages = self.API.getPages( listeURL )
			# Pour chaque page = emission
			for pageEmission in listePages.values():
				# On recupere les informations
				infos = re.findall( self.pageDescriptiveRegEx, pageEmission )
				for ( nomEmission, urlFichierXML ) in infos:
					nomEmission = nomEmission.replace( "&raquo;", "" ).title()
					self.listeEmissions[ nom ][ nomEmission ] = urlFichierXML
		
		self.sauvegarderCache( self.listeEmissions )
		self.afficher( u"Liste des émissions sauvegardées" )
		
	def listerChaines( self ):
		for chaine in self.listeEmissions.keys():
			self.ajouterChaine( chaine )
	
	def listerEmissions( self, chaine ):
		if( self.listeEmissions.has_key( chaine ) ):
			self.derniereChaine = chaine
			for emission in self.listeEmissions[ chaine ].keys():
				self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		if( self.listeEmissions.has_key( self.derniereChaine ) ):
			if( self.listeEmissions[ self.derniereChaine ].has_key( emission ) ):
				# On recupere la page web qui liste les fichiers
				pageXML = self.API.getPage( self.listeEmissions[ self.derniereChaine ][ emission ] )
				
				# On extrait les fichiers
				listeFichiers = []
				handler = PodcastsHandler( listeFichiers )
				try:
					xml.sax.parseString( pageXML, handler )
				except:
					return
				
				# On ajoute les fichiers
				for fichier in listeFichiers:
					self.ajouterFichier( emission, fichier )
		