#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier LICENSE #
#########################################

#~ Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
#~ Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
#~ Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import re
import os
import os.path
import pickle
import urllib

from Fichier import Fichier
from Plugin import Plugin

##########
# Classe #
##########

class RTL( Plugin ):
	
	listeEmissionsRegEx = re.compile( "<h4>(.+?)</h4>.*?podcast.rtl.fr/(.+?).xml", re.DOTALL )
	
	def __init__( self):
		Plugin.__init__( self, "RTL", "http://www.rtl.fr")
		
		self.listeChaines = {} # Clef = nom chaine ; Valeur = { nom emission : lien fichier XML qui contient la liste des emissions }
		self.derniereChaine = ""
		
		if os.path.exists( self.fichierCache ):
			self.listeChaines = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des chaines et des émissions..." )
		# On remet a zero la liste des chaines
		self.listeChaines.clear()
		# On recupere la page qui contient les emissions
		page = self.API.getPage( "http://www.rtl.fr/podcast.html" )
		# On decoupe la page selon le nom des chaines
		resultats = re.split( "<h3>([^<]+)</h3>", page )[ 1 : ]
		for ( chaine, texteChaine ) in ( zip( resultats[ 0::2 ], resultats[ 1::2 ] ) ):
			# On ajoute la chaine
			self.listeChaines[ chaine ] = {}
			# On extrait le nom des emissions et les liens des fichiers XML correspondants
			resultatsEmissions = re.findall( self.listeEmissionsRegEx, texteChaine )
			for res in resultatsEmissions:
				nom  = res[ 0 ]
				lien = "http://podcast.rtl.fr/" + res[ 1 ] + ".xml"
				self.listeChaines[ chaine ][ nom ] = lien
			
		self.sauvegarderCache( self.listeChaines )
		self.afficher( str( len( self.listeChaines ) ) + " chaines concervées." )
	
	def listerChaines( self ):
		for chaine in self.listeChaines.keys():
			self.ajouterChaine( chaine )

	def listerEmissions( self, chaine ):
		if( self.listeChaines.has_key( chaine ) ):
			self.derniereChaine = chaine
			for emission in self.listeChaines[ chaine ].keys():
				self.ajouterEmission( chaine, emission )
	
	def listerFichiers( self, emission ):
		if( self.listeChaines.has_key( self.derniereChaine ) ):
			if( self.listeChaines[ self.derniereChaine ].has_key( emission ) ):
				# On recupere le lien de la page de l'emission
				lienPage = self.listeChaines[ self.derniereChaine ][ emission ]
				# On recupere la page de l'emission
				page = self.API.getPage( lienPage )
				# On extrait les emissions
				resultats = re.findall( "media_url=([^\"]*)\"", page )
				for res in resultats:
					lien = urllib.unquote( res )
					listeDates = re.findall( "(\d{4})/(\d{4})", lien )
					if( listeDates == [] ): # Si on n'a pas pu extraire une date
						date = "Inconnue"
					else: # Si on a extrait une date
						date = listeDates[ 0 ][ 1 ][ 2:4 ] + "-" + listeDates[ 0 ][ 1 ][ 0:2 ] + "-" + listeDates[ 0 ][ 0 ]
					self.ajouterFichier( emission, Fichier( emission + " (" + date + ")", date, lien ) )
