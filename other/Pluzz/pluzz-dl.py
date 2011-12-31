#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import base64
import binascii
import re
import xml.etree.ElementTree as xml

from Navigateur import Navigateur

#
# Classe
#

class PluzzDL( object ):
	
	def __init__( self, url ):
		self.url        = url
		self.navigateur = Navigateur()
		
		# Recupere l'ID de l'emission
		self.id                 = self.getID()
		# Recupere l'URL du manifest
		self.manifestURL        = self.getManifestURL()
		# Lien reduit du manifest
		self.manifestURLReduite = self.manifestURL[ self.manifestURL.find( "/z/" ) : ]
		# Recupere le manifest
		self.manifest           = self.getManifest()
		
		#
		# Extrait les infos du manifest
		#
		arbre  = xml.fromstring( self.manifest )
		
		# BootstrapInfo
		self.bootstrapInfo = base64.b64decode( arbre.findall( "{http://ns.adobe.com/f4m/1.0}bootstrapInfo" )[ 2 ].text )
		# URL des fragments
		media        = arbre.findall( "{http://ns.adobe.com/f4m/1.0}media" )[ 2 ]
		urlbootstrap = media.attrib[ "url" ]
		self.urlFrag = "%s%sSeg1-Frag" %( self.manifestURL[ : -12 ], urlbootstrap )
		# Header du fichier final
		self.flvHeader = base64.b64decode( media.find( "{http://ns.adobe.com/f4m/1.0}metadata" ).text )
		
		#
		# Creation de la video
		#
		
		# Ouverture du fichier
		self.fichierVideo = open( "video.flv", "wb" )
		# Ajout de l'en-tête FLV
		self.fichierVideo.write( binascii.a2b_hex( "464c56010500000009000000001200010c00000000000000" ) )
		# Ajout de l'header du fichier
		self.fichierVideo.write( self.flvHeader )
		self.fichierVideo.write( binascii.a2b_hex( "00000000" ) ) # Padding pour avoir des blocs de 8
		
		# Ajout des fragments
		for i in xrange( 1, 100 ):
			print "Frag %d" % ( i )
			frag = self.navigateur.getFichier( "%s%d" %( self.urlFrag, i ) )
			self.fichierVideo.write( frag[ len( self.bootstrapInfo ) + 60 : ] )
		
		# Fermeture du fichier
		self.fichierVideo.close()
		
		
	def getID( self ):
		page = self.navigateur.getFichier( self.url )
		res  = re.findall( r"http://info.francetelevisions.fr/\?id-video=(\d+)", page )
		assert( len( res ) >= 1 )
		return res[ 0 ]
	
	def getManifestURL( self ):
		page = self.navigateur.getFichier( "http://www.pluzz.fr/appftv/webservices/video/getInfosOeuvre.php?mode=zeri&id-diffusion=%s" %( self.id ) )
		res  = re.findall( r"(http://[^\[]+manifest.f4m)", page )
		assert( len( res ) >= 1 )
		return res[ 0 ]
		
	def getManifest( self ):
		lien = self.navigateur.getFichier( "http://hdfauth.francetv.fr/esi/urltokengen2.html?url=%s" %( self.manifestURLReduite ) )
		return self.navigateur.getFichier( lien )

#
# Entree du programme
#

if( __name__ == "__main__" ) :
	
	PluzzDL( "http://www.pluzz.fr/rani-2011-12-28-21h35.html" )
