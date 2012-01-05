#!/usr/bin/env python2
# -*- coding:Utf-8 -*-

#
# Infos
#

__author__  = "Chaoswizard"
__license__ = "GPL 2"
__version__ = "0.1"
__url__     = "http://code.google.com/p/tvdownloader/"

#
# Modules
#

import logging
import optparse
import re
import sys

from ColorFormatter import ColorFormatter
from PluzzDL        import PluzzDL

#
# Main
#

if( __name__ == "__main__" ) :
	
	# Options de la ligne de commande
	usage   = "usage: pluzzdl [options] <url de l'emission>"
	version = "pluzzdl %s" %( __version__ )
	parser  = optparse.OptionParser( usage = usage, version = version )
	parser.add_option( "--nocolor",       action = 'store_true', default = False, help = 'desactive la couleur' )
	parser.add_option( "-v", "--verbose", action = "store_true", default = False, help = 'affiche des informations supplementaires' )
	( options, args ) = parser.parse_args()
	
	# Verification du nombre d'arguments
	if( len( args ) != 1 or args[ 0 ] == "" ):
		parser.print_help()
		parser.exit( 1 )
	
	# Mise en place du logger
	logger  = logging.getLogger( "pluzzdl" )
	console = logging.StreamHandler( sys.stdout )
	if( options.verbose ):
		logger.setLevel( logging.DEBUG )
		console.setLevel( logging.DEBUG )
	else:
		logger.setLevel( logging.ERROR )
		console.setLevel( logging.ERROR )
	console.setFormatter( ColorFormatter( not options.nocolor ) )
	logger.addHandler( console )
	
	# Verification de l'URL
	if( re.match( "http://www.pluzz.fr/[^\.]+?\.html", args[ 0 ] ) is None ):
		logger.error( "L'URL \"%s\" n'est pas valide" %( args[ 0 ] ) )
		sys.exit( -1 )
	
	# Telechargement de la video
	PluzzDL( args[ 0 ] )
