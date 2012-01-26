#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import base64
from   Crypto.Cipher import DES
import datetime
import os
import pickle
import re
import time
import unicodedata
import xml.sax

import tvdcore

import logging
logger = logging.getLogger( "TVDownloader" )

#
# Filtre Wireshark :
#    http.host == "www.m6replay.fr"
#

#
# Classe
#

class M6Replay( tvdcore.Plugin ):
	
	urlInfosXML = "http://www.m6replay.fr/files/configurationm6_lv3.xml"
	
	def __init__( self ):
		tvdcore.Plugin.__init__( self, "M6Replay", "www.m6replay.fr/", 1, "M6.jpg" )
		self.listeFichiers           = {} # Clefs = nomChaine, Valeurs = { nomEmission, [ [ Episode 1, Date1, URL1 ], ... ] }
		self.listeEmissionsCourantes = {}
		if( os.path.exists( self.fichierCache ) ):
			self.listeFichiers = self.chargerCache()
		
	def rafraichir( self ):
		logger.debug( "récupération de la liste des chaines, des émissions et des fichiers" )
		# Remet a 0 la liste des fichiers
		self.listeFichiers.clear()
		# Recupere la page qui contient les infos sur M6
		pageInfos = self.getPage( self.urlInfosXML )
		# Extrait l'URL du catalogue
		try :
			urlCatalogue = re.findall( "http://www.m6replay.fr/catalogue/\w+.xml", pageInfos )[ 0 ]
			print urlCatalogue
		except:
			logger.error( "impossible de recuperer l'URL du catalogue" )
			return		
		# Recupere le catalogue chiffre
		catalogue = self.getPage( urlCatalogue )		
		# Classe pour dechiffrer le catalogue
		decryptor = DES.new( "ElFsg.Ot", DES.MODE_ECB )
		# Page des emissions (catalogue dechiffre)
		pageEmissions = decryptor.decrypt( base64.decodestring( catalogue ) )
		# Cherche la fin du fichier XML
		finXML = pageEmissions.find( "</template_exchange_WEB>" ) + len( "</template_exchange_WEB>" )
		# Enleve ce qui est apres la fin du fichier XML
		pageEmissions = pageEmissions[ : finXML ]
		# Handler
		handler = M6ReplayHandler( self.listeFichiers )
		# Parse le fichier xml
		try :
			xml.sax.parseString( pageEmissions, handler )
		except:
			logger.error( "impossible de parser le fichier XML" )
			return		
		# Sauvegarde la liste dans le cache
		self.sauvegarderCache( self.listeFichiers )
		logger.debug( "liste des programmes sauvegardée" )
	
	def listerChaines( self ):
		for chaine in self.listeFichiers.keys():
			self.ajouterChaine( chaine )

	def listerEmissions( self, chaine ):
		if( self.listeFichiers.has_key( chaine ) ):
			self.listeEmissionsCourantes = self.listeFichiers[ chaine ]
			for emission in self.listeEmissionsCourantes.keys():
				self.ajouterEmission( chaine, emission )
		else:
			logger.warning( 'chaine "%s" introuvable' %( chaine ) )
	
	def listerFichiers( self, emission ):
		if( self.listeEmissionsCourantes.has_key( emission ) ):
			listeFichiers = self.listeEmissionsCourantes[ emission ]
			for ( nom, date, lien, urlImage, descriptif ) in listeFichiers:
				lienValide = "rtmpe://m6dev.fcod.llnwd.net:443/a3100/d1/mp4:production/regienum/" + lien
				urlImage   = "http://images.m6replay.fr" + urlImage
				# Transforme la date en type datetime.date
				dateBonFormat = datetime.datetime( *( time.strptime( date, "%Y-%m-%d %H:%M:%S" ) )[ 0 : 3 ] )
				# Extrait l'extension du fichier
				basename, extension = os.path.splitext( lien )
				self.ajouterFichier( emission, tvdcore.Fichier( nom, dateBonFormat, lienValide, nom + extension, urlImage, descriptif ) )
		else:
			logger.warning( 'emission "%s" introuvable pour la chaine courante' %( emission ) )

#
# Parser XML pour M6Replay
#

## Classe qui permet de lire les fichiers XML de M6Replay
class M6ReplayHandler( xml.sax.handler.ContentHandler ):

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
				# Commence une nouvelle emission
				pass
			else:
				# Commence une nouvelle chaine
				pass
		elif( name == "nom" ):
			# Si on a nom, cela peut etre (toujours dans cet ordre) :
			# - Le nom de la chaine
			# - Le nom de l'emission
			# - Le nom d'un episode de cette emission
			# - Le nom de la vidéo de cet episode
			# De plus, si on ne connait pas la nom de la chaine, alors le 1er nom rencontre est le nom de la chaine
			if( self.nomChaineConnu ):
				if( self.nomEmissionConnu ):
					if( self.nomEpisodeConnu ): # Nom de la video
						self.isNomVideo = True
					else: # Nom de l'episode
						self.isNomEpisode = True
				else: # Nom de l'emission
					self.isNomEmission = True
			else: # Nom de la chaine
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
			if( self.nomEmissionConnu ): # Fini de traiter une emission
				self.listeEmissions[ self.nomEmission.title() ] = self.listeVideos
				self.listeVideos                                = []
				self.nomEmissionConnu                           = False
			else: # Fini de traiter une chaine
				self.listeFichiers[ self.nomChaine.title() ]    = self.listeEmissions
				self.listeEmissions                             = {}
				self.nomChaineConnu                             = False
		elif( name == "nom" ):
			pass
		elif( name == "diffusion" ):
			self.listeVideos.append( [ self.nomEpisode.title(), self.dateEpisode, self.nomVideo, self.image, self.resume ] )
			self.nomEpisodeConnu = False
			self.nomVideoConnu   = False
