#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import dateutil.parser
import logging
logger = logging.getLogger( "TVDownloader" )
import os
import re
import xml.sax

import tvdcore

#
# Classes
#

class CanalPlus( tvdcore.Plugin ):
	
	urlFichierXMLListeProgrammes = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/initPlayer"
	urlFichierXMLEmissions       = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getMEAs/"
	urlFichierXMLFichiers        = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getVideos/"
	
	def __init__( self ):
		tvdcore.Plugin.__init__( self, "Canal+", "http://www.canalplus.fr/", 7 )
		
		self.listeProgrammes          = {} # { Nom chaine : { Nom emission : ID emission } }
		self.derniereChaine           = ""
		
		if( os.path.exists( self.fichierCache ) ):
			self.listeProgrammes = self.chargerCache()
		
	def rafraichir( self ):
		# RAZ de la liste des programmes
		self.listeProgrammes.clear()
		
		# Recupere la page qui contient les infos
		pageXML = self.getPage( self.urlFichierXMLListeProgrammes )
		
		# Handler
		handler = CanalPlusListeProgrammesHandler( self.listeProgrammes )
		# Parse le fichier xml
		try:
			xml.sax.parseString( pageXML, handler )
		except:
			logger.error( "Impossible de parser le fichier XML de la liste des programmes" )
			return
		
		# Sauvegarde la liste dans le cache
		self.sauvegarderCache( self.listeProgrammes )
		
	def listerChaines( self ):
		map( lambda x : self.ajouterChaine( ( x, None ) ), self.listeProgrammes )
	
	def listerEmissions( self, chaine ):
		if( self.listeProgrammes.has_key( chaine ) ):
			self.derniereChaine = chaine
			map( lambda x : self.ajouterEmission( chaine, x ), self.listeProgrammes[ chaine ].keys() )
				
	def listerFichiers( self, emission ):
		if( self.listeProgrammes.has_key( self.derniereChaine ) ):
			listeEmissions = self.listeProgrammes[ self.derniereChaine ]
			if( listeEmissions.has_key( emission ) ):
				IDEmission = listeEmissions[ emission ]
				# Recupere la page qui contient les ids des fichiers
				pageXML = self.getPage( self.urlFichierXMLEmissions + IDEmission )
				# Extrait les ids
				listeIDs = re.findall( "<ID>(.+?)</ID>", pageXML )
				# Construit la liste des liens a recuperer
				listeURL = []
				for IDFichier in listeIDs:
					listeURL.append( self.urlFichierXMLFichiers + IDFichier )
				# Recupere les pages correspondantes
				pagesXML = self.getPages( listeURL )
				# Parse chacune de ces pages
				for URL in listeURL:
					pageXMLFichier = pagesXML[ URL ]
					# Handler
					infosFichier = []
					handler      = CanalPlusListeFichierHandler( infosFichier )
					# Parse le fichier xml
					try:
						xml.sax.parseString( pageXMLFichier, handler )
					except:
						logger.error( "Impossible de parser le fichier XML de la liste des fichiers" )
						continue
					# Ajoute le fichier
					nom, date, lienLD, lienMD, lienHD, urlImage, descriptif = infosFichier
					if( lienHD != "" and lienHD[ : 4 ] == "rtmp" ):
						# Extrait l'extension du fichier
						basename, extension = os.path.splitext( lienHD )
						self.ajouterFichier( emission, tvdcore.Fichier( "[HD]" + nom, date, lienHD, nom + extension, urlImage, descriptif ) )	
					elif( lienMD != "" and lienMD[ : 4 ] == "rtmp" ):	
						# Extrait l'extension du fichier
						basename, extension = os.path.splitext( lienMD )
						self.ajouterFichier( emission, tvdcore.Fichier( "[MD]" + nom, date, lienMD, nom + extension, urlImage, descriptif ) )	
					elif( lienLD != "" and lienLD[ : 4 ] == "rtmp" ):	
						# Extrait l'extension du fichier
						basename, extension = os.path.splitext( lienLD )
						self.ajouterFichier( emission, tvdcore.tvdcore.Fichier( "[LD]" + nom, date, lienLD, nom + extension, urlImage, descriptif ) )

class CanalPlusListeProgrammesHandler( xml.sax.handler.ContentHandler ):
	"""
	Classe pour paser le XML qui liste les emissions
	"""

	def __init__( self, listeProgrammes ):
		# Liste des programmes
		self.listeProgrammes = listeProgrammes
		
		# Liste des emissions d'un programme (temporaire)
		# Clef : nom emission, Valeur : ID
		self.listeEmissions  = {}
		
		# Initialisation des variables a Faux
		self.nomChaineConnu   = False
		self.isNomChaine      = False
		self.isIDEmission     = False
		self.nomEmissionConnu = False
		self.isNomEmission    = False

	def startElement( self, name, attrs ):
		if( name == "THEMATIQUE" ):
			pass
		elif( name == "NOM" and self.nomChaineConnu == False ):
			self.isNomChaine = True
		elif( name == "ID" and self.nomChaineConnu == True ):
			self.isIDEmission = True
		elif( name == "NOM" and self.nomChaineConnu == True ):
			self.isNomEmission = True

	def characters( self, data ):
		if( self.isNomChaine ):
			self.nomChaine      = data
			self.nomChaineConnu = True
			self.isNomChaine    = False
		elif( self.isIDEmission ):
			self.IDEmission   = data
			self.isIDEmission = False
		elif( self.isNomEmission ):
			self.nomEmission      = data
			self.nomEmissionConnu = True
			self.isNomEmission    = False

	def endElement( self, name ):
		if( name == "THEMATIQUE" ):
			self.listeProgrammes[ self.nomChaine.title() ] = self.listeEmissions
			self.listeEmissions = {}
			self.nomChaineConnu                            = False
		elif( name == "NOM" and self.nomEmissionConnu ):
			self.listeEmissions[ self.nomEmission.title() ] = self.IDEmission
			self.nomEmissionConnu                           = False

class CanalPlusListeFichierHandler( xml.sax.handler.ContentHandler ):
	"""
	Classe qui parse le XML de description d'un fichier
	"""
	
	def __init__( self, infosFichier ):
		# Liste des programmes
		self.infosFichier = infosFichier
		
		# Il n'y a pas forcement les 3 liens
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

	def endElement( self, name ):
		if( name == "DESCRIPTION" ):
			self.isDescriptif = False
		elif( name == "VIDEO" ):
			# Convertit la date
			try:
				self.dateOk = dateutil.parser.parse( self.date )
			except:
				self.dateOk = self.date
			self.infosFichier[ : ] = self.titre, self.dateOk, self.lienLD, self.lienMD, self.lienHD, self.urlImage, self.descriptif
