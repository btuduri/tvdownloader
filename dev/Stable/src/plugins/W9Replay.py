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
import urllib
import unicodedata

from Fichier import Fichier
from Plugin import Plugin

###########
# Classes #
###########

class W9Replay( Plugin ):
	
	urlFichierXML = "http://data.w9replay.fr/catalogue/120-w9.xml"
	listeFichiers = {} # Clefs = nomChaine, Valeurs = { nomEmission, [ [ Episode 1, Date1, URL1 ], ... ] }
	
	def __init__( self ):
		Plugin.__init__( self, "W9Replay", "http://www.w9replay.fr/", 1 )
		
		self.listeEmissionsCourantes = {}
		
		if os.path.exists( self.fichierCache ):
			self.listeFichiers = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions et des fichiers..." )
		
		# On remet a 0 la liste des fichiers
		self.listeFichiers.clear()
		# On recupere la page qui contient les infos
		page = urllib.urlopen( self.urlFichierXML )
		pageXML = page.read()
		#~ pageXML = self.API.getPage( self.urlFichierXML )
		
		# Handler
		handler = W9ReplayHandler( self.listeFichiers )
		# On parse le fichier xml
		xml.sax.parseString( pageXML, handler )
		
		self.sauvegarderCache( self.listeFichiers )
		self.afficher( u"Liste sauvegardée" )
		
	def listerChaines( self ):
		for chaine in self.listeFichiers.keys():
			self.ajouterChaine( chaine )
	
	def listerEmissions( self, chaine ):
		if( self.listeFichiers.has_key( chaine ) ):
			self.listeEmissionsCourantes = self.listeFichiers[ chaine ]
			for emission in self.listeEmissionsCourantes.keys():
				self.ajouterEmission( chaine, emission )
				
	def listerFichiers( self, emission ):
		if( self.listeEmissionsCourantes.has_key( emission ) ):
			listeFichiers = self.listeEmissionsCourantes[ emission ]
			for ( nom, date, lien, urlImage, descriptif ) in listeFichiers:
				lienValide = "rtmpe://m6dev.fcod.llnwd.net:443/a3100/d1/mp4:production/w9replay/" + lien
				urlImage = "http://images.w9replay.fr" + urlImage
				# On extrait l'extension du fichier
				basename, extension = os.path.splitext( lien )
				self.ajouterFichier( emission, Fichier( nom, date, lienValide, nom + extension, urlImage, descriptif ) )	
	
#
# Parser XML pour W9Replay
#

## Classe qui permet de lire les fichiers XML de W9Replay
class W9ReplayHandler( ContentHandler ):

	# Constructeur
	# @param listeFichiers Liste des fichiers que le parser va remplir
	def __init__( self, listeFichiers ):
		# Liste des fichiers
		self.listeFichiers = listeFichiers
		# Liste des emissions (temporaire, ajoute au fur et a mesure dans listeFichiers)
		self.listeEmissions = {}
		# Liste des videos (temporaire, ajoute au fur et a mesure dans listeEmissions)
		self.listeVideos = []
		
		# Initialisation des variables a Faux
		self.nomChaineConnu   = False
		self.nomEmissionConnu = False
		self.nomEpisodeConnu  = False
		self.nomVideoConnu    = False
		self.isNomChaine      = False
		self.isNomEmission    = False
		self.isNomEpisode     = False
		self.isNomVideo       = False
		self.isResume         = False

	## Methode appelee lors de l'ouverture d'une balise
	# @param name  Nom de la balise
	# @param attrs Attributs de cette balise
	def startElement( self, name, attrs ):
		if( name == "categorie" ):
			if( self.nomChaineConnu ):
				# On commence une nouvelle emission
				pass
			else:
				# On commence une nouvelle chaine
				pass
		elif( name == "nom" ):
			# Si on a nom, cela peut etre (toujours dans cet ordre) :
			# - Le nom de l'emission
			# - Le nom d'un episode de cette emission
			# - Le nom de la vidéo de cet episode
			# De plus, si on ne connait pas la nom de la chaine, alors le 1er nom rencontre est le nom de la chaine
			if( self.nomChaineConnu ):
				if( self.nomEmissionConnu ):
					if( self.nomEpisodeConnu ): # Alors on a le nom de la video
						self.isNomVideo = True
					else: # Alors on a le nom de l'episode
						self.isNomEpisode = True
				else: # Alors on a le nom de l'emission
					self.isNomEmission = True
			else: # Alors on a le nom de la chaine
				self.isNomChaine = True
		elif( name == "diffusion" ):
			self.dateEpisode = attrs.get( "date", "" )
		elif( name == "resume" ):
			self.isResume = True
		elif( name == "produit" ):
			self.image = attrs.get( "sml_img_url", "" )

	## Methode qui renvoie les donnees d'une balise
	# @param data Donnees d'une balise
	def characters( self, data ):
		data = unicodedata.normalize( 'NFKD', data ).encode( 'ascii','ignore' )
		if( self.isNomChaine ):
			self.nomChaine         = data
			self.nomChaineConnu    = True
			self.isNomChaine       = False
		elif( self.isNomEmission ):
			self.nomEmission       = data
			self.nomEmissionConnu  = True
			self.isNomEmission     = False
		elif( self.isNomEpisode ):
			self.nomEpisode        = data
			self.nomEpisodeConnu   = True
			self.isNomEpisode      = False
		elif( self.isNomVideo ):
			self.nomVideo          = data
			self.nomVideoConnu     = True
			self.isNomVideo        = False
		elif( self.isResume ):
			self.resume            = data
			self.isResume          = False

	## Methode appelee lors de la fermeture d'une balise
	# @param name  Nom de la balise
	def endElement( self, name ):
		if( name == "categorie" ):
			if( self.nomEmissionConnu ): # On a fini de traiter une emission
				self.listeEmissions[ self.nomEmission.title() ] = self.listeVideos
				self.listeVideos                                = []
				self.nomEmissionConnu                           = False
			else: # On a fini de traiter une chaine
				self.listeFichiers[ self.nomChaine.title() ]    = self.listeEmissions
				self.listeEmissions                             = {}
				self.nomChaineConnu                             = False
		elif( name == "nom" ):
			pass
		elif( name == "diffusion" ):
			self.listeVideos.append( [ self.nomEpisode.title(), self.dateEpisode, self.nomVideo, self.image, self.resume ] )
			self.nomEpisodeConnu = False
			self.nomVideoConnu   = False
