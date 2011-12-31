#!/usr/bin/env python
# -*- coding:Utf-8 -*-


#
# Modules
#

import cookielib
import random
import sys
import urllib2


#
# Liste d'user agent
#

listeUserAgents = [ 'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
					'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
					'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; fr; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2',
					'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2) Gecko/20100115 Firefox/3.6',
					'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
					'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
					'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) midori',
					'Opera/8.50 (Windows NT 5.1; U; en)',
					'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.2.15 Version/10.00',
					'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312' ]


#
# Classe
#

class Navigateur:
	
	timeOut   = 60
	
	def __init__( self ):
		
		# Cookiejar + urlopener
		self.cookiejar            = cookielib.CookieJar()
		self.urlOpener            = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookiejar ) )
		# Spoof de l'user-agent
		self.urlOpener.addheaders = [ ( 'User-agent', random.choice( listeUserAgents ) ) ]		

	def getFichier( self, url ):
		try:
			print "--> Recuperation de la page %s" %( url )
		
			requete = urllib2.Request( url )
			page    = self.urlOpener.open( requete, timeout = self.timeOut )
			donnees = page.read()
			
			for co in self.cookiejar:
				print "Cookie : nom = %s ; valeur = %s" %( co.name, co.value )
			
			return donnees
		except urllib2.URLError, erreur:
			try:
				print erreur.reason
			except :
				pass
			print "!!! Erreur lors de la recuperation de la page %s !!!" %( url )
			sys.exit( 1 )
	
	# def has_cookie( self, name ):
		# has = False
		# for c in self.cookiejar:
			# if( c.name == name ):
				# has = True
				# break
		# return has
