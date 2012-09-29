#!/usr/bin/env python
# -*- coding:Utf-8 -*-

# Coucou les amis

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
import xml.sax
from xml.sax.handler import ContentHandler

import urllib
import unicodedata

from Fichier import Fichier
from Plugin import Plugin

##########
# Classe #
##########

class Podcasts( Plugin ):
	
	listePodcasts  = { "Allo Cine"    : { "Bandes Annonces" : "http://rss.allocine.fr/bandesannonces/ipod" },
					   "Casse Croute" : { "Recettes" : "http://www.casse-croute.fr/media/cassecroute.xml" },
					   "Game One"     : { u"E-NEWS JEUX VIDEO" : "http://podcast13.streamakaci.com/xml/GAMEONE2.xml",
									      u"NEWS DU JT"        : "http://podcast13.streamakaci.com/xml/GAMEONE6.xml",
									      u"LE TEST"           : "http://podcast13.streamakaci.com/xml/GAMEONE3.xml",
									      u"PLAY HIT"          : "http://podcast13.streamakaci.com/xml/GAMEONE9.xml",
									      u"RETRO GAME ONE"    : "http://podcast13.streamakaci.com/xml/GAMEONE11.xml",
									      u"Funky Web"         : "http://podcast13.streamakaci.com/xml/GAMEONE26.xml"
									    },
					   "No Watch"     : { u"CINEFUZZ" : "http://feeds.feedburner.com/CineFuzz?format=xml",
										  u"GEEK Inc (SD)" : "http://feeds.feedburner.com/GeekInc?format=xml",
										  u"GEEk Inc (HD)" : "http://feeds.feedburner.com/GeekIncHD?format=xml",
										  u"S.C.U.D.S tv (SD)" : "http://feeds2.feedburner.com/scudstv?format=xml",
										  u"S.C.U.D.S tv (HD)" : "http://feeds2.feedburner.com/scudshd?format=xml",
										  u"Tonight On Mars (SD)" : "http://feeds2.feedburner.com/tonightonmars?format=xml",
										  u"Zapcast tv (SD)" : "http://feeds.feedburner.com/Zapcasttv?format=xml",
										  u"Zapcast tv (HD)" : "http://feeds.feedburner.com/Zapcasthd?format=xml"},

					   "i>TELE"       : { "Le Journal" : "http://podcast12.streamakaci.com/iTELE/iTELElejournal.xml" },
					   "RMC"          : { u"Bourdin & CO" : "http://podcast.rmc.fr/channel30/RMCInfochannel30.xml",
											u"Coach Courbis" : "http://podcast.rmc.fr/channel33/RMCInfochannel33.xml",
											u"De quoi je me mail" : "http://podcast.rmc.fr/channel35/RMCInfochannel35.xml",
											u"Intégrale Foot Made in Di Meco" : "http://podcast.rmc.fr/channel192/RMCInfochannel192.xml",
											u"JO Live du jour" : "http://podcast.rmc.fr/channel196/RMCInfochannel196.xml",
											u"L'Afterfoot" : "http://podcast.rmc.fr/channel59/RMCInfochannel59.xml",
											u"Lahaie, l'amour et vous" : "http://podcast.rmc.fr/channel51/RMCInfochannel51.xml",
											u"La politique " : "http://podcast.rmc.fr/channel179/RMCInfochannel179.xml",
											u"La quotidienne courses hippiques" : "http://podcast.rmc.fr/channel197/RMCInfochannel197.xml",
											u"Larqué Foot" : "http://podcast.rmc.fr/channel53/RMCInfochannel53.xml",
											u"Le Billet de Guimard" : "http://podcast.rmc.fr/channel210/RMCInfochannel210.xml",
											u"L'économie" : "http://podcast.rmc.fr/channel178/RMCInfochannel178.xml",
											u"Le Débat du jour" : "http://podcast.rmc.fr/channel211/RMCInfochannel211.xml",
											u"Le Journal du jour" : "http://podcast.rmc.fr/channel39/RMCInfochannel39.xml",
											u"Le Mercato Show" : "http://podcast.rmc.fr/channel213/RMCInfochannel213.xml",
											u"Le Monde Hi-Tech" : "http://podcast.rmc.fr/channel31/RMCInfochannel31.xml",
											u"Les courses RMC" : "http://podcast.rmc.fr/channel193/RMCInfochannel193.xml",
											u"Les Experts F1" : "http://podcast.rmc.fr/channel191/RMCInfochannel191.xml",
											u"Les GG et vous" : "http://podcast.rmc.fr/channel181/RMCInfochannel181.xml",
											u"Les Grandes Gueules" : "http://podcast.rmc.fr/channel36/RMCInfochannel36.xml",
											u"Les Paris RMC du samedi" : "http://podcast.rmc.fr/channel160/RMCInfochannel160.xml",
											u"Le Top de l'After Foot" : "http://podcast.rmc.fr/channel174/RMCInfochannel174.xml",
											u"Le top de Sportisimon" : "http://podcast.rmc.fr/channel188/RMCInfochannel188.xml",
											u"Le Top rugby " : "http://podcast.rmc.fr/channel176/RMCInfochannel176.xml",
											u"Le Tour du jour" : "http://podcast.rmc.fr/channel209/RMCInfochannel209.xml",
											u"L'invité de Bourdin & Co" : "http://podcast.rmc.fr/channel38/RMCInfochannel38.xml",
											u"L'invité de Captain Larqué" : "http://podcast.rmc.fr/channel175/RMCInfochannel175.xml",
											u"L'invité de Luis" : "http://podcast.rmc.fr/channel170/RMCInfochannel170.xml",
											u"Love conseil " : "http://podcast.rmc.fr/channel183/RMCInfochannel183.xml",
											u"Luis Attaque" : "http://podcast.rmc.fr/channel40/RMCInfochannel40.xml",
											u"Moscato Show" : "http://podcast.rmc.fr/channel131/RMCInfochannel131.xml",
											u"Moscato Show " : "http://podcast.rmc.fr/channel190/RMCInfochannel190.xml",
											u"Motors" : "http://podcast.rmc.fr/channel42/RMCInfochannel42.xml",
											u"RMC première Le 5/7" : "http://podcast.rmc.fr/channel32/RMCInfochannel32.xml",
											u"RMC Sport matin" : "http://podcast.rmc.fr/channel77/RMCInfochannel77.xml",
											u"Sportisimon" : "http://podcast.rmc.fr/channel186/RMCInfochannel186.xml",
											u"Vos Animaux" : "http://podcast.rmc.fr/channel48/RMCInfochannel48.xml",
											u"Votre Auto" : "http://podcast.rmc.fr/channel50/RMCInfochannel50.xml",
											u"Votre Jardin" : "http://podcast.rmc.fr/channel52/RMCInfochannel52.xml",
											u"Votre Maison" : "http://podcast.rmc.fr/channel54/RMCInfochannel54.xml"
										},
							"RTL"     : { u"Grosse Tetes" : "http://www.rtl.fr/podcast/les-grosses-tetes.xml",
										  u"Laurent Gerra"        : 
										  "http://www.rtl.fr/podcast/laurent-gerra.xml",
										  u"A la bonne heure"           : 
										  "http://www.rtl.fr/podcast/a-la-bonne-heure.xml",
										  u"l heure du crime"               :
										  "http://www.rtl.fr/podcast/l-heure-du-crime.xml", 
										  u"l invite de rtl"           : 
										  "http://www.rtl.fr/podcast/linvite-de-rtl.xml",
										  u"z comme zemmour"           : 
										  "http://www.rtl.fr/podcast/z-comme-zemmour.xml",
										  u"Ca peut vous arriver"           : 
										  "http://www.rtl.fr/podcast/ca-peut-vous-arriver.xml",
										  u"le club liza.xml"           : 
										  "http://www.rtl.fr/podcast/le-club-liza.xml",
										  u"face a face aphatie duhamel en video"           : 
										  "http://www.rtl.fr/podcast/face-a-face-aphatie-duhamel-en-video.xml.xml",
										  u"La marque du mailhot"           : 
										  "http://www.rtl.fr/podcast/la-marque-du-mailhot.xml",
										  u"Le choix de yves calvi"           : 
										  "http://www.rtl.fr/podcast/le-choix-de-yves-calvi.xml",
										  u"Le choix de yves calvi en video"           : 
										  "http://www.rtl.fr/podcast/le-choix-de-yves-calvi-en-video.xml",
										  u"le grand jury"           : 
										  "http://www.rtl.fr/podcast/le-grand-jury.xml",
										  u"le journal inattendu"           : 
										  "http://www.rtl.fr/podcast/le-journal-inattendu.xml",
										  u"le fait politique"           : 
										  "http://www.rtl.fr/podcast/le-fait-politique.xml",
										  u"on est fait pour s entendre"           : 
										  "http://www.rtl.fr/podcast/on-est-fait-pour-s-entendre.xml",
										  u"a-la-bonne-heure didier porte"           : 
										  "http://www.rtl.fr/podcast/a-la-bonne-heure-didier-porte.xml",
										  u"on refait le match - Christophe Pacaud"           : 
										  "http://www.rtl.fr/podcast/on-refait-le-match-avec-christophe-pacaud.xml",
										  u"on refait le match - Eugene Saccomano"        : 
										  "http://www.rtl.fr/podcast/on-refait-le-match-avec-eugene-saccomano.xml",
										  u"a-la-bonne-heure Eric Naulleau"           : 
										  "http://www.rtl.fr/podcast/a-la-bonne-heure-eric-naulleau.xml",
										  u"a-la-bonne-heure Eric Naulleau en video"           : 
										  "http://www.rtl.fr/podcast/a-la-bonne-heure-eric-naulleau-en-video.xml",
										  }
					 }
	derniereChaine = ""
	listeFichiers  = []
	
	def __init__( self):
		Plugin.__init__( self, "Podcasts", "", 30 )
		
	def rafraichir( self ):
		pass # Rien a rafraichir ici...	   
	
	def listerChaines( self ):
		listeChaines = self.listePodcasts.keys()
		listeChaines.sort()
		for chaine in listeChaines:
			self.ajouterChaine( chaine )

	def listerEmissions( self, chaine ):
		if( self.listePodcasts.has_key( chaine ) ):
			self.derniereChaine = chaine
			listeEmissions = self.listePodcasts[ chaine ].keys()
			listeEmissions.sort()
			for emission in listeEmissions:
				self.ajouterEmission( chaine, emission )
	
	def listerFichiers( self, emission ):
		if( self.listePodcasts.has_key( self.derniereChaine ) ):
			listeEmission = self.listePodcasts[ self.derniereChaine ]
			if( listeEmission.has_key( emission ) ):
				# On remet a 0 la liste des fichiers
				del self.listeFichiers[ : ]
				# On recupere la page de l'emission
				page = urllib.urlopen( listeEmission[ emission ] )
				page = page.read()
				#~ page = self.API.getPage( listeEmission[ emission ] )
				# Handler
				handler = PodcastsHandler( self.listeFichiers )
				# On parse le fichier xml
				xml.sax.parseString( page, handler )
				
				# On ajoute les fichiers
				for fichier in self.listeFichiers:
					self.ajouterFichier( emission, fichier )

#
# Parser XML pour les podcasts
#

## Classe qui permet de lire les fichiers XML de podcasts
class PodcastsHandler( ContentHandler ):

	# Constructeur
	# @param listeFichiers Liste des fichiers que le parser va remplir
	def __init__( self, listeFichiers ):
		# Liste des fichiers
		self.listeFichiers = listeFichiers
		
		# Url de l'image globale
		self.urlImageGlobale = ""
		
		# Initialisation des variables a Faux
		self.isItem        = False
		self.isTitle       = False
		self.isDescription = False
		self.isPubDate     = False
		self.isGuid        = False

	## Methode appelee lors de l'ouverture d'une balise
	# @param name  Nom de la balise
	# @param attrs Attributs de cette balise
	def startElement( self, name, attrs ):
		if( name == "item" ):
			self.isItem          = True
			self.titre           = ""
			self.date            = ""
			self.urlFichier      = ""
			self.urlImage        = ""
			self.description     = ""
		elif( name == "title" and self.isItem ):
			self.isTitle = True
		elif( name == "description" and self.isItem ):
			self.isDescription = True
		elif( name == "pubDate" and self.isItem ):
			self.isPubDate = True
		elif( name == "media:thumbnail" and self.isItem ):
			self.urlImage = attrs.get( "url", "" )
		elif( name == "media:content" and self.isItem ):
			self.urlFichier = attrs.get( "url", "" )
		elif( name == "guid" and self.isItem ):
			self.isGuid = True
		elif( name == "itunes:image" and not self.isItem ):
			self.urlImageGlobale = attrs.get( "href", "" )

	## Methode qui renvoie les donnees d'une balise
	# @param data Donnees d'une balise
	def characters( self, data ):
		if( self.isTitle ):
			self.titre   += data
			#~ self.isTitle = False
		elif( self.isDescription ):
			if( data.find( "<" ) == -1 ):
				self.description  += data
			else:
				self.isDescription = False
		elif( self.isPubDate ):
			self.date      = data
			self.isPubDate = False
		elif( self.isGuid ):
			self.urlFichier = data
			self.isGuid     = False
			
	## Methode appelee lors de la fermeture d'une balise
	# @param name  Nom de la balise
	def endElement( self, name ):
		if( name == "item" ):
			# On extrait l'extension du fichier
			basename, extension = os.path.splitext( self.urlFichier )
			# Si le fichier n'a pas d'image, on prend l'image globale
			if( self.urlImage == "" ):
				self.urlImage = self.urlImageGlobale
			# On ajoute le fichier
			self.listeFichiers.append( Fichier ( self.titre, self.date, self.urlFichier, self.titre + extension, self.urlImage, self.description ) )
			self.isTitle = False
		elif( name == "description" ):
			self.isDescription = False
		elif( name == "title" ):
			self.isTitle = False
		
