#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import cookielib
import random
import threading
import urllib2

from Cache import Cache

import logging
logger = logging.getLogger( "pluzzdl" )

#
# Classe
#

class Navigateur( object ):
	
	timeOut        = 60
	maxThread      = 10
	userAgentsList = [ 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; fr-fr) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1',
					   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1',
					   'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
					   'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) midori',
					   'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.107 Safari/535.1',
					   'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312',
					   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
					   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8' ]
	instance = None
	
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( Navigateur, self ).__new__( self )
		return self.instance	
	
	def __init__( self, proxy = None ):
		# HTTP proxy
		self.proxy = proxy
		# Cookiejar + urlopener
		self.cookiejar            = cookielib.CookieJar()
		if( proxy is None ):
			self.urlOpener        = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookiejar ) )
		else:
			self.urlOpener        = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookiejar ), urllib2.ProxyHandler( { 'http' : self.proxy } ) )
		# User-agent
		self.urlOpener.addheaders = [ ( 'User-agent', random.choice( self.userAgentsList ) ) ]
		
		# Lock for threads
		self.lock                 = threading.Lock()
		# Semaphore
		self.semaphore            = threading.Semaphore( self.maxThread )
		# Condition "no thread running"
		self.noThreadRunning      = threading.Condition()
		# Number of running threads
		self.runningThreads       = 0
	
	@Cache( maxSize = 10 * 1024 * 1024, acceptedTypes = [ "text", "image" ] )
	def getFile( self, url ):
		try:
			logger.debug( "GET %s" %( url ) )
			request = urllib2.Request( url )
			page    = self.urlOpener.open( request, timeout = self.timeOut )
			data = page.read()
			return data
		except urllib2.URLError, e :
			if( hasattr( e, 'reason' ) ):
				logger.debug( e.reason )
			elif( hasattr( e, 'code' ) ):
				logger.debug( "Erreur %d" %( e.code ) )
			raise
		except:
			raise
	
	## Use threads to download several files
	# @param  urlList URL list [ url1, url2, ... ]
	# @return dictionnary { url1 : data1, url2 : data2, ... }
	def getFiles( self, urlList ):
		
		def threadGetFile( self, url ):
			# Thread += 1
			with self.lock:
				self.runningThreads += 1
			# Get data
			data = self.getFile( url )
			# Save data and thread -= 1
			with self.lock:
				self.filesData[ url ] = data
				self.runningThreads -= 1
				with self.noThreadRunning:
					if( self.runningThreads == 0 ):
						self.noThreadRunning.notify()	
			self.semaphore.release()
		
		self.filesData = {}
		currentFile    = 0
		
		if( len( urlList ) == 0 ):
			return self.filesData
		
		# Launch threads
		while( currentFile < len( urlList ) ):
			self.semaphore.acquire()
			threading.Thread( target = threadGetFile, 
							  args = ( self, urlList[ currentFile ] ) 
							).start()
			currentFile += 1
		
		# Wait the end of all threads
		with self.noThreadRunning:
			self.noThreadRunning.wait()
		
		return self.filesData
				
	def appendCookie( self, cookieName, cookieValue ):
		for cookie in self.cookiejar:
			if( cookie.name == cookieName ):
				cookie.value += "; %s" %( cookieValue )
				break
