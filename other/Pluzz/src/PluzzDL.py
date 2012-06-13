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
	
	def __init__( self, url, useFragments = False, proxy = None, resume = False, progressFnct = lambda x : None, stopDownloadEvent = threading.Event() ):
		self.url               = url
		self.useFragments      = useFragments
		self.proxy             = proxy
		self.resume            = resume
		self.progressFnct      = progressFnct
		self.stopDownloadEvent = stopDownloadEvent
		self.navigateur        = Navigateur( self.proxy )
		self.historique        = Historique()
		self.configuration     = Configuration()
		self.lienMMS           = None
		self.lienRTMP          = None
		self.manifestURL       = None
		self.drm               = None
		
		self.hmacKey           = self.configuration[ "hmac_key" ].decode( "hex" )
		self.playerHash        = self.configuration[ "player_hash" ]
		
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
			# Lien MMS trouve
			if( self.lienMMS is not None ):
				logger.info( "Lien MMS : %s\nUtiliser par exemple mimms ou msdl pour la recuperer directement ou l'option -f de pluzzdl pour essayer de la charger via ses fragments" %( self.lienMMS ) )
			# Lien RTMP trouve
			if( self.lienRTMP is not None ):
				logger.info( "Lien RTMP : %s\nUtiliser par exemple rtmpdump pour la recuperer directement ou l'option -f de pluzzdl pour essayer de la charger via ses fragments" %( self.lienRTMP ) )
			# N'utilise pas les fragments si cela n'a pas ete demande et que des liens directs ont ete trouves
			if( ( ( self.lienMMS is not None ) or ( self.lienRTMP is not None ) ) and not self.useFragments ):
				sys.exit( 0 )
			# Lien du manifest non trouve
			if( self.manifestURL is None ):
				logger.critical( "Pas de lien vers le manifest" )
				sys.exit( -1 )
			self.nomFichier         = "%s.flv" %( re.findall( "http://www.pluzz.fr/([^\.]+?)\.html", self.url )[ 0 ] )
		else:
			page = self.navigateur.getFichier( self.url )
			try:
				self.manifestURL = re.findall( "(http://.+?manifest.f4m)", page )[ 0 ]
			except:
				logger.critical( "Pas de lien vers le manifest" )
				sys.exit( -1 )
			try:
				self.nomFichier         = "%s.flv" %( self.url.split( "/" )[ -1 ] )
			except:
				self.nomFichier = "video.flv"
			
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
		
		# S'il faut reprendre le telechargement
		if( self.resume ):
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
		else: # S'il ne faut pas reprendre le telechargement
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

	def getPlayerHash( self ):
		# Get SWF player
		playerData = self.navigateur.getFichier( "http://www.pluzz.fr/layoutftv/players/h264/player.swf" )
		# Uncompress SWF player
		playerDataUncompress = self.decompressSWF( playerData )
		# Perform sha256 of uncompressed SWF player
		hashPlayer = hashlib.sha256( playerDataUncompress ).hexdigest()
		# Perform base64
		return base64.encodestring( hashPlayer.decode( 'hex' ) )

	def decompressSWF( self, swfData ):
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

	def debutVideo( self, fragID, fragData ):
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
		
	def getID( self ):
		try :
			page     = self.navigateur.getFichier( self.url )
			self.id  = re.findall( r"http://info.francetelevisions.fr/\?id-video=([^\"]+)", page )[ 0 ]
			logger.debug( "ID de l'émission : %s" %( self.id ) )
		except :
			logger.critical( "Impossible de récupérer l'ID de l'émission" )
			sys.exit( -1 )
		
	def parseInfos( self ):
		try : 
			xml.sax.parseString( self.pageInfos, PluzzDLInfosHandler( self ) )
			logger.debug( "Lien MMS : %s" %( self.lienMMS ) )
			logger.debug( "Lien RTMP : %s" %( self.lienRTMP ) )
			logger.debug( "URL manifest : %s" %( self.manifestURL ) )
			logger.debug( "Utilisation de DRM : %s" %( self.drm ) )
		except :
			logger.critical( "Impossible de parser le fichier XML de l'émission" )
			sys.exit( -1 )
	
	def parseManifest( self ):
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
		try :
			# Ouverture du fichier
			self.fichierVideo = open( self.nomFichier, "a+b" )
		except :
			logger.critical( "Impossible d'écrire dans le répertoire %s" %( os.getcwd() ) )
			sys.exit( -1 )
		
class PluzzDLInfosHandler( xml.sax.handler.ContentHandler ):
	
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
		elif( self.isDRM ):
			self.pluzzdl.drm = data
			
	def endElement( self, name ):
		if( name == "url" ):
			self.isUrl = False
		elif( name == "drm" ):
			self.isDRM = False
