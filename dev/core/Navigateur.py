#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier COPYING #
#########################################

# Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
# Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
# Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import urllib
import urllib2
import mechanize

import random
import re
import threading
import time

import xml.sax.saxutils

import logging
logger = logging.getLogger( __name__ )

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

##########
# Classe #
##########

## Classe Navigateur pour charger les pages web
class Navigateur( object ):
	
	timeOut   = 5
	maxThread = 10
	
	## Constructeur
	def __init__( self ):
		
		# Navigateur
		self.navigateur = mechanize.Browser()
		
		#
		# Options du Navigateur
		#

		# User Agent
		self.navigateur.addheaders = [ ('User-agent', random.choice( listeUserAgents ) ) ]
		# 
		self.navigateur.set_handle_equiv( True )
		# Active compression gzip
		#~ self.navigateur.set_handle_gzip( True )
		# 
		self.navigateur.set_handle_redirect( True )
		# N'ajoute pas le referer a l'en-tete
		self.navigateur.set_handle_referer( False )
		# Ne prend pas en compte les robots.txt
		self.navigateur.set_handle_robots( False )
		# Ne doit pas gerer les cookies
		self.navigateur.set_cookiejar( None )
		
	## Methode pour recuperer une page web
	# @param  URLPage URL de la page web a charger
	# @return Code de la page
	def getPage( self, URLPage ):
		logger.info( "acces a la page %s" %( URLPage ) )
		try:
			# Page a charger
			page = self.navigateur.open( URLPage, timeout = self.timeOut )			
			
			# Si le fichier est un XML
			if( URLPage[ -4 : ] == ".xml" ):
				# On la page telle quelle, sans aucun traitement
				return page.read()
			else: # Sinon, on va cherche a determiner son encodage
				
				# Donnees de la page
				donnees = self.unescape( page.read() )
				
				# On recupere si possible l'encodage de la page
				contentType = page.info()[ "Content-type" ]
				# Type d'encodage de la page
				encodagePage = ""
				# On extrait l'encodage
				res = re.findall( "charset=(.+)", contentType )
				if( len( res ) != 0 ):
					encodagePage = res[ 0 ].lower()
				
				# Si on a trouve un encodage et qui n'est pas de l'utf-8
				if( encodagePage != "" and encodagePage != "utf-8" ):
					# On retourne la page dans le bon encodage
					return unicode( donnees, encodagePage ).encode( 'utf-8', 'replace' )
				else:
					return donnees
		except urllib2.URLError, erreur:
			try:
				logger.error( erreur.reason )
			except :
				pass
			return ""
		except:
			return ""
	
	## Methode pour recuperer plusieurs pages web
	# @param listeURL Liste des URLs des pages web a charger
	# @return         La liste (dictionnaire) des pages web recuperees { URLPage : Page }
	def getPages( self, listeURL ):
		## Sous methode qui gere le telechargement d'une page (thread)
		# @param URLPage   URL de la page a charger
		def ajoutPage( self, URLPage ):
			# On a un thread lance de plus
			self.lock.acquire()
			self.nbThreadLances += 1
			self.lock.release()
			
			# On recupere la page web
			try:
				page = self.getPage( URLPage )
			except:
				page = ""
			#~ print "DL de %s fini" %( URLPage )
			
			# On ajoute la page a la liste et on a un thread lance de moins
			self.lock.acquire()
			self.listePage[ URLPage ] = page
			self.nbThreadLances -= 1
			self.lock.release()
			
		self.listePage      = {}
		self.nbThreadLances = 0
		indiceActuelListe   = 0
		tailleListe         = len( listeURL )
		self.lock           = threading.Lock()
		
		# Boucle pour lancer les threads
		self.lock.acquire()
		while( indiceActuelListe < tailleListe ): # Tant qu'on a pas fini de parcourir la liste
			if( self.nbThreadLances < self.maxThread ): # Si on peut encore lance des threads
				#~ print "Indice = %d" %( indiceActuelListe )
				self.lock.release()
				# On en lance un
				threading.Thread( target = ajoutPage, 
								  args = ( self, listeURL[ indiceActuelListe ] ) 
								).start()
				indiceActuelListe += 1
				#~ self.lock.release()
				#~ time.sleep( 0.01 ) # Legere attente pour que le thread ait le temps d'incrementer le nombre de threads lances
			else: # Sinon,
				# On attend un peu avant de reessayer
				self.lock.release()
				time.sleep( 0.1 )
			#~ print self.nbThreadLances
			self.lock.acquire()
		self.lock.release()
		
		# Boucle pour attendre la fin de tous les threads
		self.lock.acquire()
		while( self.nbThreadLances > 0 ): # Si des threads ne sont pas finis
			#~ print self.nbThreadLances
			# On attend un peu
			self.lock.release()
			time.sleep( 0.1 )
			self.lock.acquire()
		self.lock.release()
		
		return self.listePage
	
	## Methode pour recuperer une image
	# @param  URLPicture URL de l'image a charger
	# @return les données de l'image
	def getPicture( self, URLPicture ):
		logger.info( "acces a l'image %s" %( URLPicture ) )
		try:
			# Image a charger
			page = self.navigateur.open( URLPicture, timeout = self.timeOut )
			
			# Donnees de l'image
			donnees = page.read()
			
			return donnees
		except urllib2.URLError, erreur:
			try:
				logger.error( erreur.reason )
			except :
				pass
			return ""

	def unescape( self, texte ):
		#~ def ent2chr( m ):
			#~ code = m.group( 1 )
			#~ if( code.isdigit() ): 
				#~ code = int( code )
			#~ else:
				#~ code = int( code[ 1 : ], 16 )
			#~ if( code < 256 ): 
				#~ return chr( code )
			#~ else: 
				#~ return '?'
#~ 
		#~ texte = texte.replace( "&lt;", "<" )
		#~ texte = texte.replace( "&gt;", ">" )
		#~ texte = texte.replace( "&amp;", "&" )
		#~ texte = texte.replace( "&#034;", '"' )
		#~ texte = texte.replace( "&#039;", "'" )
		#~ texte = re.sub( r'\&\#(x?[0-9a-fA-F]+);', ent2chr, texte )
		return xml.sax.saxutils.unescape( texte )
	
