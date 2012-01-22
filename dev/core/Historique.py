#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import cPickle as pickle
import os

import Constantes
from Fichier import Fichier

import logging
logger = logging.getLogger( __name__ )

import threading
from tvdcore.util import SynchronizedMethod

##########
# Classe #
##########

## Classe qui gere l'historique des telechargements
class Historique( object ):
	
	# Instance de la classe (singleton)
	__instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__(typ, *args, **kwargs):
		if Historique.__instance == None:
			return super(Historique, typ).__new__(typ, *args, **kwargs)
		else:
			return Historique.__instance
	
	# Historique : les fichiers sont d'abord hashes selon leur date pour diminuer le temps de recherche
	# Ainsi, l'historique est de la forme { date1, [ Fichiers a date1 ], date2, [ Fichiers a date2 ], ... }
	
	## Constructeur
	def __init__( self ):
		if Historique.__instance != None:
			return
		Historique.__instance = self
		
		self.RLOCK = threading.RLock()
		
		self.chargerHistorique()
	
	## Destructeur
	def __del__( self ):
		self.sauverHistorique()
	
	## Charge l'historique existant	
	@SynchronizedMethod
	def chargerHistorique( self ):
		if os.path.exists( Constantes.FICHIER_HISTORIQUE_TVD ): # Charge le fichier s'il existe
			logger.info( "chargerHistorique : chargement de l'historique" )
			with open( Constantes.FICHIER_HISTORIQUE_TVD, "r" ) as fichier:
				self.historique = pickle.load( fichier )
		else: # Sinon, historique vide
			logger.info( "chargerHistorique : fichier historique non trouve ; creation" )
			self.historique = {}

	## Ajoute un fichier a l'historique
	# @param nouveauFichier Fichier a ajouter a l'historique
	@SynchronizedMethod
	def ajouterHistorique( self, nouveauFichier ):
		if( isinstance( nouveauFichier, Fichier ) ):
			date = nouveauFichier.date
			if( self.historique.has_key( date ) ):
				self.historique[ date ].append( nouveauFichier )
			else:
				self.historique[ date ] = [ nouveauFichier ]

	## Sauvegarde l'historique
	@SynchronizedMethod
	def sauverHistorique( self ):
		# On enregistre l'historique
		with open( Constantes.FICHIER_HISTORIQUE_TVD, "w" ) as fichier:
			logger.info( "sauverHistorique : sauvegarde de l'historique" )
			pickle.dump( self.historique, fichier )
		
	## Verifie si un fichier se trouve dans l'historique
	# @param fichier Fichier a chercher dans l'historique
	# @return        Si le fichier est present ou non dans l'historique
	@SynchronizedMethod
	def comparerHistorique( self, fichier ):
		if( isinstance( fichier, Fichier ) ):
			date = fichier.date
			if( self.historique.has_key( date ) ):
				return fichier in self.historique[ date ]
			else:
				return False
		else:
			return False
			
	## Nettoie l'historique
	# Supprime les entrees les plus vieilles de l'historique
	@SynchronizedMethod
	def nettoieHistorique( self ):
		logger.info( "nettoieHistorique : suppression des vieilles reference de l'historique" )
