#!/usr/bin/env python
# -*- coding:Utf-8 -*-


#
# Modules
#

import mechanize
import random
import urllib2
import sys


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
		
		# Navigateur
		self.navigateur = mechanize.Browser()
		
		#
		# Options du Navigateur
		#

		# User Agent + cookie connexion proxy
		self.navigateur.addheaders = [ ( 'User-agent', random.choice( listeUserAgents ) ) ]
		# 
		self.navigateur.set_handle_equiv( True )
		# Active compression gzip
		# self.navigateur.set_handle_gzip( True )
		# 
		self.navigateur.set_handle_redirect( True )
		# N'ajoute pas le referer a l'en-tete
		self.navigateur.set_handle_referer( True )
		# Ne prend pas en compte les robots.txt
		self.navigateur.set_handle_robots( False )
		# Ne doit pas gerer les cookies
		self.navigateur.set_cookiejar( None )
		# Utilise le proxy
		# self.navigateur.set_proxies( { 'http' : 'http://127.0.0.1:8000/' } )

	def getFichier( self, url ):
		try:
			page    = self.navigateur.open( url, timeout = self.timeOut )
			donnees = page.read()
			return donnees
		except urllib2.URLError, erreur:
			try:
				print erreur.reason
			except :
				pass
			sys.exit( 1 )
