#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#



from APIPrive      import APIPrive
from base.Browser  import Browser
from base.Patterns import Singleton

import logging
logger = logging.getLogger( "tvdownloader" )

#
# Class
#

class API( APIPrive ):
	__metaclass__ = Singleton
	
	def __init__( self ):
		APIPrive.__init__( self )
		self.browser = Browser()

	## Récupère une page web
	# @param url  URL de la page
	# @param data POST data { name : value }
	# @return page web
	def getPage( self, url, data = None ):
		return self.browser.getFile( url, data )
	
	## Récupère plusieurs pages sur le web
	# @param urlListe  Liste des URLs [ ( url, data ) ]
	# @return pages web { ( url, data ) : page } 
	def getPages( self, urlListe ):
		return self.browser.getFiles( urlList )
