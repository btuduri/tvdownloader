#!/usr/bin/env python
# -*- coding:Utf-8 -*-

# Notes :
#    -> Filtre Wireshark : 
#          http.host contains "ftvodhdsecz" or http.host contains "francetv" or http.host contains "pluzz"
#    -> 

#
# Modules
#

import base64
import binascii
import hashlib
import hmac
import os
import re
import StringIO
import struct
import sys
import threading
import urllib
import urllib2
import xml.etree.ElementTree
import xml.sax
import zlib

from Configuration import Configuration
from Historique    import Historique, Video
from Navigateur    import Navigateur

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Classes
#

class PluzzDL( object ):
	"""
	Classe principale
	"""
	
	def __init__( self, url, useFragments = False, proxy = None, resume = False, progressFnct = lambda x : None, stopDownloadEvent = threading.Event(), outDir = "." ):
		# Options
		self.url               = url
		self.useFragments      = useFragments
		self.proxy             = proxy
		self.resume            = resume
		self.progressFnct      = progressFnct
		self.stopDownloadEvent = stopDownloadEvent
		self.outDir            = outDir
		# Classes
		self.navigateur        = Navigateur( self.proxy )
		# Infos video
		self.id                = None
		self.lienMMS           = None
		self.lienRTMP          = None
		self.manifestURL       = None
		self.m3u8URL           = None
		self.drm               = None
		
		# Liens pluzz.fr
		if( re.match( "http://www.pluzz.fr/[^\.]+?\.html", self.url ) ):
			# Recupere l'ID de l'emission
			self.getID()
			# Recupere la page d'infos de l'emission
			self.pageInfos = self.navigateur.getFichier( "http://www.pluzz.fr/appftv/webservices/video/getInfosOeuvre.php?mode=zeri&id-diffusion=%s" %( self.id ) )
			# Parse la page d'infos
			self.parseInfos()
			# Petit message en cas de DRM
			if( self.drm == "oui" ):
				logger.warning( "La vidéo posséde un DRM ; elle sera sans doute illisible" )
			# Verification qu'un lien existe
			if( self.m3u8URL is None and
				self.manifestURL is None and
				self.lienRTMP is None and
				self.lienMMS is None ):
				logger.critical( "Aucun lien vers la vidéo" )
				sys.exit( -1 )			
			# Telechargement de la video
			if( self.m3u8URL is not None ):
				# Nom du fichier
				self.nomFichier = os.path.join( self.outDir, "%s.mp4" %( re.findall( "http://www.pluzz.fr/([^\.]+?)\.html", self.url )[ 0 ] ) )
				# Downloader
				downloader = PluzzDLM3U8( self.m3u8URL, self.nomFichier, self.navigateur )
			elif( self.manifestURL is not None ):
				# Nom du fichier
				self.nomFichier = os.path.join( self.outDir, "%s.flv" %( re.findall( "http://www.pluzz.fr/([^\.]+?)\.html", self.url )[ 0 ] ) )
				# Downloader
				downloader = PluzzDLF4M( self.manifestURL, self.nomFichier, self.navigateur, self.stopDownloadEvent, self.progressFnct )
			elif( self.lienRTMP is not None ):
				# Downloader
				downloader = PluzzDLRTMP( self.lienRTMP )
			elif( self.lienMMS is not None ):
				# Downloader
				downloader = PluzzDLMMS( self.lienMMS )
			# Lance le téléchargement
			downloader.telecharger()

	def getID( self ):
		"""
		Recupere l'ID de la video
		"""
		try :
			page     = self.navigateur.getFichier( self.url )
			self.id  = re.findall( r"http://info.francetelevisions.fr/\?id-video=([^\"]+)", page )[ 0 ]
			logger.debug( "ID de l'émission : %s" %( self.id ) )
		except :
			logger.critical( "Impossible de récupérer l'ID de l'émission" )
			sys.exit( -1 )

	def parseInfos( self ):
		"""
		Parse le fichier qui contient les liens
		"""
		try : 
			xml.sax.parseString( self.pageInfos, PluzzDLInfosHandler( self ) )
			logger.debug( "Lien MMS : %s" %( self.lienMMS ) )
			logger.debug( "Lien RTMP : %s" %( self.lienRTMP ) )
			logger.debug( "URL manifest : %s" %( self.manifestURL ) )
			logger.debug( "URL m3u8 : %s" %( self.m3u8URL ) )
			logger.debug( "Utilisation de DRM : %s" %( self.drm ) )
		except :
			logger.critical( "Impossible de parser le fichier XML de l'émission" )
			sys.exit( -1 )

class PluzzDLM3U8( object ):
	"""
	Telechargement des liens m3u8
	"""
	
	def __init__( self, m3u8URL, nomFichier, navigateur ):
		self.m3u8URL    = m3u8URL
		self.nomFichier = nomFichier
		self.navigateur = navigateur
	
	def telecharger( self ):
		# Recupere le fichier master.m3u8
		self.m3u8 = self.navigateur.getFichier( self.m3u8URL )
		# Recupere le lien avec le plus gros bitrate (toujours 1205000 ?)
		try:
			self.listeFragmentsURL = re.findall( "http://ftvodhd-i\.akamaihd.net/.+?index_2_av\.m3u8.+", self.m3u8 )[ 0 ]
		except:
			logger.critical( "Impossible de trouver le lien vers la liste des fragments" )
			sys.exit( -1 )
		# Recupere la liste des fragments
		self.listeFragmentsPage = self.navigateur.getFichier( self.listeFragmentsURL )
		# Extrait l'URL de tous les fragments
		self.listeFragments = re.findall( "http://ftvodhd-i.akamaihd.net.+", self.listeFragmentsPage )
		# Ouvre le fichier
		try :
			# Ouverture du fichier
			self.fichierVideo = open( self.nomFichier, "wb" )
		except :
			logger.critical( "Impossible d'écrire dans le répertoire %s" %( os.getcwd() ) )
			sys.exit( -1 )
		# Charge tous les fragments
		for fragURL in self.listeFragments:
			frag = self.navigateur.getFichier( fragURL )
			self.fichierVideo.write( frag )
		# Fermeture du fichier
		self.fichierVideo.close()
	
class PluzzDLF4M( object ):
	"""
	Telechargement des liens f4m
	"""
	
	def __init__( self, manifestURL, nomFichier, navigateur, stopDownloadEvent ):
		self.manifestURL       = manifestURL
		self.nomFichier        = nomFichier
		self.navigateur        = navigateur
		self.stopDownloadEvent = stopDownloadEvent
		self.progressFnct      = progressFnct
		
		self.historique    = Historique()
		self.configuration = Configuration()
		self.hmacKey       = self.configuration[ "hmac_key" ].decode( "hex" )
		self.playerHash    = self.configuration[ "player_hash" ]
		
	def parseManifest( self ):
		"""
		Parse le manifest
		"""
		try :
			arbre          = xml.etree.ElementTree.fromstring( self.manifest )
			# Duree
			self.duree     = float( arbre.find( "{http://ns.adobe.com/f4m/1.0}duration" ).text )
			self.pv2       = arbre.find( "{http://ns.adobe.com/f4m/1.0}pv-2.0" ).text
			media          = arbre.findall( "{http://ns.adobe.com/f4m/1.0}media" )[ -1 ]
			# Bitrate
			self.bitrate   = int( media.attrib[ "bitrate" ] )
			# URL des fragments
			urlbootstrap   = media.attrib[ "url" ]
			self.urlFrag   = "%s%sSeg1-Frag" %( self.manifestURLToken[ : self.manifestURLToken.find( "manifest.f4m" ) ], urlbootstrap )
			# Header du fichier final
			self.flvHeader = base64.b64decode( media.find( "{http://ns.adobe.com/f4m/1.0}metadata" ).text )
		except :
			logger.critical( "Impossible de parser le manifest" )
			sys.exit( -1 )

	def ouvrirNouvelleVideo( self ):
		"""
		Creer une nouvelle video
		"""
		try :
			# Ouverture du fichier
			self.fichierVideo = open( self.nomFichier, "wb" )
		except :
			logger.critical( "Impossible d'écrire dans le répertoire %s" %( os.getcwd() ) )
			sys.exit( -1 )
		# Ajout de l'en-tête FLV
		self.fichierVideo.write( binascii.a2b_hex( "464c56010500000009000000001200010c00000000000000" ) )
		# Ajout de l'header du fichier
		self.fichierVideo.write( self.flvHeader )
		self.fichierVideo.write( binascii.a2b_hex( "00000000" ) ) # Padding pour avoir des blocs de 8
		
	def ouvrirVideoExistante( self ):
		"""
		Ouvre une video existante
		"""
		try :
			# Ouverture du fichier
			self.fichierVideo = open( self.nomFichier, "a+b" )
		except :
			logger.critical( "Impossible d'écrire dans le répertoire %s" %( os.getcwd() ) )
			sys.exit( -1 )

	def decompressSWF( self, swfData ):
		"""
		Decompresse un fichier swf
		"""
		# Adapted from :
		#    Prozacgod
		#    http://www.python-forum.org/pythonforum/viewtopic.php?f=2&t=14693
		if( type( swfData ) is str ):
			swfData = StringIO.StringIO( swfData )

		swfData.seek( 0, 0 )
		magic = swfData.read( 3 )

		if( magic == "CWS" ):
			return "FWS" + swfData.read( 5 ) + zlib.decompress( swfData.read() )
		else:
			return None

	def getPlayerHash( self ):
		"""
		Recupere le sha256 du player flash
		"""
		# Get SWF player
		playerData = self.navigateur.getFichier( "http://static.francetv.fr/players/Flash.H264/player.swf" )
		# Uncompress SWF player
		playerDataUncompress = self.decompressSWF( playerData )
		# Perform sha256 of uncompressed SWF player
		hashPlayer = hashlib.sha256( playerDataUncompress ).hexdigest()
		# Perform base64
		return base64.encodestring( hashPlayer.decode( 'hex' ) )

	def debutVideo( self, fragID, fragData ):
		"""
		Trouve le debut de la video dans un fragment
		"""
		# Skip fragment header
		start = fragData.find( "mdat" ) + 4
		# For all fragment (except frag1)
		if( fragID > 1 ):
			# Skip 2 FLV tags
			for dummy in range( 2 ):
				tagLen, = struct.unpack_from( ">L", fragData, start ) # Read 32 bits (big endian)
				tagLen &= 0x00ffffff                                  # Take the last 24 bits
				start  += tagLen + 11 + 4                             # 11 = tag header len ; 4 = tag footer len
		return start
	
	def telecharger( self ):
		# Verifie si le lien du manifest contient la chaine "media-secure"
		if( self.manifestURL.find( "media-secure" ) != -1 ):
			logger.critical( "pluzzdl ne sait pas encore gérer ce type de vidéo..." )
			sys.exit( 0 )
		# Lien du manifest (apres le token)
		self.manifestURLToken = self.navigateur.getFichier( "http://hdfauth.francetv.fr/esi/urltokengen2.html?url=%s" %( self.manifestURL[ self.manifestURL.find( "/z/" ) : ] ) )
		# Recupere le manifest
		self.manifest = self.navigateur.getFichier( self.manifestURLToken )
		# Parse le manifest
		self.parseManifest()
		# Calcul les elements
		self.hdnea = self.manifestURLToken[ self.manifestURLToken.find( "hdnea" ) : ]
		self.pv20, self.hdntl = self.pv2.split( ";" )
		self.pvtokenData = r"st=0000000000~exp=9999999999~acl=%2f%2a~data=" + self.pv20 + "!" + self.playerHash
		self.pvtoken = "pvtoken=%s~hmac=%s" %( urllib.quote( self.pvtokenData ), hmac.new( self.hmacKey, self.pvtokenData, hashlib.sha256 ).hexdigest() )
		
		#
		# Creation de la video
		#
		self.premierFragment    = 1
		self.telechargementFini = False
		
		video = self.historique.getVideo( self.urlFrag )
		# Si la video est dans l'historique
		if( video is not None ):
			# Si la video existe sur le disque
			if( os.path.exists( self.nomFichier ) ):
				if( video.finie ):
					logger.info( "La vidéo a déjà été entièrement téléchargée" )
					sys.exit( 0 )
				else:
					self.ouvrirVideoExistante()
					self.premierFragment = video.fragments
					logger.info( "Reprise du téléchargement de la vidéo au fragment %d" %( video.fragments ) )
			else:
				self.ouvrirNouvelleVideo()
				logger.info( "Impossible de reprendre le téléchargement de la vidéo, le fichier %s n'existe pas" %( self.nomFichier ) )
		else: # Si la video n'est pas dans l'historique
			self.ouvrirNouvelleVideo()
			
		# Calcul l'estimation du nombre de fragments
		self.nbFragMax = round( self.duree / 6 )
		logger.debug( "Estimation du nombre de fragments : %d" %( self.nbFragMax ) )
		
		# Ajout des fragments
		logger.info( "Début du téléchargement des fragments" )
		try :
			i = self.premierFragment
			while( not self.stopDownloadEvent.isSet() ):
				frag  = self.navigateur.getFichier( "%s%d?%s&%s&%s" %( self.urlFrag, i, self.pvtoken, self.hdntl, self.hdnea ) )
				debut = self.debutVideo( i, frag )
				self.fichierVideo.write( frag[ debut : ] )
				# Affichage de la progression
				self.progressFnct( min( int( ( i / self.nbFragMax ) * 100 ), 100 ) )
				i += 1
		except urllib2.URLError, e :
			if( hasattr( e, 'code' ) ):
				if( e.code == 403 ):
					if( e.reason == "Forbidden" ):
						logger.info( "Le hash du player semble invalide ; calcul du nouveau hash" )
						newPlayerHash = self.getPlayerHash()
						if( newPlayerHash != self.playerHash ):
							self.configuration[ "player_hash" ] = newPlayerHash
							self.configuration.writeConfig()
							logger.info( "Un nouveau hash a été trouvé ; essayez de relancer l'application" )
						else:
							logger.critical( "Pas de nouveau hash disponible..." )						
					else:
						logger.critical( "Impossible de charger la vidéo" )
				elif( e.code == 404 ):
					self.progressFnct( 100 )
					self.telechargementFini = True
					logger.info( "Fin du téléchargement" )
		except KeyboardInterrupt:
			logger.info( "Interruption clavier" )
		except:
			logger.critical( "Erreur inconnue" )
		finally :
			# Ajout dans l'historique
			self.historique.ajouter( Video( lien = self.urlFrag, fragments = i, finie = self.telechargementFini ) )
			# Fermeture du fichier
			self.fichierVideo.close()
	
class PluzzDLRTMP( object ):
	"""
	Telechargement des liens rtmp
	"""

	def __init__( self, lienRTMP ):
		self.lien = lienRTMP
	
	def telecharger( self ):
		logger.info( "Lien RTMP : %s\nUtiliser par exemple rtmpdump pour la recuperer directement" %( self.lien ) )
	
class PluzzDLMMS( object ):
	"""
	Telechargement des liens mms
	"""
	
	def __init__( self, lienMMS ):
		self.lien = lienMMS
	
	def telecharger( self ):
		logger.info( "Lien MMS : %s\nUtiliser par exemple mimms ou msdl pour la recuperer directement" %( self.lien ) )
	
class PluzzDLInfosHandler( xml.sax.handler.ContentHandler ):
	"""
	Handler pour parser le XML
	"""
	
	def __init__( self, pluzzdl ):
		self.pluzzdl = pluzzdl
		
		self.isUrl = False
		self.isDRM = False
		
	def startElement( self, name, attrs ):
		if( name == "url" ):
			self.isUrl = True
		elif( name == "drm" ):
			self.isDRM = True
	
	def characters( self, data ):
		if( self.isUrl ):
			if( data[ : 3 ] == "mms" ):
				self.pluzzdl.lienMMS = data
			elif( data[ : 4 ] == "rtmp" ):
				self.pluzzdl.lienRTMP = data
			elif( data[ -3 : ] == "f4m" ):
				self.pluzzdl.manifestURL = data
			elif( data[ -4 : ] == "m3u8" ):
				self.pluzzdl.m3u8URL = data
		elif( self.isDRM ):
			self.pluzzdl.drm = data
			
	def endElement( self, name ):
		if( name == "url" ):
			self.isUrl = False
		elif( name == "drm" ):
			self.isDRM = False
