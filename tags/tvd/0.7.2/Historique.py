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

import os
import pickle

from Fichier import Fichier

##########
# Classe #
##########

## Classe qui gere l'historique des telechargements
class Historique( object ):
	
	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( Historique, self ).__new__( self )
		return self.instance
	
	# Historique : les fichiers sont d'abord hashes selon leur date pour diminuer le temps de recherche
	# Ainsi, l'historique est de la forme { date1, [ Fichiers a date1 ], date2, [ Fichiers a date2 ], ... }
	
	## Constructeur
	def __init__( self ):
		self.home = os.path.expanduser( "~" )
		self.fichierHistorique = self.home + "/.tvdownloader/logs/historique"
		self.chargerHistorique()
	
	## Methode qui charge l'historique existant	
	def chargerHistorique( self ):
		if os.path.exists( self.fichierHistorique ): # Si le fichier existe, on le charge
			fichier = open( self.fichierHistorique, "r" )
			self.historique = pickle.load( fichier )
			fichier.close()
		else: # Sinon, on creee un historique vide
			self.historique = {}

	## Methode qui ajoute un fichier a l'historique
	# @param nouveauFichier Fichier a ajouter a l'historique
	def ajouterHistorique( self, nouveauFichier ):
		if( isinstance( nouveauFichier, Fichier ) ):
			date = getattr( nouveauFichier, "date" )
			if( self.historique.has_key( date ) ):
				self.historique[ date ].append( nouveauFichier )
			else:
				self.historique[ date ] = [ nouveauFichier ]

	## Methode qui sauvegarde l'historique
	def sauverHistorique( self ):
		# On enregistre l'historique
		fichier = open( self.fichierHistorique, "w" )
		pickle.dump( self.historique, fichier )
		fichier.close()
		
	## Methode qui verifie si un fichier se trouve dans l'historique
	# @param fichier Fichier a chercher dans l'historique
	# @return        Si le fichier est present ou non dans l'historique
	def comparerHistorique( self, fichier ):
		if( isinstance( fichier, Fichier ) ):
			date = getattr( fichier, "date" )
			if( self.historique.has_key( date ) ):
				return fichier in self.historique[ date ]
			else:
				return False
		else:
			return False
