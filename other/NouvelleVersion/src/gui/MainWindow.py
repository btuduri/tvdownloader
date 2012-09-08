#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import threading

import Constantes
# import lib

from PyQt4 import QtGui, QtCore
from gui.Qt.MyQPushButton  import MyQPushButton
from gui.Qt.MyQTableWidget import MyQTableWidget

import logging
logger = logging.getLogger( __name__ )

# import threading
# 
# import Constantes
# 
# from PyQt4 import QtGui, QtCore

from core.PluginManager import PluginManager

# 
# from API                              import API
# from Fichier                          import Fichier
# from GUI.AProposDialog                import AProposDialog
# from GUI.ConvertQString               import *
# from GUI.Downloader                   import Downloader
# from GUI.FenetreAttenteProgressDialog import FenetreAttenteProgressDialog
# from GUI.PreferencePluginDialog       import PreferencePluginDialog
# from GUI.PreferencesDialog            import PreferencesDialog
# from GUI.UpdateManagerDialog          import UpdateManagerDialog
# from Historique                       import Historique
# from PluginManager                    import PluginManager
# from Preferences                      import Preferences
# 
# import logging
# logger = logging.getLogger( __name__ )

##########
# Classe #
##########

## Fenetre principale de l'application
class MainWindow( QtGui.QMainWindow ):
	
	## Constructeur
	# Cree la fenetre principale en y ajoutant tous les widgets necessaires au programme
	def __init__( self ):
		
		
		
		
		
		# Appel au constructeur de la classe mere
		QtGui.QMainWindow.__init__( self )
		
		###########
		# Fenetre #
		###########
		
		###
		# Reglages de la fenetre principale
		###
		
		# Nom de la fenetre
		self.setWindowTitle( "%s %s" %( Constantes.TVD_NOM, Constantes.TVD_VERSION ) )
		# Mise en place de son icone
		self.setWindowIcon( QtGui.QIcon( "ico/TVDownloader.png" ) )

		###
		# Mise en place des widgets dans la fenetre
		###
		
		# Widget central qui contiendra tout
		self.centralWidget = QtGui.QWidget( self )
		
		#
		# Onglets
		#
		
		# Gestionnaire onglets
		self.tabWidget = QtGui.QTabWidget( self.centralWidget )
		
		# Onglet Fichiers
		self.tabFichiers = QtGui.QWidget( self.centralWidget )
		self.tabWidget.addTab( self.tabFichiers, u"Fichiers" )
		
		# Onglet Telechargements
		self.tabTelechargements = QtGui.QWidget( self.centralWidget )
		self.tabWidget.addTab( self.tabTelechargements, u"Téléchargements" )				

		#
		# Onglet Fichiers
		#

		# Layout de grille qui contient les elements de l'onglet Fichier
		self.gridLayoutFichiers = QtGui.QGridLayout( self.tabFichiers )
		
		# Liste des plugins
		self.listWidgetPlugins = QtGui.QListWidget( self.tabFichiers )
		self.listWidgetPlugins.setIconSize( QtCore.QSize( 75, 75 ) )
		self.gridLayoutFichiers.addWidget( self.listWidgetPlugins, 0, 0, 4, 1 )
		
		# Liste des chaines
		self.listWidgetChaines = QtGui.QListWidget( self.tabFichiers )
		self.gridLayoutFichiers.addWidget( self.listWidgetChaines, 0, 1, 1, 1 )
		
		# Liste des emissions
		self.listWidgetEmissions = QtGui.QListWidget( self.tabFichiers )
		self.gridLayoutFichiers.addWidget( self.listWidgetEmissions, 0, 2, 1, 1 )
		
		# Logo de l'emission
		self.logoFichierDefaut = QtGui.QPixmap()
		self.logoFichierDefaut.load( "img/logoVide.svg" )
		self.labelLogo = QtGui.QLabel( self.tabFichiers )
		self.labelLogo.setScaledContents( True )
		self.labelLogo.setPixmap( self.logoFichierDefaut.scaled( QtCore.QSize( 150, 150 ), QtCore.Qt.KeepAspectRatio ) )
		self.gridLayoutFichiers.addWidget( self.labelLogo, 0, 3, 1, 1 )
		
		# Descriptif du fichier
		# self.plainTextEditDescriptif = QtGui.QPlainTextEdit( self.tabFichiers )
		# self.gridLayoutFichiers.addWidget( self.plainTextEditDescriptif, 3, 1, 1, 3 )
		
		#
		# Onglet Fichiers - Liste des fichiers
		#
		
		# Layout de grille qui contient le tableau qui liste les fichiers et ses boutons
		self.gridLayoutListeFichiers = QtGui.QGridLayout( self.tabFichiers )
		
		# Tableau qui contient la liste des fichiers disponibles pour l'emission courante
		self.tableWidgetFichier = MyQTableWidget( self.tabFichiers )
		# Il a 4 colonnes et 0 ligne (pour l'instant)
		self.tableWidgetFichier.setColumnCount( 3 )
		self.tableWidgetFichier.setRowCount( 0 )
		# On ajoute les titres
		self.tableWidgetFichier.setHorizontalHeaderItem( 0,
														 self.tableWidgetFichier.creerItem( "" ) )
		self.tableWidgetFichier.setHorizontalHeaderItem( 1,
														 self.tableWidgetFichier.creerItem( "Date" ) )
		self.tableWidgetFichier.setHorizontalHeaderItem( 2,
														 self.tableWidgetFichier.creerItem( "Emission" ) )
		# Ajout au layout
		self.gridLayoutListeFichiers.addWidget( self.tableWidgetFichier, 0, 1, 4, 3 )
		
		# Icones du tableWidget
		self.iconeFichier     = QtGui.QIcon( "ico/gtk-file.svg" )
		self.iconeAjoute      = QtGui.QIcon( "ico/gtk-add.svg" )
		self.iconeTelecharge  = QtGui.QIcon( "ico/gtk-apply.svg" )
		
		# Bouton pour lire le fichier selectionnne
		self.pushButtonLire = MyQPushButton( self.tabFichiers )
		self.pushButtonLire.setIcon( QtGui.QIcon( "ico/gtk-media-play-ltr.svg" ) )
		self.pushButtonLire.setToolTip( u"Lire la vidéo selectionnée" )
		self.gridLayoutListeFichiers.addWidget( self.pushButtonLire, 0, 0, 1, 1 )
		
		# Bouton pour ajouter tous les fichiers a la liste des telechargements
		self.pushButtonToutAjouter = MyQPushButton( self.tabFichiers )
		self.pushButtonToutAjouter.setIcon( QtGui.QIcon( "ico/gtk-add.svg" ) )
		self.pushButtonToutAjouter.setToolTip( u"Ajouter tous les fichiers à la liste des téléchargements" )
		self.gridLayoutListeFichiers.addWidget( self.pushButtonToutAjouter, 1, 0, 1, 1 )
		
		# Bouton pour rafraichir le plugin courant
		self.pushButtonRafraichirPlugin = MyQPushButton( self.tabFichiers )
		self.pushButtonRafraichirPlugin.setIcon( QtGui.QIcon( "ico/gtk-refresh.svg" ) )
		self.pushButtonRafraichirPlugin.setToolTip( "Rafraichir le plugin" )
		self.gridLayoutListeFichiers.addWidget( self.pushButtonRafraichirPlugin, 2, 0, 1, 1 )

		# Bouton pour ouvrir la fenetre des preferences du plugin courant
		self.pushButtonPreferencesPlugin = MyQPushButton( self.tabFichiers )
		self.pushButtonPreferencesPlugin.setIcon( QtGui.QIcon( "ico/gtk-preferences.svg" ) )
		self.pushButtonPreferencesPlugin.setToolTip( u"Ouvrir les préférences du plugin" )
		self.gridLayoutListeFichiers.addWidget( self.pushButtonPreferencesPlugin, 3, 0, 1, 1 )		
		
		# Mise en place du layout sur un widget
		self.widgetFichiers = QtGui.QWidget( self.tabFichiers )
		self.widgetFichiers.setLayout( self.gridLayoutListeFichiers )
		self.gridLayoutFichiers.addWidget( self.widgetFichiers, 1, 1, 2, 3 )

		#
		# Barre progression de telechargement d'un fichier
		#
		self.progressBarTelechargementFichier = QtGui.QProgressBar( self.centralWidget )
		self.progressBarTelechargementFichier.setProperty( "value", 0 )
		
		#
		# Barre de progression de telechargement des fichiers
		#
		self.progressBarTelechargement = QtGui.QProgressBar( self.centralWidget )
		self.progressBarTelechargement.setProperty( "value", 0 )
		
		#
		# Boutons du bas pour gerer ajouter/supprimer/lancer telechargements
		#
		
		# Layout horizontal qui contiendra les boutons
		self.horizontalLayoutBarreBas = QtGui.QHBoxLayout()
		
		# Bouton pour lancer les telechargements
		self.pushButtonLancer = QtGui.QPushButton( QtGui.QIcon( "ico/gtk-media-play-ltr.svg" ), u"Lancer téléchargement", self.centralWidget )
		self.horizontalLayoutBarreBas.addWidget( self.pushButtonLancer )

		# Bouton pour stopper les telechargements
		self.pushButtonStop = QtGui.QPushButton( QtGui.QIcon( "ico/gtk-media-stop.svg" ), u"Stopper le téléchargement", self.centralWidget )
		self.pushButtonStop.setEnabled( False )
		self.horizontalLayoutBarreBas.addWidget( self.pushButtonStop )	
		
		###
		# Positionnement des differents widgets/layouts sur le layout de grille
		###
		
		# Layout de grille dans lequel on va placer nos widgets/layouts
		self.gridLayout = QtGui.QGridLayout( self.centralWidget )
		self.gridLayout.addWidget( self.tabWidget, 0, 0, 1, 2 )
		self.gridLayout.addWidget( self.progressBarTelechargementFichier, 2, 0, 1, 3 )
		self.gridLayout.addWidget( self.progressBarTelechargement, 3, 0, 1, 3 )
		self.gridLayout.addLayout( self.horizontalLayoutBarreBas, 4, 0, 1, 3 )		
		
		###
		# Mise en place du  central widget dans la fenetre
		###
		
		self.setCentralWidget( self.centralWidget )		
		
		###
		# Mise en place du menu
		###
		
		# Menu barre
		self.menubar = QtGui.QMenuBar( self )
		self.menubar.setGeometry( QtCore.QRect( 0, 0, 480, 25 ) )
		
		# Menu Fichier
		self.menuFichier = QtGui.QMenu( "&Fichier", self.menubar )
		self.menubar.addAction( self.menuFichier.menuAction() )
		
		# Action Fichier -> Quitter
		self.actionQuitter = QtGui.QAction( QtGui.QIcon( "ico/gtk-quit.svg" ), "&Quitter", self.menuFichier )
		self.actionQuitter.setIconVisibleInMenu( True )
		self.menuFichier.addAction( self.actionQuitter )
		
		# Menu Edition
		self.menuEdition = QtGui.QMenu( "&Edition", self.menubar )
		self.menubar.addAction( self.menuEdition.menuAction() )
		
		# Action Edition -> Mise a jour
		self.actionMAJ = QtGui.QAction( QtGui.QIcon( "ico/gtk-refresh.svg" ), u"&Mise à jour des plugins", self.menuEdition )
		self.actionMAJ.setIconVisibleInMenu( True )
		self.menuEdition.addAction( self.actionMAJ )
		
		# Action Edition -> Preferences
		self.actionPreferences = QtGui.QAction( QtGui.QIcon( "ico/gtk-preferences.svg" ), u"&Préférences", self.menuEdition )
		self.actionPreferences.setIconVisibleInMenu( True )
		self.menuEdition.addAction( self.actionPreferences )
		
		# Menu Aide
		self.menuAide = QtGui.QMenu( "&Aide", self.menubar )
		self.menubar.addAction( self.menuAide.menuAction() )
		
		# Action Aide -> A propos
		self.actionAPropos = QtGui.QAction( QtGui.QIcon( "ico/gtk-about.svg" ), u"À p&ropos", self.menuAide )
		self.actionAPropos.setIconVisibleInMenu( True )
		self.menuAide.addAction( self.actionAPropos )
		
		# Ajout du menu a l'interface
		self.setMenuBar( self.menubar )		
		
		
		
		
		
		
		
		self.resize( 500, 500 )



		################################################
		# Instanciations + initialisation de variables #
		################################################
		
		# Plugin Manager
		self.pluginManager = PluginManager()
		# Mise en place des plugins
		self.ajouterPlugins( [ ( inst.nom, inst.logo ) for inst in self.pluginManager.getPluginListeInstances() ] )






	## Execute les actions necessaires avant de quitter le programme
	def actionsAvantQuitter( self ):
		pass

	#########################################
	# Surcharge des methodes de QMainWindow #
	#########################################
	
	## Surcharge de la methode appelee lors de la fermeture de la fenetre
	# Ne doit pas etre appele explicitement
	# @param evenement Evenement qui a provoque la fermeture
	def closeEvent( self, evenement ):
		pass	

	##################################################################
	# Methodes qui remplissent les elements de l'onglet de recherche #
	##################################################################
	
	## Ajoute les plugins
	# @param listePlugins Liste des plugins sous la forme [ ( nom, image ) ]
	def ajouterPlugins( self, listePlugins ):
		for ( nom, logo ) in listePlugins:
			item = QtGui.QListWidgetItem( QtGui.QIcon( logo ), "" )
			item.setToolTip( nom )
			self.listWidgetPlugins.addItem( item )
	
	## Ajoutes les chaines
	# @param listeChaines Liste des chaines
	def ajouterChaines( self, listeChaines ):
		pass

	## Ajoute les emissions
	# @param listeEmissions Liste des emissions	
	def ajouterEmissions( self, listeEmissions ):
		pass
	
	## Ajoute le logo de l'emission selectionnee
	# @param cheminLogo Chemin du logo
	def ajouterLogoEmission( self, cheminLogo ):
		pass
		
	## Ajoute les fichiers
	# @param listeFichiers Liste des fichiers
	def ajouterFichiers( self, listeFichiers ):
		pass

	## Ajoute le descriptif du fichier selectionne
	# @param descriptif Descriptif du fichier
	def ajouterDescriptif( self, descriptif ):	
		pass
		
	##################################
	# Slots de l'onglet de recherche #
	##################################	
	
	## Liste les chaines d'un plugin
	# @param nomPlugin Nom du plugin
	def listerChaines( self, nomPlugin ):
		pass
	
	## Liste les emissions d'une chaine
	# @param nomChaine Nom de la chaine
	# @param nomPlugin Nom du plugin
	def listerEmissions( self, nomChaine, nomPlugin ):
		pass
	
	## Liste les fichiers d'une emissions
	# @param nomEmission Nom d'une emission
	# @param nomChaine   Nom de la chaine
	# @param nomPlugin   Nom du plugin
	def listerFichiers( self, nomEmission, nomChaine, nomPlugin ):
		pass
	
	## Rafraichit un plugin
	# @param nomPlugin Nom du plugin a rafraichir
	def rafraichirPlugin( self, nomPlugin ):
		pass
		
	#######################################################################
	# Methodes qui remplissent les elements de l'onglet de telechargement #
	#######################################################################
	
	
		
	#######################################
	# Slots de l'onglet de telechargement #
	#######################################	



	##############################################
	# Slots pour l'ouverture des autres fenetres #
	##############################################	
	
	## Ouvre la fenetre About
	def ouvrirFenetreAPropos( self ):
		pass
	
	## Ouvre les preferences du logiciel
	def ouvrirPreferencesLogiciel( self ):
		pass
	
	## Ouvre la fenetre de mise a jour des plugins
	def ouvrirFenetreMiseAJour( self ):
		pass
		
	## Ouvre les preferences du plugin courant
	# @param nomPlugin Nom du plugin	
	def ouvrirPreferencesPlugin( self, nomPlugin ):
		pass
	
	## Ouvre le repertoire de telechargement
	def ouvrirRepertoireTelechargement( self ):
		pass
