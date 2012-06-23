#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import sys
sys.path.append( ".." ) 

from base.qt.qtString import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

from qt.QtIconsList import QtIconsList
from qt.QtTable     import QtTable

#
# Classe
#

class MainWindow( QtGui.QMainWindow ):
	"""
	TVDownloader MainWindows
	"""
	
	def __init__( self, tvdVersion ):
		"""
		Constructeur
		"""
		# Appel au constructeur de la classe mere
		QtGui.QMainWindow.__init__( self )
		
		#
		# Icones
		#
		
		self.tvdIco = QtGui.QIcon( "qt/ico/TVDownloader.png" )
		
		#
		# Reglages de la fenetre
		#
		
		# Nom de la fenetre
		self.setWindowTitle( "TVDownloader %s" %( tvdVersion ) )
		# Mise en place de son icone
		self.setWindowIcon( self.tvdIco )
		
		#
		# Widget central de la fenetre
		#
		
		# Widget central qui contiendra tout
		self.centralWidget = QtGui.QWidget( self )
		self.setCentralWidget( self.centralWidget )
		
		# Layout de grille pour le widget central
		self.centralGridLayout = QtGui.QGridLayout( self.centralWidget )
		
		#
		# Onglets
		#
		
		# Gestionnaire onglets
		self.tabWidget = QtGui.QTabWidget( self.centralWidget )
		self.centralGridLayout.addWidget( self.tabWidget, 0, 0, 1, 1 )
		
		# Onglet Fichiers
		self.fichiersSplitter = QtGui.QSplitter( self.centralWidget )
		self.tabWidget.addTab( self.fichiersSplitter, u"Choix des fichiers" )
		
		# Onglet Telechargements
		self.telechargementsWidget = QtGui.QWidget( self.centralWidget )
		self.tabWidget.addTab( self.telechargementsWidget, u"Téléchargements" )
		
		# Onglet Parametres
		self.parametresWidget = QtGui.QWidget( self.centralWidget )
		self.tabWidget.addTab( self.parametresWidget, u"Paramètres" )
		
		#
		# Onglet Fichiers
		#
		
		# Widget choix de la chaine
		self.chaineWidget = QtGui.QWidget( self.fichiersSplitter )
		self.fichiersSplitter.addWidget( self.chaineWidget )
		
		# Layout vertical
		self.chaineLayout = QtGui.QVBoxLayout( self.chaineWidget )
		
		# Choix du plugin
		self.pluginComboBox = QtGui.QComboBox( self.chaineWidget )
		self.chaineLayout.addWidget( self.pluginComboBox )
		
		# Liste des chaines
		self.chaineIconsList = QtIconsList( self.chaineWidget )
		self.chaineLayout.addWidget( self.chaineIconsList )
		
		# Widget choix des fichiers
		self.fichierWidget = QtGui.QWidget( self.fichiersSplitter )
		self.fichiersSplitter.addWidget( self.fichierWidget )
		
		# Layout vertical
		self.fichierLayout = QtGui.QVBoxLayout( self.fichierWidget )
		
		# Choix de l'emission
		self.emissionComboBox = QtGui.QComboBox( self.fichierWidget )
		self.fichierLayout.addWidget( self.emissionComboBox )
		
		# Liste des fichiers
		self.fichierTableWidget = QtTable( self.fichierWidget )
		self.fichierLayout.addWidget( self.fichierTableWidget )
	
	def closeEvent( self, evt ):
		"""
		Surcharge de la methode appele lors de la fermeture de la fenetre
		"""
		self.actionsAvantQuitter()
		evt.accept()
	
	def actionsAvantQuitter( self ):
		"""
		Actions a realiser avant de quitter le programme
		"""
		print "Bye bye"
		
	
	

if __name__ == "__main__" :
	app = QtGui.QApplication( sys.argv )
	window = MainWindow( "1.0" )
	window.show()
	sys.exit( app.exec_() )	
