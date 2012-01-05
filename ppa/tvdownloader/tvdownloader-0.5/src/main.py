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

#
# Entree du programme
#

if __name__ == "__main__" :	

	# On met en place les repertoires de travail du logiciel
	home = os.path.expanduser( "~" )
	repertoires = [ "/.tvdownloader/cache", \
					"/.tvdownloader/conf", \
					"/.tvdownloader/logs", \
					"/.tvdownloader/plugins", \
					"/TVDownloader" ]
	for repertoire in repertoires:
		rep = home + repertoire
		if( not os.path.isdir( rep ) ):
			print "Création du répertoire %s" %( rep )
			os.makedirs( rep )
	
	# On demarre le CLI ou le GUI ?
	if( len( sys.argv ) == 2 and sys.argv[ 1 ] == "no-gui" ):
		# On importe les fichiers necessaires a la CLI
		from CLI.cli import cli
		# On lance la CLI
		cli()
	else:
		# On importe les fichiers necessaires pour le GUI
		try:
			from PyQt4 import QtGui, QtCore
		except ImportError:
			print "Ouuupppss : il vous faut PyQt4 pour pouvoir utiliser ce programme..."
			sys.exit( 1 )
		
		from GUI.MainWindow import MainWindow
		
		# On creer l'interface graphique
		app = QtGui.QApplication( sys.argv )
		window = MainWindow()
		window.show()
		sys.exit( app.exec_() )
