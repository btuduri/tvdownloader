#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import operator
import threading

import sys
sys.path.append( ".." ) 

from base.qt.qtString import qstringToString
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
		
		self.tvdIco   = QtGui.QIcon( "qt/ico/TVDownloader.png" )
		# self.addIco   = QtGui.QIcon( "qt/ico/gtk-add.svg" )
		# self.applyIco = QtGui.QIcon( "qt/ico/gtk-apply.svg" )
		# self.fileIco  = QtGui.QIcon( "qt/ico/gtk-file.svg" )
		
		#
		# Signaux
		#
		
		# Liste des plugins a mettre en place
		self.listePluginsSignal = QtCore.SIGNAL( "listePlugins(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listePluginsSignal , self.ajouterPlugins )
		
		# Liste des chaines a mettre en place
		self.listeChainesSignal = QtCore.SIGNAL( "listeChaines(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listeChainesSignal , self.ajouterChaines )
		
		# Liste des emissions a mettre en place
		self.listeEmissionsSignal = QtCore.SIGNAL( "listeEmission(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listeEmissionsSignal , self.ajouterEmissions )
		
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
		QtCore.QObject.connect( self.pluginComboBox,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerChaines )
		self.chaineLayout.addWidget( self.pluginComboBox )
		
		# Liste des chaines
		self.chaineIconsList = QtIconsList( self.chaineWidget )
		QtCore.QObject.connect( self.chaineIconsList,
								QtCore.SIGNAL( "buttonClicked(PyQt_PyObject)" ),
								self.listerEmissions )
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
		self.fichierTableWidget.setColumnCount( 3 ) # 3 colonnes
		self.fichierTableWidget.setRowCount( 0 )    # 0 ligne
		self.fichierTableWidget.setHorizontalHeaderItem( 0, self.fichierTableWidget.createItem( "" ) )
		self.fichierTableWidget.setHorizontalHeaderItem( 1, self.fichierTableWidget.createItem( "Date" ) )
		self.fichierTableWidget.setHorizontalHeaderItem( 2, self.fichierTableWidget.createItem( "Emission" ) )
		self.fichierLayout.addWidget( self.fichierTableWidget )
		
		#
		# Debut
		#
		
		self.actionsAuDebut()
		
	def closeEvent( self, evt ):
		"""
		Surcharge de la methode appele lors de la fermeture de la fenetre
		"""
		self.actionsAvantQuitter()
		evt.accept()
	
	def actionsAuDebut( self ):
		"""
		Actions a realiser au demarage du programe
		"""
		self.listerPlugins()
	
	def actionsAvantQuitter( self ):
		"""
		Actions a realiser avant de quitter le programme
		"""
		print "Bye bye"
		
	def listerPlugins( self ):
		"""
		Fonction qui demande la liste des plugins
		"""
		def threadListerPlugins( self ):
			listePlugins = [ "B", "A", "C", "D" ]
			self.emit( self.listePluginsSignal, listePlugins )
		
		threading.Thread( target = threadListerPlugins, args = ( self, ) ).start()
	
	def listerChaines( self, plugin = None ):
		"""
		Fonction qui demande la liste des chaines d'un plugin donne
		Si plugin = None, alors elle demande la liste des chaines de tous les plugins
		"""
		def threadListerChaines( self, plugin ):
			listeChaines = [ ( "4", None ), ( "2", None ), ( "3", None ), ( "1", None ), ( "0", None ), ( "42", None ) ]
			self.emit( self.listeChainesSignal, listeChaines )
		
		if( plugin ):
			plugin = qstringToString( plugin )
		threading.Thread( target = threadListerChaines, args = ( self, plugin ) ).start()

	def listerEmissions( self, chaine ):
		"""
		Fonction qui demande la liste des emissions d'une chaine donnee
		"""
		def threadListerEmissions( self, chaine ):
			listeEmissions = [ "Alpha", "Beta", "Gamma" ]
			self.emit( self.listeEmissionsSignal, listeEmissions )

		threading.Thread( target = threadListerEmissions, args = ( self, chaine ) ).start()
		
	def ajouterPlugins( self, listePlugins ):
		"""
		Met en place la liste des plugins donnee
		"""
		listePlugins.sort()
		self.pluginComboBox.clear()
		map( lambda x : self.pluginComboBox.addItem( stringToQstring( x ) ), listePlugins )
	
	def ajouterChaines( self, listeChaines ):
		"""
		Met en place la liste des chaines donnee sous la forme ( nomChaine, logoChaine )
		"""
		listeChaines = sorted( listeChaines, key = operator.itemgetter( 0 ) )
		self.chaineIconsList.clear()
		map( lambda ( x, y ) : self.chaineIconsList.addIcon( x, y ), listeChaines )

	def ajouterEmissions( self, listeEmissions ):
		"""
		Met en place la liste des emissions
		"""
		listeEmissions.sort()
		self.emissionComboBox.clear()
		map( lambda x : self.emissionComboBox.addItem( stringToQstring( x ) ), listeEmissions )
		
		
if __name__ == "__main__" :
	app = QtGui.QApplication( sys.argv )
	window = MainWindow( "1.0" )
	window.show()
	sys.exit( app.exec_() )	
