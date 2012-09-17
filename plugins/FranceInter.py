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
	
	ulrListeEmission     = "http://www.franceinter.fr/podcasts/liste-des-emissions"
	listeEmissions       = {} # { Nom emission, URL fichier XML }
	pageRegEx            = re.compile( 'class="visuel" title="([^"]*?)".+?href="(http://radiofrance-podcast.net/podcast09/.+?.xml)', re.DOTALL )
	
	def __init__( self ):
		Plugin.__init__( self, "France Inter", "http://www.franceinter.fr/podcasts", 30 )
		
		if os.path.exists( self.fichierCache ):
			self.listeEmissions = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		
		# On remet a 0 la liste des emissions
		self.listeEmissions.clear()
		# On recupere la page web
		page = self.API.getPage( self.ulrListeEmission )
		# Extraction des emissions
		self.listeEmissions = dict( re.findall( self.pageRegEx, page ) )
		
		self.sauvegarderCache( self.listeEmissions )
		self.afficher( u"Liste des émissions sauvegardées" )
		
	def listerChaines( self ):
		self.ajouterChaine( self.nom )
	
	def listerEmissions( self, chaine ):
		for emission in self.listeEmissions.keys():
			self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		
		if( self.listeEmissions.has_key( emission ) ):
			# On recupere la page web qui liste les fichiers
			pageXML = self.API.getPage( self.listeEmissions[ emission ] )
			
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
		
