#!/usr/bin/env python
# -*- coding:Utf-8 -*-


#
# Modules
#

import cookielib
import random
import urllib2

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Classe
#

class Navigateur:
	
	timeOut   = 60
	listeUserAgents = [ 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; fr-fr) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1',
						'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1',
						'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
						'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) midori',
						'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.107 Safari/535.1',
						'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312',
						'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
						'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8' ]
	
	def __init__( self, proxy = None ):
		self.proxy = proxy
		
		# Cookiejar + urlopener
		self.cookiejar            = cookielib.CookieJar()
		if( proxy is None ):
			self.urlOpener        = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookiejar ) )
		else:
			self.urlOpener        = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookiejar ), urllib2.ProxyHandler( { 'http' : self.proxy } ) )
		# Spoof de l'user-agent
		self.urlOpener.addheaders = [ ( 'User-agent', random.choice( self.listeUserAgents ) ) ]		

	def getFichier( self, url ):
		try:
			logger.debug( "GET %s" %( url ) )
			
			# Modif à la con du cookie >< !
			for cookie in self.cookiejar:
				if( cookie.name == "hdntl" and cookie.value.find( "PV-IDENT" ) == -1 ):
					cookie.value += "; PV-IDENT=exp=1330022391~acl=%2f*~hmac=66cbe2c1a63657297bd537b393263d3ebb06980089188e9013690390b6f8da3b"
			
			requete = urllib2.Request( url )
			page    = self.urlOpener.open( requete, timeout = self.timeOut )
			donnees = page.read()
			return donnees
		except urllib2.URLError, e :
			if( hasattr( e, 'reason' ) ):
				logger.debug( e.reason )
			elif( hasattr( e, 'code' ) ):
				logger.debug( "Erreur %d" %( e.code ) )
			raise
