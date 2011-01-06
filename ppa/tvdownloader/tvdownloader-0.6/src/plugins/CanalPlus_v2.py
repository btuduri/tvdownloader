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
import pickle
import xml.sax
from xml.sax.handler import ContentHandler
#~ import urllib
#~ import unicodedata

from Fichier import Fichier
from Plugin import Plugin

###########
# Classes #
###########

class CanalPlusv2( Plugin ):
	
	urlFichierXMLListeProgrammes = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/initPlayer"
	urlFichierXMLEmissions = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getMEAs/"
	urlFichierXMLFichiers = "http://www.canalplus.fr/rest/bootstrap.php?/bigplayer/getVideos/"
	listeProgrammes = {} # Clef = Nom Chaine, Valeur = { Nom emission : ID }
	derniereChaine = ""
	
	def __init__( self ):
		Plugin.__init__( self, "Canal+ v2", "http://www.canalplus.fr/", 7 )
		
		if os.path.exists( self.fichierCache ):
			self.listeProgrammes = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		
		# On remet a 0 la liste des programmes
		self.listeProgrammes.clear()
		
		# On recupere la page qui contient les infos
		#~ page = urllib.urlopen( self.urlFichierXMLListeProgrammes )
		#~ pageXML = page.read()
		pageXML = self.API.getPage( self.urlFichierXMLListeProgrammes )
		
		# Handler
		handler = CanalPlusListeProgrammesHandler( self.listeProgrammes )
		# On parse le fichier xml
		xml.sax.parseString( pageXML, handler )
		
		self.sauvegarderCache( self.listeProgrammes )
		
		self.afficher( "Emissions conservées." )
		
	def listerChaines( self ):
		liste = self.listeProgrammes.keys()
		liste.sort()
		for chaine in liste:
			self.ajouterChaine( chaine )
	
	def listerEmissions( self, chaine ):
		if( self.listeProgrammes.has_key( chaine ) ):
			self.derniereChaine = chaine
			liste = self.listeProgrammes[ chaine ].keys()
			liste.sort()
			for emission in liste:
				self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		if( self.listeProgrammes.has_key( self.derniereChaine ) ):
			listeEmissions = self.listeProgrammes[ self.derniereChaine ]
			if( listeEmissions.has_key( emission ) ):
				IDEmission = listeEmissions[ emission ]
				# On recupere la page qui contient les ids des fichiers
				pageXML = self.API.getPage( self.urlFichierXMLEmissions + IDEmission )
				# On extrait les ids
				listeIDs = re.findall( "<ID>(.+?)</ID>", pageXML )
				# Pour chacun des IDs, on va recuperer les infos sur la videos
				for IDFichier in listeIDs:
					pageXMLFichier = self.API.getPage( self.urlFichierXMLFichiers + IDFichier )
					
					# Handler
					infosFichier = []
					handler = CanalPlusListeFichierHandler( infosFichier )
					# On parse le fichier xml
					xml.sax.parseString( pageXMLFichier, handler )
					
					# On ajoute le fichier
					nom, date, lienLD, lienMD, lienHD, urlImage, descriptif = infosFichier
					if( lienHD != "" and lienHD[ : 4 ] == "rtmp" ):
						# On extrait l'extension du fichier
						basename, extension = os.path.splitext( lienHD )
						self.ajouterFichier( emission, Fichier( "[HD]" + nom, date, lienHD, nom + extension, urlImage, descriptif ) )	
					elif( lienMD != "" and lienMD[ : 4 ] == "rtmp" ):	
						# On extrait l'extension du fichier
						basename, extension = os.path.splitext( lienMD )
						self.ajouterFichier( emission, Fichier( "[MD]" + nom, date, lienMD, nom + extension, urlImage, descriptif ) )	
					elif( lienLD != "" and lienLD[ : 4 ] == "rtmp" ):	
						# On extrait l'extension du fichier
						basename, extension = os.path.splitext( lienLD )
						self.ajouterFichier( emission, Fichier( "[LD]" + nom, date, lienLD, nom + extension, urlImage, descriptif ) )	
					
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
		