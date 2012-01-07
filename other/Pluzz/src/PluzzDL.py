#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import base64
import binascii
import os
import re
import sys
import xml.etree.ElementTree as xml

from Navigateur import Navigateur

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Classe
#

class PluzzDL( object ):
	
	def __init__( self, url, useFragments, proxy ):
		self.url          = url
		self.useFragments = useFragments
		self.proxy        = proxy
		self.navigateur   = Navigateur( self.proxy )
		
		# Recupere l'ID de l'emission
		self.id = self.getID()
		# Recupere le lien direct et le lien du manifest
		( self.lienDirect, self.manifestURL ) = self.getLiens()
		# Lien direct trouve
		if( self.lienDirect is not None ):
				logger.info( "Lien direct de la vidéo : %s\nUtiliser par exemple mimms ou msdl pour la récupérer directement ou l'option -f de pluzzdl pour essayer de la charger via ses fragments" %( self.lienDirect ) )
				if( not self.useFragments ):
					sys.exit( 0 )
		
		#
		# Utilisation du manifest
		#
		
		# Lien du manifest non trouve
		if( self.manifestURL is None ):
			logger.critical( "Pas de lien vers le manifest" )
			sys.exit( -1 )
		
		# Lien reduit du manifest
		self.manifestURLReduite = self.manifestURL[ self.manifestURL.find( "/z/" ) : ]
		# Recupere le manifest
		self.manifest = self.getManifest()
		logger.debug( "Manifest récupéré" )
		
		#
		# Extrait les infos du manifest
		#
		try :
			arbre  = xml.fromstring( self.manifest )
			# URL des fragments
			media        = arbre.findall( "{http://ns.adobe.com/f4m/1.0}media" )[ -1 ]
			urlbootstrap = media.attrib[ "url" ]
			self.urlFrag = "%s%sSeg1-Frag" %( self.manifestURL[ : -12 ], urlbootstrap )
			# Header du fichier final
			self.flvHeader = base64.b64decode( media.find( "{http://ns.adobe.com/f4m/1.0}metadata" ).text )
			# Fin
			logger.debug( "Fin d'extraction des informations du manifest" )
		except :
			logger.critical( "Erreur lors du parsing du manifest" )
			sys.exit( -1 )
		
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
		except :
			pass
		else :
			# Fermeture du fichier
			self.fichierVideo.close()
		
	def getID( self ):
		try :
			page = self.navigateur.getFichier( self.url )
			res  = re.findall( r"http://info.francetelevisions.fr/\?id-video=([^\"]+)", page )[ 0 ]
			logger.debug( "ID de l'émission = %s" %( res ) )
		except :
			logger.critical( "Impossible de récupérer l'ID de l'émission" )
			sys.exit( -1 )
		return res
	
	def getLiens( self ):
		page = self.navigateur.getFichier( "http://www.pluzz.fr/appftv/webservices/video/getInfosOeuvre.php?mode=zeri&id-diffusion=%s" %( self.id ) )
		# Lien direct
		try :
			lienDirect = re.findall( r"(mms://[^\]]+\.wmv)", page )[ 0 ]
			logger.debug( "URL directe = %s" %( lienDirect ) )
		except :
			lienDirect = None
			logger.debug( "Pas de lien direct vers la vidéo" )
		# Lien du manifest	
		try :
			lienManifest = re.findall( r"(http://[^\]]+manifest\.f4m)", page )[ 0 ]
			logger.debug( "URL manifest = %s" %( lienManifest ) )
		except :
			lienManifest = None
			logger.debug( "Pas de lien vers le manifest" )
		# Test
		if( lienDirect is None and lienManifest is None ): # Aucun lien trouve
			logger.critical( "Aucun lien disponible pour charger la vidéo" )
			sys.exit( -1 )
		return ( lienDirect, lienManifest )
		
	def getManifest( self ):
		lien = self.navigateur.getFichier( "http://hdfauth.francetv.fr/esi/urltokengen2.html?url=%s" %( self.manifestURLReduite ) )
		return self.navigateur.getFichier( lien )
