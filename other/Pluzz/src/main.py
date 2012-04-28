#!/usr/bin/env python2
# -*- coding:Utf-8 -*-

#
# Infos
#

__author__  = "Chaoswizard"
__license__ = "GPL 2"
__version__ = "0.8"
__url__     = "http://code.google.com/p/tvdownloader/"

#
# Modules
#

import logging
import optparse
import platform
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
	parser.add_option( "--nocolor",           action = 'store_true', default = False, help = 'desactive la couleur dans le terminal' )
	parser.add_option( "-v", "--verbose",     action = "store_true", default = False, help = 'affiche les informations de debugage' )
	parser.add_option( "-b", "--progressbar", action = "store_true", default = False, help = 'affiche la progression du telechargement' )
	parser.add_option( "-f", "--fragments",   action = "store_true", default = False, help = 'telecharge la video via ses fragments meme si un lien direct existe' )
	parser.add_option( "-r", "--resume",      action = "store_true", default = False, help = 'essaye de reprendre un téléchargement interrompu' )
	parser.add_option( "-p", "--proxy", dest = "proxy", metavar = "PROXY",          help = 'utilise un proxy HTTP au format suivant http://URL:PORT' )
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
		logger.setLevel( logging.INFO )
		console.setLevel( logging.INFO )
	console.setFormatter( ColorFormatter( not options.nocolor ) )
	logger.addHandler( console )
	
	# Affiche la version de pluzzdl et de python
	logger.debug( "%s avec Python %s" %( version, platform.python_version() ) )
	
	# Verification de l'URL
	if( re.match( "http://www.pluzz.fr/[^\.]+?\.html", args[ 0 ] ) is None ):
		logger.error( "L'URL \"%s\" n'est pas valide" %( args[ 0 ] ) )
		sys.exit( -1 )
	
	# Verification du proxy
	if( options.proxy is not None and re.match( "http://[^:]+?:\d+", options.proxy ) is None ):
		logger.error( "Le proxy \"%s\" n'est pas valide" %( options.proxy ) )
		sys.exit( -1 )
	
	# Telechargement de la video
	PluzzDL( url          = args[ 0 ],
			 useFragments = options.fragments,
			 proxy        = options.proxy,
			 progressbar  = options.progressbar,
			 resume       = options.resume )
