#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import datetime
import os.path
import re
import xml.sax

import tvdcore

import logging
logger = logging.getLogger( "TVDownloader" )

class CanalPlus( tvdcore.Plugin ):
	
	urlFichierXMLListeProgrammes = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/initPlayer/"
	regexThematique = re.compile("<THEMATIQUE.*?<NOM>(.*?)</NOM>.*?<SELECTIONS>(.*?)</SELECTIONS>.*?</THEMATIQUE", re.DOTALL)
	regexSelection = re.compile("<ID>([0-9]+)</ID>.*?<NOM>([^<]+)</NOM>", re.DOTALL)
	
	urlFichierXMLEmissions       = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getMEAs/"
	regexMea = re.compile("<ID>(.+?)</ID>")
	urlFichierXMLFichiers        = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getVideos/"
	
	
	def __init__( self ):
		tvdcore.Plugin.__init__( self, "Canal+", "http://www.canalplus.fr/", 7, "CanalPlus.jpg" )
		
		# Charge le cache
		cache = self.chargerCache() # { Nom chaine : { Nom emission : ID emission } }
		if cache != None:
			listeChaines,self.nomEmissionToIdEmission = cache
			for chaine,emissions in listeChaines:
				self.ajouterChaine(chaine)
				for emission in emissions:
					self.ajouterEmission(chaine, emission)
			for emission,idEmission in self.nomEmissionToIdEmission:
				self.ajouterEmission(chaine, emission)
		else:
			self.nomEmissionToIdEmission = {}
	
	def rafraichir( self ):
		data = self.getPage(CanalPlus.urlFichierXMLListeProgrammes)
		
		thematiques = re.findall(CanalPlus.regexThematique, data)
		if thematiques == None:
			logger.warning( "Aucune thématique trouvée." )
			return
		listeChaines = {}
		for thematique in thematiques:
			selections = re.findall(CanalPlus.regexSelection, thematique[1])
			chaine = thematique[0].title()
			listeChaines[chaine] = []
			self.ajouterChaine(chaine)
			if selections == None:
				logger.warning( "Aucune sélection trouvée." )
				continue
			for selection in selections:
				emission = selection[1].title()
				listeChaines[chaine]+=emission
				self.nomEmissionToIdEmission[emission] = selection[0]
				self.ajouterEmission(chaine, emission)
		self.sauvegarderCache((listeChaines,self.nomEmissionToIdEmission))
	
	def listerChaines( self ):
		pass
	
	def listerEmissions( self, chaine ):
		pass
				
	def listerFichiers( self, emission ):
		if emission in self.nomEmissionToIdEmission:
			data = self.getPage(self.urlFichierXMLEmissions+self.nomEmissionToIdEmission[emission])
			ids = re.findall(self.regexMea, data)
			
			urls = []
			for idMea in ids:
				urls.append(self.urlFichierXMLFichiers+idMea )
			# Recupere les pages correspondantes
			pages = self.getPages( urls )
			
			for url in urls:
				infosFichier = []
				handler = CanalPlusListeFichierHandler(infosFichier)
				try:
					xml.sax.parseString( pages[url], handler )
				except:
					logger.error( "impossible de parser le fichier XML %s" %( url ) )
					continue
				nom, date, lienLD, lienMD, lienHD, urlImage, descriptif = infosFichier
				# Transforme la date en type datetime.date
				try:
					dateDecoupee  = map( int, date.split( "/" ) )
					dateBonFormat = datetime.date( dateDecoupee[ 2 ], dateDecoupee[ 1 ], dateDecoupee[ 0 ] )
				except:
					dateBonFormat = datetime.date.today()
					logger.error( "impossible de transformer la date" )
				if( lienHD != "" and lienHD[ : 4 ] == "rtmp" ):
					basename, extension = os.path.splitext( lienHD )
					self.ajouterFichier( emission, tvdcore.Fichier( "[HD]" + nom, dateBonFormat, lienHD, nom + extension, urlImage, descriptif ) )	
				if( lienMD != "" and lienMD[ : 4 ] == "rtmp" ):	
					basename, extension = os.path.splitext( lienMD )
					self.ajouterFichier( emission, tvdcore.Fichier( "[MD]" + nom, dateBonFormat, lienMD, nom + extension, urlImage, descriptif ) )	
				if( lienLD != "" and lienLD[ : 4 ] == "rtmp" ):	
					basename, extension = os.path.splitext( lienLD )
					self.ajouterFichier( emission, tvdcore.Fichier( "[LD]" + nom, dateBonFormat, lienLD, nom + extension, urlImage, descriptif ) )
		else:
			logger.warning( 'emission "%s" introuvable' %( emission ) )


## Classe qui permet de lire le fichier XML d'un fichier de Canal
class CanalPlusListeFichierHandler( xml.sax.handler.ContentHandler ):

	# Constructeur
	# @param infosFichier Infos du fichier que le parser va remplir
	def __init__( self, infosFichier ):
		# Liste des programmes
		self.infosFichier = infosFichier
		
		# Il n'a pas forcement les 3 liens
		self.lienLD = ""
		self.lienMD = ""
		self.lienHD = ""
		
		# Initialisation des variables a Faux
		self.isTitre      = False
		self.isDate       = False
		self.isLienLD     = False
		self.isLienMD     = False
		self.isLienHD     = False
		self.isLienImage  = False
		self.isDescriptif = False

	## Methode appelee lors de l'ouverture d'une balise
	# @param name  Nom de la balise
	# @param attrs Attributs de cette balise
	def startElement( self, name, attrs ):
		if( name == "DESCRIPTION" ):
			self.descriptif   = ""
			self.isDescriptif = True
		elif( name == "DATE" ):
			self.isDate = True
		elif( name == "TITRAGE" ):
			self.titre = ""
		elif( name == "TITRE" or name == "SOUS_TITRE" ):
			self.isTitre = True
		elif( name == "PETIT" ):
			self.isLienImage = True
		elif( name == "BAS_DEBIT" ):
			self.isLienLD = True
		elif( name == "HAUT_DEBIT" ):
			self.isLienMD = True
		elif( name == "HD" ):
			self.isLienHD = True

	## Methode qui renvoie les donnees d'une balise
	# @param data Donnees d'une balise
	def characters( self, data ):
		if( self.isDescriptif ):
			self.descriptif += data
		elif( self.isDate ):
			self.date   = data
			self.isDate = False
		elif( self.isTitre ):
			self.titre  += " %s" %( data )
			self.isTitre = False
		elif( self.isLienImage ):
			self.urlImage    = data
			self.isLienImage = False
		elif( self.isLienLD ):
			self.lienLD     = data
			self.isLienLD   = False
		elif( self.isLienHD ):
			self.lienHD     = data
			self.isLienHD   = False
			 
	## Methode appelee lors de la fermeture d'une balise
	# @param name  Nom de la balise
	def endElement( self, name ):
		if( name == "DESCRIPTION" ):
			self.isDescriptif = False
		elif( name == "VIDEO" ):
			self.infosFichier[:] = self.titre, self.date, self.lienLD, self.lienMD, self.lienHD, self.urlImage, self.descriptif

