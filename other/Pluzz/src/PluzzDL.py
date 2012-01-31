#!/usr/bin/env python
# -*- coding:Utf-8 -*-

# Notes :
#    -> Filtre Wireshark : 
#          http.host == "ftvodhdsecz2-f.akamaihd.net" or http.host == "ftvodhdsecz-f.akamaihd.net" or http.host == "hdfauth.francetv.fr" or http.host == "www.pluzz.fr"
#    -> 

#
# Modules
#

import base64
import binascii
import os
import re
import sys
import urllib2
import xml.etree.ElementTree
import xml.sax
from   xml.sax.handler import ContentHandler

from Navigateur import Navigateur

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Classes
#

class PluzzDL( object ):
	
	def __init__( self, url, useFragments, proxy ):
		self.url              = url
		self.useFragments     = useFragments
		self.proxy            = proxy
		self.navigateur       = Navigateur( self.proxy )
		
		self.lienMMS          = None
		self.lienRTMP         = None
		self.manifestURL      = None
		self.drm              = None
		
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
		# Lien du manifest (apres le token)
		self.manifestURLToken = self.navigateur.getFichier( "http://hdfauth.francetv.fr/esi/urltokengen2.html?url=%s" %( self.manifestURL[ self.manifestURL.find( "/z/" ) : ] ) )
		# Recupere le manifest
		self.manifest = self.navigateur.getFichier( self.manifestURLToken )
		# Parse le manifest
		self.parseManifest()
		#
		# Creation de la video
		#
		self.nomFichier   = "%s.flv" %( re.findall( "http://www.pluzz.fr/([^\.]+?)\.html", self.url )[ 0 ] )
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
		# Ajout des fragments
		logger.info( "Début du téléchargement des fragments" )
		try :
			frag = self.navigateur.getFichier( "%s1" %( self.urlFrag ) )
			self.fichierVideo.write( frag[ frag.find( "mdat" ) + 4 : ] )
			for i in xrange( 2, 99999 ):
				frag = self.navigateur.getFichier( "%s%d" %( self.urlFrag, i ) )
				self.fichierVideo.write( frag[ frag.find( "mdat" ) + 79 : ] )
		except urllib2.URLError, e :
			if( hasattr( e, 'code' ) ):
				if( e.code == 403 ):
					logger.critical( "Impossible de charger la vidéo" )
				elif( e.code == 404 ):
					logger.info( "Fin du téléchargement" )
		else :
			# Fermeture du fichier
			self.fichierVideo.close()
		
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
			arbre  = xml.etree.ElementTree.fromstring( self.manifest )
			# URL des fragments
			media        = arbre.findall( "{http://ns.adobe.com/f4m/1.0}media" )[ -1 ]
			urlbootstrap = media.attrib[ "url" ]
			self.urlFrag = "%s%sSeg1-Frag" %( self.manifestURLToken[ : self.manifestURLToken.find( "manifest.f4m" ) ], urlbootstrap )
			# Header du fichier final
			self.flvHeader = base64.b64decode( media.find( "{http://ns.adobe.com/f4m/1.0}metadata" ).text )
		except :
			logger.critical( "Impossible de parser le manifest" )
			sys.exit( -1 )	
		
class PluzzDLInfosHandler( ContentHandler ):
	
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
