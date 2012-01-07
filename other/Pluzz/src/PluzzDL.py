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
		self.proxy        = proxy
		self.navigateur   = Navigateur( self.proxy )
		self.useFragments = useFragments
		
		# Recupere l'ID de l'emission
		self.id = self.getID()
		logger.debug( "ID de l'emission = %s" %( self.id ) )
		# Recupere la page d'info de l'emission
		page = self.navigateur.getFichier( "http://www.pluzz.fr/appftv/webservices/video/getInfosOeuvre.php?mode=zeri&id-diffusion=%s" %( self.id ) )
		# Tente de recuperer l'URL directe de la video
		self.lienDirect = False
		res             = re.findall( r"(mms://[^\]]+\.wmv)", page )
		if( len( res ) > 0 ): # Lien direct
			logger.info( "Lien direct vers la video : %s \n Utiliser par exemple mimms ou msdl pour la récuperer" %( res[ 0 ] ) )
			self.lienDirect = True
		else:
			logger.debug( "Pas de lien direct vers la vidéo" )
		if( not self.useFragments and self.lienDirect ):
			sys.exit( 0 )
		# Tente de recuperer l'URL du manifest
		res = re.findall( r"(http://[^\]]+manifest\.f4m)", page )
		if( len( res ) > 0 ): # Lien manifest
			self.manifestURL = res[ 0 ]
			logger.debug( "URL du manifest = %s" %( self.manifestURL ) )
		else:
			logger.critical( "Impossible de recuperer l'URL du manifest" )
			sys.exit( -1 )
		# Lien reduit du manifest
		self.manifestURLReduite = self.manifestURL[ self.manifestURL.find( "/z/" ) : ]
		# Recupere le manifest
		self.manifest = self.getManifest()
		logger.debug( "Manifest recupere" )
		
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
			logger.critical( "Impossible d'ecrire dans le repertoire %s" %( os.getcwd() ) )
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
		except :
			logger.critical( "Impossible de recuperer l'ID de l'emission" )
			sys.exit( -1 )
		return res
		
	def getManifest( self ):
		lien = self.navigateur.getFichier( "http://hdfauth.francetv.fr/esi/urltokengen2.html?url=%s" %( self.manifestURLReduite ) )
		return self.navigateur.getFichier( lien )
