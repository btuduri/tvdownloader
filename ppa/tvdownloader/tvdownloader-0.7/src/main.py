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

import sys
import os
import optparse
import logging

#
# Entree du programme
#

if __name__ == "__main__" :	
	
	# On se deplace dans le repertoire de travail du logciel
	repertoireTravail = os.path.dirname( os.path.abspath( __file__ ) )
	sys.path.insert( 0, repertoireTravail )
	os.chdir( repertoireTravail )
	
	# Options a parser
	parser = optparse.OptionParser()
	parser.add_option( "-v", "--verbose",
					   action = "store_true", dest = "verbose", default = False,
					   help = "Affiche informations dans le terminal" )
	parser.add_option( "-c", "--cli",
					   action = "store_true", dest = "cli", default = False,
					   help = "Affiche la version CLI" )
	parser.add_option( "-d", "--dialog",
					   action = "store_true", dest = "dialog", default = False,
					   help = u"Affiche la version Dialog (en cours de développement)" )
	parser.add_option( "-g", "--genererXML",
					   action = "store_true", dest = "genererXML", default = False,
					   help = u"Génère le fichier XML qui decrit les plugins" )
	options, args = parser.parse_args()
	
	# On a active le mode verbeux ?
	logger  = logging.getLogger( "" )
	console = logging.StreamHandler( sys.stdout )
	if( options.verbose ):
		logger.setLevel( logging.DEBUG )
		console.setLevel( logging.DEBUG )
	else:
		logger.setLevel( logging.ERROR )
		console.setLevel( logging.ERROR )
	console.setFormatter( logging.Formatter( '%(levelname)-7s %(name)s : %(message)s' ) )
	logger.addHandler( console )
	
	# On veut generer le fichier XML qui decrit les plugins
	if( options.genererXML ):
		import UpdateManager
		UpdateManager.UpdateManager.creerXML()
		sys.exit( 0 )
	
	# On met en place les repertoires de travail du logiciel
	home = os.path.expanduser( "~" )
	repertoires = [ "/.tvdownloader/cache", \
					"/.tvdownloader/conf", \
					"/.tvdownloader/logs", \
					"/.tvdownloader/plugins" ]
	for repertoire in repertoires:
		rep = home + repertoire
		if( not os.path.isdir( rep ) ):
			logger.info( "création du répertoire %s" %( rep ) )
			os.makedirs( rep )
	
	# On demarre le CLI ou le GUI ?
	if( options.cli == False and options.dialog == False ):
		# On importe les fichiers necessaires pour le GUI
		try:
			from PyQt4 import QtGui, QtCore
		except ImportError:
			logger.critical( "ouuupppss : il vous faut PyQt4 pour pouvoir utiliser ce programme..." )
			sys.exit( 1 )
		
		from GUI.MainWindow import MainWindow
		
		# On creer l'interface graphique
		app = QtGui.QApplication( sys.argv )
		window = MainWindow()
		window.show()
		sys.exit( app.exec_() )
	elif( options.cli == True ):
		from CLI.cli import cli
		cli()				
	else:
		from CLIDialog.CLIDialog import CLIDialog
		CLIDialog()
	