#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import operator
import threading

import sys
sys.path.append( ".." ) 

import tvdcore

from base.qt.QtFolderChooser import QtFolderChooser
from base.qt.qtString        import qstringToString
from base.qt.qtString        import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

from uis.qt.QtIconsList import QtIconsList
from uis.qt.QtTable     import QtTable

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
		
		self.tvdIco   = QtGui.QIcon( "uis/qt/ico/TVDownloader.png" )
		self.folderIco = QtGui.QIcon( "uis/qt/ico/gtk-folder.svg" )
		# self.addIco   = QtGui.QIcon( "uis/qt/ico/gtk-add.svg" )
		# self.applyIco = QtGui.QIcon( "uis/qt/ico/gtk-apply.svg" )
		# self.fileIco  = QtGui.QIcon( "uis/qt/ico/gtk-file.svg" )
		
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

		# Liste des fichiers a mettre en place
		self.listeFichiersSignal = QtCore.SIGNAL( "listeFichiers(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listeFichiersSignal , self.ajouterFichiers )
		
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
		QtCore.QObject.connect( self.emissionComboBox,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerFichiers )
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
		# Recupere l'instance de TVDContext
		self.tvdContext = tvdcore.TVDContext()
		# Recupere les instances des classes utiles
		self.pluginManager = self.tvdContext.pluginManager
		
		# Liste les plugins
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
			listePlugins = self.pluginManager.getPluginListe()
			self.emit( self.listePluginsSignal, listePlugins )
		
		threading.Thread( target = threadListerPlugins, args = ( self, ) ).start()
	
	def listerChaines( self, plugin = None ):
		"""
		Fonction qui demande la liste des chaines d'un plugin donne
		Si plugin = None, alors elle demande la liste des chaines de tous les plugins
		"""
		def threadListerChaines( self, plugin ):
			listeChaines = map( lambda x : ( x, None ), self.pluginManager.getPluginListeChaines( plugin ) )
			self.emit( self.listeChainesSignal, listeChaines )
		
		if( plugin ):
			plugin = qstringToString( plugin )
		threading.Thread( target = threadListerChaines, args = ( self, plugin ) ).start()

	def listerEmissions( self, chaine ):
		"""
		Fonction qui demande la liste des emissions d'une chaine donnee
		"""
		def threadListerEmissions( self, plugin, chaine ):
			listeEmissions = self.pluginManager.getPluginListeEmissions( plugin, chaine )
			self.emit( self.listeEmissionsSignal, listeEmissions )
		
		plugin = qstringToString( self.pluginComboBox.currentText() )
		threading.Thread( target = threadListerEmissions, args = ( self, plugin, chaine ) ).start()

	def listerFichiers( self, emission ):
		"""
		Fonction qui demande la liste des fichiers d'une emission donnee
		"""		
		def threadListerFichiers( self, plugin, emission ):
			listeFichiers = self.pluginManager.getPluginListeFichiers( plugin, emission )
			self.emit( self.listeFichiersSignal, listeFichiers )
		
		plugin = qstringToString( self.pluginComboBox.currentText() )
		threading.Thread( target = threadListerFichiers, args = ( self, plugin, emission ) ).start()		
		
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
	
	def ajouterFichiers( self, listeFichiers ):
		"""
		Met en place la liste des fichiers
		"""
		self.fichierTableWidget.clear()
		ligneCourante = 0
		for fichier in listeFichiers:
			self.fichierTableWidget.insertRow( ligneCourante )
			tableRow = []
			tableRow.append( self.fichierTableWidget.createItem( "" ) )
			tableRow.append( self.fichierTableWidget.createItem( fichier.date ) )
			tableRow.append( self.fichierTableWidget.createItem( fichier.nom ) )
			self.fichierTableWidget.setLigne( ligneCourante, tableRow )
			ligneCourante += 1
		self.fichierTableWidget.resizeColumnsToContents()
		
