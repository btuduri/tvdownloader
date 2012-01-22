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

# Modules Python
import datetime
import os.path
import re
import xml.sax
from xml.sax.handler import ContentHandler

# Modules de TVD
from tvdcore import Fichier, Plugin

# Logger de TVD
import logging
logger = logging.getLogger( __name__ )

###########
# Classes #
###########

class CanalPlus( Plugin ):
	
	urlFichierXMLListeProgrammes = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/initPlayer"
	urlFichierXMLEmissions       = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getMEAs/"
	urlFichierXMLFichiers        = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getVideos/"
	
	def __init__( self ):
		Plugin.__init__( self, "Canal+", "http://www.canalplus.fr/", 7, "CanalPlus.jpg" )
		
		self.listeProgrammes          = {} # { Nom chaine : { Nom emission : ID emission } }
		self.derniereChaine           = ""
		
		if os.path.exists( self.fichierCache ):
			self.listeProgrammes = self.chargerCache()
		
	def rafraichir( self ):
		logger.info( "récupération de la liste des chaines et des émissions" )
		
		# On remet a 0 la liste des programmes
		self.listeProgrammes.clear()
		
		# On recupere la page qui contient les infos
		pageXML = self.getPage( self.urlFichierXMLListeProgrammes )
		
		# Handler
		handler = CanalPlusListeProgrammesHandler( self.listeProgrammes )
		# On parse le fichier xml
		try:
			xml.sax.parseString( pageXML, handler )
		except:
			logger.error( "impossible de parser le fichier XML de la liste des programmes" )
			return
		
		# On sauvegarde la liste dans le cache
		self.sauvegarderCache( self.listeProgrammes )
		
		logger.info( "liste des programmes sauvegardée" )
		
	def listerChaines( self ):
		for chaine in self.listeProgrammes.keys():
			self.ajouterChaine( chaine )
	
	def listerEmissions( self, chaine ):
		if( self.listeProgrammes.has_key( chaine ) ):
			self.derniereChaine = chaine
			for emission in self.listeProgrammes[ chaine ].keys():
				self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		if( self.listeProgrammes.has_key( self.derniereChaine ) ):
			listeEmissions = self.listeProgrammes[ self.derniereChaine ]
			if( listeEmissions.has_key( emission ) ):
				IDEmission = listeEmissions[ emission ]
				# On recupere la page qui contient les ids des fichiers
				pageXML = self.getPage( self.urlFichierXMLEmissions + IDEmission )
				# On extrait les ids
				listeIDs = re.findall( "<ID>(.+?)</ID>", pageXML )
				# On construit la liste des liens a recuperer
				listeURL = []
				for IDFichier in listeIDs:
					listeURL.append( self.urlFichierXMLFichiers + IDFichier )
				# On recupere les pages correspondantes
				pagesXML = self.getPages( listeURL )
				# On parse chacune de ces pages
				for URL in listeURL:
					pageXMLFichier = pagesXML[ URL ]
					# Handler
					infosFichier = []
					handler      = CanalPlusListeFichierHandler( infosFichier )
					# On parse le fichier xml
					try:
						xml.sax.parseString( pageXMLFichier, handler )
					except:
						logger.error( "impossible de parser le fichier XML de la liste des fichiers" )
						continue
					
					# On ajoute le fichier
					nom, date, lienLD, lienMD, lienHD, urlImage, descriptif = infosFichier
					# On transforme la date en type datetime.date
					try:
						dateDecoupee  = map( int, date.split( "/" ) )
						dateBonFormat = datetime.date( dateDecoupee[ 2 ], dateDecoupee[ 1 ], dateDecoupee[ 0 ] )
					except:
						dateBonFormat = date
					if( lienHD != "" and lienHD[ : 4 ] == "rtmp" ):
						# On extrait l'extension du fichier
						basename, extension = os.path.splitext( lienHD )
						self.ajouterFichier( emission, Fichier( "[HD]" + nom, dateBonFormat, lienHD, nom + extension, urlImage, descriptif ) )	
					elif( lienMD != "" and lienMD[ : 4 ] == "rtmp" ):	
						# On extrait l'extension du fichier
						basename, extension = os.path.splitext( lienMD )
						self.ajouterFichier( emission, Fichier( "[MD]" + nom, dateBonFormat, lienMD, nom + extension, urlImage, descriptif ) )	
					elif( lienLD != "" and lienLD[ : 4 ] == "rtmp" ):	
						# On extrait l'extension du fichier
						basename, extension = os.path.splitext( lienLD )
						self.ajouterFichier( emission, Fichier( "[LD]" + nom, dateBonFormat, lienLD, nom + extension, urlImage, descriptif ) )	
					
#
# Parsers XML pour Canal+
#

## Classe qui permet de lire le fichier XML de Canal qui liste les emissions
class CanalPlusListeProgrammesHandler( ContentHandler ):

	# Constructeur
	# @param listeProgrammes Liste des programmes que le parser va remplir
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

	## Methode appelee lors de l'ouverture d'une balise
	# @param name  Nom de la balise
	# @param attrs Attributs de cette balise
	def startElement( self, name, attrs ):
		if( name == "THEMATIQUE" ):
			pass
		elif( name == "NOM" and self.nomChaineConnu == False ):
			self.isNomChaine = True
		elif( name == "ID" and self.nomChaineConnu == True ):
			self.isIDEmission = True
		elif( name == "NOM" and self.nomChaineConnu == True ):
			self.isNomEmission = True

	## Methode qui renvoie les donnees d'une balise
	# @param data Donnees d'une balise
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
			 
	## Methode appelee lors de la fermeture d'une balise
	# @param name  Nom de la balise
	def endElement( self, name ):
		if( name == "THEMATIQUE" ):
			self.listeProgrammes[ self.nomChaine.title() ] = self.listeEmissions
			self.listeEmissions = {}
			self.nomChaineConnu                            = False
		elif( name == "NOM" and self.nomEmissionConnu ):
			self.listeEmissions[ self.nomEmission.title() ] = self.IDEmission
			self.nomEmissionConnu                           = False

## Classe qui permet de lire le fichier XML d'un fichier de Canal
class CanalPlusListeFichierHandler( ContentHandler ):

	# Constructeur
	# @param infosFichier Infos du fichier que le parser va remplir
	def __init__( self, infosFichier ):
		# Liste des programmes
		self.infosFichier = infosFichier
		
		# On n'a pas forcement les 3 liens
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


