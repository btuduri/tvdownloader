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
import base64
from Crypto.Cipher import DES
import xml.sax
from xml.sax.handler import ContentHandler

from Fichier import Fichier
from Plugin import Plugin

##########
# Classes #
##########

class M6Replay( Plugin ):
	
	def __init__( self ):
		Plugin.__init__( self, "M6Replay", "www.m6replay.fr/", 0)
		
		# Liste des programmes sous la forme
		# { Emission1 : [ [ Episode 1, Date1, URL1 ], ... ], Emission2 : ... }
		self.listeProgrammes = {}

		if os.path.exists( self.fichierCache ):
			self.listeProgrammes = self.chargerCache()
		
	def rafraichir( self ):
		self.afficher( u"Récupération de la liste des émissions..." )
		
		# On remet a 0 la liste des programmes
		self.listeProgrammes.clear()
		
		# On recupere la page qui contient les donnees chiffrees
		pageEmissionsChiffree = self.API.getPage( "http://www.m6replay.fr/catalogue/catalogueWeb3.xml" )
		
		#
		# N.B. : La page http://www.m6replay.fr/catalogue/catalogueWeb4.xml semble contenir
		#        des videos non presentent sur le site...
		#        Il faudrait voir ce qu'il en retourne (pourquoi ne sont-elles pas sur le site ? les liens fonctionnent-ils ?)
		#
		
		# Classe pour dechiffrer la page
		decryptor = DES.new( "ElFsg.Ot", DES.MODE_ECB )
		# Page des emissions dechiffree
		pageEmissions = decryptor.decrypt( base64.decodestring( pageEmissionsChiffree ) )
		# On cherche la fin du fichier XML
		finXML = pageEmissions.find( "</template_exchange_WEB>" ) + len( "</template_exchange_WEB>" )
		# On enleve ce qui est apres la fin du fichier XML
		pageEmissions = pageEmissions[ : finXML ]
		
		# Handler
		handler = M6ReplayHandler( self.listeProgrammes )
		# On parse le fichier xml
		xml.sax.parseString( pageEmissions, handler )
		
		self.sauvegarderCache( self.listeProgrammes )
		self.afficher( str( len( self.listeProgrammes.keys() ) ) + " émissions concervées." )
	
	def listerChaines( self ):
		self.ajouterChaine(self.nom)

	def listerEmissions( self, chaine ):
		# On renvoit le resulat
		liste = self.listeProgrammes.keys()
		liste.sort()
		for emission in liste:
			self.ajouterEmission(chaine, emission)
	
	def listerFichiers( self, emission ):
		try:
			infosEpisodes = self.listeProgrammes[ emission ]
		except KeyError :
			return
		
		for info in infosEpisodes:
			episode  = info[ 0 ]
			date     = info[ 1 ]
			lien     = "rtmpe://m6dev.fcod.llnwd.net:443/a3100/d1/mp4:production/regienum/" + info[ 2 ]
			
			self.ajouterFichier(emission, Fichier( episode, date, lien ) )

#
# Parser XML pour W9Replay
#

## Classe qui permet de lire les fichiers XML de M6Replay
class M6ReplayHandler( ContentHandler ):

	# Constructeur
	# @param listeProgrammes Liste des programmes que le parser va remplir
	def __init__( self, listeProgrammes ):
		# Initialisation des variables a Faux
		self.nomEmissionConnu = False
		self.nomEpisodeConnu  = False
		self.nomVideoConnu    = False
		self.isNomEmission    = False
		self.isNomEpisode     = False
		self.isNomVideo       = False
		# Liste des programmes
		self.listeProgrammes = listeProgrammes
		# Liste des videos (temporaire, ajoute au fur et a mesure dans listeProgrammes )
		self.listeVideos = []

	## Methode appelee lors de l'ouverture d'une balise
	# @param name  Nom de la balise
	# @param attrs Attributs de cette balise
	def startElement( self, name, attrs ):
		if( name == "categorie" ):
			# On commence une nouvelle emission
			pass
		elif( name == "nom" ):
			# Si on a nom, cela peut etre (toujours dans cet ordre) :
			# - Le nom de l'emission
			# - Le nom d'un episode de cette emission
			# - Le nom de la vidéo de cet episode
			if( self.nomEmissionConnu ):
				if( self.nomEpisodeConnu ): # Alors on a le nom de la video
					self.isNomVideo = True
				else: # Alors on a le nom de l'episode
					self.isNomEpisode = True
			else: # Alors on a le nom de l'emission
				self.isNomEmission = True
		elif( name == "diffusion" ):
			self.dateEpisode = attrs.get( "date", "" ) 		

	## Methode qui renvoie les donnees d'une balise
	# @param data Donnees d'une balise
	def characters( self, data ):
		if( self.isNomEmission ):
			self.nomEmission = data
			self.nomEmissionConnu = True
			self.isNomEmission = False
		elif( self.isNomEpisode ):
			self.nomEpisode = data
			self.nomEpisodeConnu = True
			self.isNomEpisode = False
		elif( self.isNomVideo ):
			self.nomVideo = data
			self.nomVideoConnu = True
			self.isNomVideo = False

	## Methode appelee lors de la fermeture d'une balise
	# @param name  Nom de la balise
	def endElement( self, name ):
		if( name == "categorie" ):
			self.listeProgrammes[ self.nomEmission ] = self.listeVideos
			self.listeVideos = []
			self.nomEmissionConnu = False
		elif( name == "nom" ):
			pass
		elif( name == "diffusion" ):
			self.listeVideos.append( [ self.nomEpisode, self.dateEpisode, self.nomVideo ] )
			self.nomEpisodeConnu = False
			self.nomVideoConnu = False
