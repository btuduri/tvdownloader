#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import operator
import threading

import sys
sys.path.append( ".." ) 

from base.qt.QtFolderChooser import QtFolderChooser
from base.qt.qtString        import qstringToString
from base.qt.qtString        import stringToQstring

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
		# Fonts
		#
		
		# Font pour les titres
		self.titreFont = QtGui.QFont()
		self.titreFont.setPointSize( 11 )
		self.titreFont.setWeight( 75 )
		self.titreFont.setBold( True )
		
		#
		# Icones
		#
		
		self.tvdIco   = QtGui.QIcon( "ico/TVDownloader.png" )
		self.folderIco = QtGui.QIcon( "ico/gtk-folder.svg" )
		# self.addIco   = QtGui.QIcon( "ico/gtk-add.svg" )
		# self.applyIco = QtGui.QIcon( "ico/gtk-apply.svg" )
		# self.fileIco  = QtGui.QIcon( "ico/gtk-file.svg" )
		
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
		self.telechargementsWidget = QtGui.QScrollArea( self.centralWidget )
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
		# Onglet Parametres
		#
		
		# Layout de forumlaire
		self.parametresLayout = QtGui.QFormLayout( self.parametresWidget )
		
		# Titre Repertoire
		self.titreRepertoireLabel = QtGui.QLabel( self.parametresWidget )
		self.titreRepertoireLabel.setFont( self.titreFont )
		self.titreRepertoireLabel.setText( u"Répertoires :" )
		self.parametresLayout.addRow( self.titreRepertoireLabel, None )		
		
		# Repertoire par defaut pour les videos
		self.choixRepertoire = QtFolderChooser( self.parametresWidget, self.folderIco )
		self.parametresLayout.addRow( u"Répertoire de téléchargement :", self.choixRepertoire )
		
		# Titre Internet
		self.titreInternetLabel = QtGui.QLabel( self.parametresWidget )
		self.titreInternetLabel.setFont( self.titreFont )
		self.titreInternetLabel.setText( u"Paramètres Internet :" )
		self.parametresLayout.addRow( self.titreInternetLabel, None )
		
		# Time out du navigateur
		self.timeOutSpinBox = QtGui.QSpinBox( self.parametresWidget )
		self.timeOutSpinBox.setMinimum( 1 )
		self.timeOutSpinBox.setMaximum( 60 )
		self.parametresLayout.addRow( u"Time out (en s) :", self.timeOutSpinBox )
		
		# Nombre de threads du navigateur
		self.threadSpinBox = QtGui.QSpinBox( self.parametresWidget )
		self.threadSpinBox.setMinimum( 1 )
		self.threadSpinBox.setMaximum( 100 )
		self.parametresLayout.addRow( u"Nombre de threads max :", self.threadSpinBox )
		
		
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
