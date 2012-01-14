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
	listeUserAgents = [ 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
						'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
						'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
						'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; fr-fr) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1',
						'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; fr; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3',
						'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
						'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1',
						'Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
						'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
						'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) midori',
						'Opera/8.50 (Windows NT 5.1; U; en)',
						'Opera/8.50 (Windows NT 5.1; U; en)',
						'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.2.15 Version/10.00' ]
	
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
