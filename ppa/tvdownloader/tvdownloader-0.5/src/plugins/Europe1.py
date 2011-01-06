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

class Europe1( Plugin ):
	
	listeEmissionsRegEx = re.compile( "<td class=\"programme\">.+?<a href=\".+?>(.+?)</a>.+?podcasts/(.+?)\.xml", re.DOTALL )
	
	def __init__( self):
		Plugin.__init__(self, "Europe1", "http://www.europe1.fr")
		# On instancie la classe qui permet de charger les pages web
		
		self.listeEmissions = {} # Clef = nom emission ; Valeur = lien fichier XML qui contient la liste des emissions
		
		if os.path.exists( self.fichierCache ):
			self.listeEmissions = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		
		# On remet a zero la liste des emissions
		self.listeEmissions.clear()
		# On recupere la page qui contient les emissions
		for page in [ "http://www.europe1.fr/Radio/Podcasts/Semaine/", "http://www.europe1.fr/Radio/Podcasts/Samedi/", "http://www.europe1.fr/Radio/Podcasts/Dimanche/" ]:
			pageEmissions = self.API.getPage( page )
			# On extrait le nom des emissions et les liens des fichiers XML correspondants
			resultats = re.findall( self.listeEmissionsRegEx, pageEmissions )
			for res in resultats:
				nom  = res[ 0 ]
				lien = "http://www.europe1.fr/podcasts/" + res[ 1 ] + ".xml"
				self.listeEmissions[ nom ] = lien
		
		self.sauvegarderCache( self.listeEmissions )
		self.afficher( str( len( self.listeEmissions ) ) + " émissions concervées." )
	
	def listerChaines( self ):
		self.ajouterChaine(self.nom)

	def listerEmissions( self, chaine ):
		# On renvoit le resulat
		liste = self.listeEmissions.keys()
		liste.sort()
		for emission in  liste:
			self.ajouterEmission(chaine, emission)
	
	def listerFichiers( self, emission ):
		if( emission != "" ):
			if( emission in self.listeEmissions ):
				# On recupere le lien de la page de l'emission
				lienPage = self.listeEmissions[ emission ]
				# On recupere la page de l'emission
				page = self.API.getPage( lienPage )
				# On extrait les emissions
				resultats = re.findall( "media_url=([^\"]*)\"", page )
				for res in resultats:
					lien = urllib.unquote( res )
					listeDates = re.findall( "\d{2}-\d{2}-\d{4}", lien )
					if( listeDates == [] ): # Si on n'a pas pu extraire une date
						date = "Inconnue"
					else: # Si on a extrait une date
						date = listeDates[ 0 ]
					self.ajouterFichier(emission, Fichier( emission + " (" + date + ")", date, lien ) )
