#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import datetime
import os.path
import time

from DownloaderFactory import DownloaderFactory

import util as lib
import util.html
import util.fichierDossier

import logging
logger = logging.getLogger( "TVDownloader" )

##########
# Classe #
##########

## Classe qui contient les informations d'un fichier
class Fichier(object):
	DOWNLOADER_FACTORY = DownloaderFactory()
	
	## Contructeur
	# @param nom              Le nom du fichier (tel qu'affiché à l'utilisateur)
	# @param date             La date du fichier
	# @param lien             L'url où se trouve le fichier
	# @param nomFichierSortie Nom du fichier de sortie
	# @param urlImage         URL de l'image a afficher
	# @param descriptif       Texte descriptif a afficher
	def __init__( self, nom, date = datetime.datetime.now(), lien = "", nomFichierSortie = "", urlImage = "", descriptif = "" ):
		self.nom              = util.html.supprimeBalisesHTML( nom )
		self.date             = date
		self.lien             = lien
		if( nomFichierSortie == "" ):
			self.nomFichierSortie = util.fichierDossier.chaineToNomFichier( os.path.basename( self.lien ) )
		else:
			self.nomFichierSortie = util.fichierDossier.chaineToNomFichier( nomFichierSortie )
		self.urlImage         = urlImage
		self.descriptif       = util.html.supprimeBalisesHTML( descriptif )
	
	## Surcharge de la methode ==
	# @param autre L'autre Fichier a comparer
	# @return      Si les 2 Fichiers sont egaux	
	def __eq__( self, autre ):
		if not isinstance( autre, Fichier ):
			return False
		else:
			return ( self.nom == autre.nom and self.date == autre.date and self.lien == autre.lien )	

	## Surcharge de la methode !=
	# @param autre L'autre Fichier a comparer
	# @return      Si les 2 Fichiers sont differents	
	def __ne__( self, autre ):
		return not self.__eq__( autre )

	## Surcharge de la methode d'affichage d'un fichier
	def __str__( self ):
		return "--> Fichier :\nNom : %s\nLien : %s" %( self.nom, self.lien )
	
	def getDownloader(self):
		return Fichier.DOWNLOADER_FACTORY.create(self.lien)
