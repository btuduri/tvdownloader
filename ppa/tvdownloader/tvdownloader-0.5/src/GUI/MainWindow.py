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

import os
import os.path
import time
import threading

from PyQt4 import QtGui, QtCore
from GUI.Qt.MyQTableWidget import MyQTableWidget

from GUI.ConvertQString import *
from API import API
from GUI.Signaux import Signaux
from PluginManager import PluginManager
from Preferences import Preferences
from GUI.PreferencesDialog import PreferencesDialog
from GUI.PreferencePluginDialog import PreferencePluginDialog
from Downloader import Downloader
from GUI.AProposDialog import AProposDialog
from Fichier import Fichier
from Historique import Historique
from GUI.FenetreAttenteProgressDialog import FenetreAttenteProgressDialog

##############
# Constantes #
##############

# Position des colonnes dans tableWidgetFichier
FICHIER_COLONNE_DATE			   = 0
FICHIER_COLONNE_EMISSION		   = 1
FICHIER_COLONNE_LIEN			   = 2
FICHIER_COLONNE_NOM_FICHIER_SORTIE = 3

# Position des colonnes dans tableWidgetTelechargement
TELECHARGEMENT_COLONNE_DATE			      = 0
TELECHARGEMENT_COLONNE_EMISSION		      = 1
TELECHARGEMENT_COLONNE_LIEN			      = 2
TELECHARGEMENT_COLONNE_NOM_FICHIER_SORTIE = 3
TELECHARGEMENT_COLONNE_ETAT			      = 4

##########
# Classe #
##########

## Fenetre principale de l'application
class MainWindow( QtGui.QMainWindow ):
	
	## Constructeur
	# Le constructeur va creer la fenetre principale en y ajoutant tous les widgets necessaires au programme
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
		self.setWindowTitle( "TVDownloader" )
		# Dimensions la fenetre
		self.resize( 500, 500 )
		# Mise en place de son icone
		self.setWindowIcon( QtGui.QIcon( "ico/TVDownloader.png" ) )
		
		###
		# Mise en place des widgets dans la fenetre
		###
		
		# Widget central qui contiendra tout
		self.centralWidget = QtGui.QWidget( self )
		
		#
		# Barre du haut
		#
		
		# Layout horizontal qui contiendra les listes deroulantes
		self.horizontalLayoutBarreHaut = QtGui.QHBoxLayout()
		
		# Liste deroulante pour choisir le site (plugin)
		self.comboBoxSite = QtGui.QComboBox( self.centralWidget )
		self.horizontalLayoutBarreHaut.addWidget( self.comboBoxSite )
		
		# Liste deroulante pour choisir une chaine du site courant
		self.comboBoxChaine = QtGui.QComboBox( self.centralWidget)
		self.horizontalLayoutBarreHaut.addWidget( self.comboBoxChaine )
		
		# Liste deroulante pour choisir une emission de la chaine courante
		self.comboBoxEmission = QtGui.QComboBox( self.centralWidget )
		self.horizontalLayoutBarreHaut.addWidget( self.comboBoxEmission )
		
		#
		# Liste des fichiers
		#
		
		# Layout de grille qui contient le tableau qui liste les fichiers + boutons
		self.gridLayoutFichiers = QtGui.QGridLayout()
		
		# Tableau qui contient la liste des fichiers disponibles pour l'emission courante
		self.tableWidgetFichier = MyQTableWidget( self.centralWidget )
		# Il a 4 colonnes et 0 ligne (pour l'instant)
		self.tableWidgetFichier.setColumnCount( 4 )
		self.tableWidgetFichier.setRowCount( 0 )
		# On ajoute le titre des 4 colonnes
		self.tableWidgetFichier.setHorizontalHeaderItem( FICHIER_COLONNE_DATE,
														 self.tableWidgetFichier.creerItem( "Date" ) )
		self.tableWidgetFichier.setHorizontalHeaderItem( FICHIER_COLONNE_EMISSION,
														 self.tableWidgetFichier.creerItem( "Emission" ) )
		self.tableWidgetFichier.setHorizontalHeaderItem( FICHIER_COLONNE_LIEN,
														 self.tableWidgetFichier.creerItem( "Lien" ) )
		self.tableWidgetFichier.setHorizontalHeaderItem( FICHIER_COLONNE_NOM_FICHIER_SORTIE,
														 self.tableWidgetFichier.creerItem( "NomFichierSortie" ) )
		# On masque la colonne qui contient les liens et les noms des fichiers en sortie
		self.tableWidgetFichier.setColumnHidden( FICHIER_COLONNE_LIEN, True )
		self.tableWidgetFichier.setColumnHidden( FICHIER_COLONNE_NOM_FICHIER_SORTIE, True )
		# On l'ajoute au layout
		self.gridLayoutFichiers.addWidget( self.tableWidgetFichier, 0, 1, 4, 1 )
		
		# Bouton pour ajouter tous les fichiers a la liste des telechargements
		self.pushButtonToutAjouter = QtGui.QPushButton( self.centralWidget )
		self.pushButtonToutAjouter.setIcon( QtGui.QIcon( "ico/gtk-add.svg" ) )
		self.pushButtonToutAjouter.setToolTip( u"Ajouter tous les fichiers a la liste des téléchargements" )
		sizePolicy = self.pushButtonToutAjouter.sizePolicy()
		sizePolicy.setVerticalPolicy( QtGui.QSizePolicy.Expanding )
		self.pushButtonToutAjouter.setSizePolicy( sizePolicy )
		self.gridLayoutFichiers.addWidget( self.pushButtonToutAjouter, 0, 0, 2, 1 )
		
		# Bouton pour rafraichir le plugin courant
		self.pushButtonRafraichirPlugin = QtGui.QPushButton( self.centralWidget )
		self.pushButtonRafraichirPlugin.setIcon( QtGui.QIcon( "ico/gtk-refresh.svg" ) )
		self.pushButtonRafraichirPlugin.setToolTip( "Rafraichir le plugin" )
		self.gridLayoutFichiers.addWidget( self.pushButtonRafraichirPlugin, 2, 0, 1, 1 )

		# Bouton pour ouvrir la fenetre des preferences du plugin courant
		self.pushButtonPreferencesPlugin = QtGui.QPushButton( self.centralWidget )
		self.pushButtonPreferencesPlugin.setIcon( QtGui.QIcon( "ico/gtk-preferences.svg" ) )
		self.pushButtonPreferencesPlugin.setToolTip( u"Préférences du plugin" )
		self.gridLayoutFichiers.addWidget( self.pushButtonPreferencesPlugin, 3, 0, 1, 1 )
		
		#
		# Liste des telechargements
		#
		
		# Layout de grille qui contient le tableau qui liste les fichiers a telecharger + les boutons pour le controller
		self.gridLayoutTelechargement = QtGui.QGridLayout()
		
		# Tableau qui contient la liste des fichiers a telecharger
		self.tableWidgetTelechargement = MyQTableWidget( self.centralWidget )
		# Il a 5 colonnes et 0 ligne (pour l'instant)
		self.tableWidgetTelechargement.setColumnCount( 5 )
		self.tableWidgetTelechargement.setRowCount( 0 )
		# On ajoute le titre des 5 colonnes
		self.tableWidgetTelechargement.setHorizontalHeaderItem( TELECHARGEMENT_COLONNE_DATE,
																self.tableWidgetTelechargement.creerItem( "Date" ) )
		self.tableWidgetTelechargement.setHorizontalHeaderItem( TELECHARGEMENT_COLONNE_EMISSION,
																self.tableWidgetTelechargement.creerItem( "Emission" ) )
		self.tableWidgetTelechargement.setHorizontalHeaderItem( TELECHARGEMENT_COLONNE_LIEN,
																self.tableWidgetTelechargement.creerItem( "Lien" ) )
		self.tableWidgetTelechargement.setHorizontalHeaderItem( TELECHARGEMENT_COLONNE_NOM_FICHIER_SORTIE,
																self.tableWidgetTelechargement.creerItem( "NomFichierSortie" ) )
		self.tableWidgetTelechargement.setHorizontalHeaderItem( TELECHARGEMENT_COLONNE_ETAT,
																self.tableWidgetTelechargement.creerItem( "Etat" ) )
		# On masque la colonne qui contient les liens et les noms des fichiers en sortie
		self.tableWidgetTelechargement.setColumnHidden( TELECHARGEMENT_COLONNE_LIEN, True )
		self.tableWidgetTelechargement.setColumnHidden( TELECHARGEMENT_COLONNE_NOM_FICHIER_SORTIE, True )
		# On l'ajoute au layout
		self.gridLayoutTelechargement.addWidget( self.tableWidgetTelechargement, 0, 1, 4, 1 )
		
		# Bouton pour monter l'element selectionne tout en haut de la liste
		self.pushButtonExtremiteMonter = QtGui.QPushButton( self.centralWidget )
		self.pushButtonExtremiteMonter.setIcon( QtGui.QIcon( "ico/gtk-jump-to-rtl.svg" ) )
		self.pushButtonExtremiteMonter.setToolTip( u"Placer l'élément sélectionné en haut de la liste" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonExtremiteMonter, 0, 0, 1, 1 )
		
		# Bouton pour monter l'element selectionne d'un cran dans la liste
		self.pushButtonMonter = QtGui.QPushButton( self.centralWidget )
		self.pushButtonMonter.setIcon( QtGui.QIcon( "ico/gtk-go-up.svg" ) )
		self.pushButtonMonter.setToolTip( u"Monter l'élément sélectionné" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonMonter, 1, 0, 1, 1 )

		# Bouton pour descendre l'element selectionne d'un cran dans la liste
		self.pushButtonDescendre = QtGui.QPushButton( self.centralWidget )
		self.pushButtonDescendre.setIcon( QtGui.QIcon( "ico/gtk-go-down.svg" ) )
		self.pushButtonDescendre.setToolTip( u"Descendre l'élément selectionné" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonDescendre, 2, 0, 1, 1 )
		
		# Bouton pour descendre l'element selectionne tout en bas de la liste
		self.pushButtonExtremiteDescendre = QtGui.QPushButton( self.centralWidget )
		self.pushButtonExtremiteDescendre.setIcon( QtGui.QIcon( "ico/gtk-jump-to-ltr.svg" ) )
		self.pushButtonExtremiteDescendre.setToolTip( u"Placer l'élément sélectionné en bas de la liste" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonExtremiteDescendre, 3, 0, 1, 1 )
		
		# Bouton pour supprimer tous les elements de la liste
		self.pushButtonToutSupprimer = QtGui.QPushButton( self.centralWidget )
		self.pushButtonToutSupprimer.setIcon( QtGui.QIcon( "ico/gtk-cancel.svg" ) )
		self.pushButtonToutSupprimer.setToolTip( u"Supprime tous les éléments de la liste" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonToutSupprimer, 0, 2, 1, 1 )
		
		# Bouton pour supprimer de la liste les telechargements termines
		self.pushButtonNettoyer = QtGui.QPushButton( self.centralWidget )
		self.pushButtonNettoyer.setIcon( QtGui.QIcon( "ico/gtk-delete-full.svg" ) )
		self.pushButtonNettoyer.setToolTip( u"Nettoie les téléchargement terminés" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonNettoyer, 1, 2, 1, 1 )
		
		# Bouton pour ouvrir le dossier des telechargements
		self.pushButtonOuvrirDossierTelechargement = QtGui.QPushButton( self.centralWidget )
		self.pushButtonOuvrirDossierTelechargement.setIcon( QtGui.QIcon( "ico/gtk-folder.svg" ) )
		self.pushButtonOuvrirDossierTelechargement.setToolTip( u"Ouvrir le dossier des téléchargements" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonOuvrirDossierTelechargement, 2, 2, 1, 1 )
		
		## !!!
		## Ajouter un bouton pour lire une video + bouton pour ouvrir le dossier des telechargements
		## !!!
		
		
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
		# On ajoute la barre du haut
		self.gridLayout.addLayout( self.horizontalLayoutBarreHaut, 0, 0, 1, 3 )
		# On ajoute le tableau des fichiers diponibles
		self.gridLayout.addLayout( self.gridLayoutFichiers, 1, 0, 1, 3 )
		# On ajouteb le tableau des ficheirs a telecharger + ses boutons
		self.gridLayout.addLayout( self.gridLayoutTelechargement, 2, 0, 1, 3 )
		# On ajoute la barre de progression de telechargement d'un fichier
		self.gridLayout.addWidget( self.progressBarTelechargementFichier, 3, 0, 1, 3 )
		# On ajoute la barre de progression de telechargement des fichiers
		self.gridLayout.addWidget( self.progressBarTelechargement, 4, 0, 1, 3 )
		# On ajoute les boutons ajouter/supprimer/lancer
		self.gridLayout.addLayout( self.horizontalLayoutBarreBas, 5, 0, 1, 3 )
		
		###
		# Mise en place le central widget dans la fenetre
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
		self.actionQuitter = QtGui.QAction( QtGui.QIcon( "ico/gtk-quit.svg" ), "&Quitter", self )
		self.actionQuitter.setIconVisibleInMenu( True )
		self.menuFichier.addAction( self.actionQuitter )
		
		# Menu Edition
		self.menuEdition = QtGui.QMenu( "&Edition", self.menubar )
		self.menubar.addAction( self.menuEdition.menuAction() )
		
		# Action Edition -> Preferences
		self.actionPreferences = QtGui.QAction( QtGui.QIcon( "ico/gtk-preferences.svg" ), u"&Préférences", self )
		self.actionPreferences.setIconVisibleInMenu( True )
		self.menuEdition.addAction( self.actionPreferences )
		
		# Menu Aide
		self.menuAide = QtGui.QMenu( "&Aide", self.menubar )
		self.menubar.addAction( self.menuAide.menuAction() )
		
		# Action Aide -> A propos
		self.actionAPropos = QtGui.QAction( QtGui.QIcon( "ico/gtk-about.svg" ), u"À p&ropos", self )
		self.actionAPropos.setIconVisibleInMenu( True )
		self.menuAide.addAction( self.actionAPropos )
		
		# Ajout du menu a l'interface
		self.setMenuBar( self.menubar )

		###
		# Signaux provenants de l'interface
		###

		QtCore.QObject.connect( self.tableWidgetFichier,
								QtCore.SIGNAL( "cellDoubleClicked(int,int)" ),
								self.ajouterTelechargement )	
								
		QtCore.QObject.connect( self.pushButtonToutAjouter,
								QtCore.SIGNAL( "clicked()" ),
								self.ajouterTousLesFichiers )								

		QtCore.QObject.connect( self.pushButtonRafraichirPlugin,
								QtCore.SIGNAL( "clicked()" ),
								self.rafraichirPlugin )

		QtCore.QObject.connect( self.tableWidgetTelechargement,
								QtCore.SIGNAL( "cellDoubleClicked(int,int)" ),
								self.supprimerTelechargement )	
		
		QtCore.QObject.connect( self.pushButtonExtremiteMonter,
								QtCore.SIGNAL( "clicked()" ),
								lambda versLeHaut = True, extremite = True : self.tableWidgetTelechargement.deplacerLigne( versLeHaut, extremite ) )
		
		QtCore.QObject.connect( self.pushButtonMonter,
								QtCore.SIGNAL( "clicked()" ),
								lambda versLeHaut = True, extremite = False : self.tableWidgetTelechargement.deplacerLigne( versLeHaut, extremite ) )
		
		QtCore.QObject.connect( self.pushButtonDescendre,
								QtCore.SIGNAL( "clicked()" ),
								lambda versLeHaut = False, extremite = False : self.tableWidgetTelechargement.deplacerLigne( versLeHaut, extremite ) )
		
		QtCore.QObject.connect( self.pushButtonExtremiteDescendre,
								QtCore.SIGNAL( "clicked()" ),
								lambda versLeHaut = False, extremite = True : self.tableWidgetTelechargement.deplacerLigne( versLeHaut, extremite ) )
		
		QtCore.QObject.connect( self.pushButtonToutSupprimer,
								QtCore.SIGNAL( "clicked()" ),
								self.tableWidgetTelechargement.toutSupprimer )
		
		QtCore.QObject.connect( self.pushButtonNettoyer,
								QtCore.SIGNAL( "clicked()" ),
								self.nettoyer )
		
		QtCore.QObject.connect( self.pushButtonLancer,
								QtCore.SIGNAL( "clicked()" ),
								self.lancerTelechargement )

		QtCore.QObject.connect( self.pushButtonStop,
								QtCore.SIGNAL( "clicked()" ),
								self.stopperTelechargement )
		
		QtCore.QObject.connect( self.actionQuitter,
								QtCore.SIGNAL( "triggered()" ),
								self.close )						
	
		################################################
		# Instanciations + initialisation de variables #
		################################################
		
		# Fenetre About
		self.aProposDialog = None
		# Fenetre des preferences du logiciel
		self.preferencesDialog = None
		# Nom plugin courant
		self.nomPluginCourant = ""
		
		# On intancie le lanceur de signaux
		self.signaux = Signaux()
		# On instancie le plugin manager
		#~ self.pluginManager = PluginManager()
		# On instancie le gestionnaire de preferences
		self.preferences = Preferences()
		# On instancie le gestionnaire de preferences des plugins
		self.preferencesPluginDialog = PreferencePluginDialog( self )
		# On instancie le gestionnaire de download
		self.downloader = Downloader( self.signaux )	
		# On recupere l'instance de API
		self.api = API.getInstance()
		# On instancie le gestionnaire d'historique
		self.historique = Historique()
		# On instancie la fenetre d'attente
		self.fenetreAttenteProgressDialog = FenetreAttenteProgressDialog( self ) 										 
		
		#
		# Fenetre de confirmation pour quitter le logiciel
		#
		self.quitterMessageBox = QtGui.QMessageBox( self )
		self.quitterMessageBox.setWindowTitle( "Fermeture de TVDownloader" )
		self.quitterMessageBox.setText( u"Voulez-vous réellement quitter TVDownloader ?" )
		self.quitterMessageBox.setInformativeText( u"Votre liste de téléchargement sera perdue" )
		self.quitterMessageBox.addButton( "Oui", QtGui.QMessageBox.AcceptRole )
		self.quitterMessageBox.addButton( "Non", QtGui.QMessageBox.RejectRole )
		
		############################################################
		# On connecte les signaux des instances precedements crees #
		############################################################	

		QtCore.QObject.connect( self.pushButtonOuvrirDossierTelechargement,
								QtCore.SIGNAL( "clicked()" ),
								self.ouvrirRepertoireTelechargement )
		
		QtCore.QObject.connect( self.comboBoxSite,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerChaines )
		
		QtCore.QObject.connect( self.comboBoxChaine,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerEmissions )
		
		QtCore.QObject.connect( self.comboBoxEmission,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerFichiers )

		QtCore.QObject.connect( self.pushButtonPreferencesPlugin,
								QtCore.SIGNAL( "clicked()" ),
								self.ouvrirPreferencesPlugin )

		QtCore.QObject.connect( self.actionPreferences,
								QtCore.SIGNAL( "triggered()" ),
								self.ouvrirPreferencesLogiciel )	

		QtCore.QObject.connect( self.actionAPropos,
								QtCore.SIGNAL( "triggered()" ),
								self.ouvrirFenetreAPropos )
		
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ) , self.fenetreAttenteProgressDialog.ouvrirFenetreAttente )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "finActualisation()" ) , self.fenetreAttenteProgressDialog.fermerFenetreAttente )		
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "actualiserListesDeroulantes()" ) , self.actualiserListesDeroulantes )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "listeChaines(PyQt_PyObject)" ) , self.ajouterChaines )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "listeEmissions(PyQt_PyObject)" ) , self.ajouterEmissions )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "listeFichiers(PyQt_PyObject)" ) , self.ajouterFichiers )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "debutTelechargement(int)" ) , self.debutTelechargement )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "finTelechargement(int)" ) , self.finTelechargement )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "finDesTelechargements()" ) , self.activerDesactiverInterface )
		QtCore.QObject.connect( self.signaux, QtCore.SIGNAL( "pourcentageFichier(int)" ) , self.progressBarTelechargementFichier.setValue )		

		#########
		# Début #
		#########			
		
		# Si aucun plugin n'est active, on ouvre la fenetre des preferences
		if( len( self.preferences.getPreference( "pluginsActifs" ) ) == 0 ):
			self.ouvrirPreferencesLogiciel()
		
		# On actualise tous les plugins
		self.rafraichirTousLesPlugins()

	## Methode qui execute les actions necessaires avant de quitter le programme
	def actionsAvantQuitter( self ):
		# On sauvegarde les options des plugins
		self.api.fermeture()
		# On sauvegarde les options du logiciel
		self.preferences.sauvegarderConfiguration()
		# On sauvegarde l'historique
		self.historique.sauverHistorique()
		# On stoppe les telechargements
		self.stopperTelechargement()

	#########################################
	# Surcharge des methodes de QMainWindow #
	#########################################
	
	## Surcharge de la methode appelee lors de la fermeture de la fenetre
	# Ne doit pas etre appele explicitement
	# @param evenement Evenement qui a provoque la fermeture
	def closeEvent( self, evenement ):
		# On affiche une fenetre pour demander la fermeture si des fichiers sont dans la liste de telechargement
		if( self.tableWidgetTelechargement.rowCount() > 0 ):
			# On affiche une fenetre qui demande si on veut quitter
			retour = self.quitterMessageBox.exec_()
			# Si on veut quitter
			if( retour == 0 ):
				# On execute les actions necessaires
				self.actionsAvantQuitter()
				# On accept la fermeture
				evenement.accept()
			else:
				# On refuse la fermeture
				evenement.ignore()
		else: # S'il n'y a pas de fichier
			# On execute les actions necessaires
			self.actionsAvantQuitter()
			# On accept la fermeture
			evenement.accept()		

	##############################################
	# Methodes pour remplir les menus deroulants #
	##############################################

	## Methode qui actualise les listes deroulantes
	def actualiserListesDeroulantes( self ):
		# On lance juste l'ajout des sites en se basant sur les plugins actifs
		self.ajouterSites( self.preferences.getPreference( "pluginsActifs" ) )

	## Methode qui lance le listage des chaines
	# @param site Nom du plugin/site pour lequel on va lister les chaines
	def listerChaines( self, site ):
		def threadListerChaines( self, nomPlugin ):
			self.signaux.signal( "debutActualisation", nomPlugin )
			listeChaines = self.api.getPluginListeChaines( nomPlugin )
			self.signaux.signal( "listeChaines", listeChaines )
			self.signaux.signal( "finActualisation" )
			
		if( site != "" ):
			self.nomPluginCourant = qstringToString( site )
			threading.Thread( target = threadListerChaines, args = ( self, self.nomPluginCourant ) ).start()
			# On active (ou pas) le bouton de preference du plugin
			self.pushButtonPreferencesPlugin.setEnabled( self.api.getPluginListeOptions( self.nomPluginCourant ) != [] )
		
	## Methode qui lance le listage des emissions
	# @param chaine Nom de la chaine pour laquelle on va lister les emissions
	def listerEmissions( self, chaine ):
		def threadListerEmissions( self, nomPlugin, chaine ):
			self.signaux.signal( "debutActualisation", nomPlugin )
			listeEmissions = self.api.getPluginListeEmissions( nomPlugin, chaine )
			self.signaux.signal( "listeEmissions", listeEmissions )
			self.signaux.signal( "finActualisation" )
			
		if( chaine != "" ):
			threading.Thread( target = threadListerEmissions, args = ( self, self.nomPluginCourant, qstringToString( chaine ) ) ).start()
		
	## Methode qui lance le listage des fichiers
	# @param emission Nom de l'emission pour laquelle on va lister les fichiers
	def listerFichiers( self, emission ):
		def threadListerFichiers( self, nomPlugin, emission ):
			self.signaux.signal( "debutActualisation", nomPlugin )
			listeFichiers = self.api.getPluginListeFichiers( nomPlugin, emission )
			self.signaux.signal( "listeFichiers", listeFichiers )
			self.signaux.signal( "finActualisation" )
			
		if( emission != "" ):
			threading.Thread( target = threadListerFichiers, args = ( self, self.nomPluginCourant, qstringToString( emission ) ) ).start()
	
	## Methode qui met en place une liste de sites sur l'interface
	# @param listeSites Liste des sites a mettre en place
	def ajouterSites( self, listeSites ):
		# On efface la liste des sites
		self.comboBoxSite.clear()
		# On met en place les sites
		for site in listeSites:
			self.comboBoxSite.addItem( stringToQstring( site ) )
		# On lance l'ajout des chaines
		self.listerChaines( self.comboBoxSite.currentText() )
	
	## Methode qui met en place une liste de chaines sur l'interface
	# @param listeChaines Liste des chaines a mettre en place
	def ajouterChaines( self, listeChaines ):
		# On efface la liste des chaines
		self.comboBoxChaine.clear()
		# On met en place les chaines
		for chaine in listeChaines:
			self.comboBoxChaine.addItem( stringToQstring( chaine ) )
		# On lance l'ajout des emissions
		self.listerEmissions( self.comboBoxChaine.currentText() )

	## Methode qui met en place une liste d'emissions sur l'interface
	# @param listeEmissions Liste des emissions a mettre en place	
	def ajouterEmissions( self, listeEmissions ):
		# On efface la liste des emissions
		self.comboBoxEmission.clear()
		# On met en place la liste des emissions
		for emission in listeEmissions:
			self.comboBoxEmission.addItem( stringToQstring( emission ) )
		# On lance l'ajout des fichiers
		self.listerFichiers( self.comboBoxEmission.currentText() )
	
	###############################################
	# Methodes pour remplir la liste des fichiers #
	###############################################
	
	## Methode pour ajouter des fichiers a l'interface
	# @param listeFichiers Liste des fichiers a ajouter
	def ajouterFichiers( self, listeFichiers ):
		# On efface la liste des fichiers
		self.tableWidgetFichier.toutSupprimer()
		# On commence au depart
		ligneCourante = 0
		# On met en place chacun des fichiers
		for fichier in listeFichiers:
			# On ajoute une ligne
			self.tableWidgetFichier.insertRow( ligneCourante )
			# On ajoute la date, le nom et le lien au tableWidgetFichier
			liste = []
			liste.insert( FICHIER_COLONNE_DATE,     self.tableWidgetFichier.creerItem( getattr( fichier, "date" ) ) )
			liste.insert( FICHIER_COLONNE_EMISSION, self.tableWidgetFichier.creerItem( getattr( fichier, "nom" ) ) )
			liste.insert( FICHIER_COLONNE_LIEN,     self.tableWidgetFichier.creerItem( getattr( fichier, "lien" ) ) )
			
			nomFichierSortie = getattr( fichier, "nomFichierSortie" )
			if( nomFichierSortie == "" ): # Si le nom du fichier de sortie n'existe pas, on l'extrait de l'URL
				nomFichierSortie = os.path.basename( getattr( fichier, "lien" ) )
			liste.insert( FICHIER_COLONNE_NOM_FICHIER_SORTIE, self.tableWidgetFichier.creerItem( nomFichierSortie ) )
			
			self.tableWidgetFichier.setLigne( ligneCourante, liste )
			ligneCourante += 1
		# On adapte la taille des colonnes
		self.tableWidgetFichier.adapterColonnes()

	######################################################
	# Methodes pour remplir la liste des telechargements #
	######################################################
	
	## Methode qui ajoute un fichier a la liste des telechargements
	# @param ligne   Numero de la ligne (dans la liste des fichiers) de l'element a ajouter
	# @param colonne Numero de colonne (inutile, juste pour le slot)
	def ajouterTelechargement( self, ligne, colonne = 0 ):
		numLigne = self.tableWidgetTelechargement.rowCount()
		# On insere une nouvelle ligne dans la liste des telechargements
		self.tableWidgetTelechargement.insertRow( numLigne )
		# On copie la ligne de fichier a telechargement
		self.tableWidgetTelechargement.setLigne( numLigne, self.tableWidgetFichier.copierLigne( ligne )
														   + [ self.tableWidgetFichier.creerItem( u"En attente de téléchargement" ) ] )
		# On adapte la taille des colonnes
		self.tableWidgetTelechargement.adapterColonnes()
	
	## Methode qui ajoute tous les fichiers a la liste des telechargements
	def ajouterTousLesFichiers( self ):
		for i in range( self.tableWidgetFichier.rowCount() ):
			self.ajouterTelechargement( i )
	
	## Methode qui supprime un fichier de la liste des telechargements
	# @param ligne   Numero de la ligne a supprimer
	# @param colonne Numero de colonne (inutile, juste pour le slot)	
	def supprimerTelechargement(  self, ligne, colonne = 0 ):
		self.tableWidgetTelechargement.removeRow( ligne )
	
	## Methode qui lance le telechargement des fichiers	
	def lancerTelechargement( self ):	
		# On liste les emissions a telecharger avec leurs numeros de ligne
		listeFichiers = []
		for i in range( self.tableWidgetTelechargement.rowCount() ): # Pour chaque ligne
			listeFichiers.append( [ i,
									qstringToString( self.tableWidgetTelechargement.item( i, TELECHARGEMENT_COLONNE_LIEN ).text() ),
									qstringToString( self.tableWidgetTelechargement.item( i, TELECHARGEMENT_COLONNE_NOM_FICHIER_SORTIE ).text() ) ] )
				
		nbATelecharger = len( listeFichiers )
		# Si on a des elements a charger
		if( nbATelecharger > 0 ):
			# On met en place la valeur du progressBar
			self.progressBarTelechargement.setMaximum( nbATelecharger )
			self.progressBarTelechargement.setValue( 0 )
			# On lance le telechargement
			threading.Thread( target = self.downloader.lancerTelechargement, args = ( listeFichiers, ) ).start()
			# On active/desactive ce qui va bien sur l'interface
			self.activerDesactiverInterface( True )
			
	## Methode qui stoppe le telechargement
	def stopperTelechargement( self ):
		# On stoppe le telechargement
		self.downloader.stopperTelechargement()

	############################################
	# Methodes pour ouvrir les autres fenetres #
	############################################
	
	#
	# Fenetre About
	#
	
	## Methode pour afficher la fenetre About
	def ouvrirFenetreAPropos( self ):
		if( self.aProposDialog == None ):
			self.aProposDialog = AProposDialog()
		self.aProposDialog.show()
		
	#
	# Fenetre de preference du logiciel
	#
	
	## Methode pour ouvrir les preferences du logiciel
	def ouvrirPreferencesLogiciel( self ):
		if( self.preferencesDialog == None ):
			self.preferencesDialog = PreferencesDialog( self.signaux )
		self.preferencesDialog.afficher()
	
	#
	# Fenetre de preference des plugins
	# 
	
	## Methode pour ouvrir les preferences du plugin courant	
	def ouvrirPreferencesPlugin( self ):
		listeOptions = self.api.getPluginListeOptions( self.nomPluginCourant )
		self.preferencesPluginDialog.ouvrirDialogPreferences( self.nomPluginCourant, listeOptions )
			
	#########
	# Slots #
	#########
	
	## Methode qui ouvre le repertoire de telechargement
	def ouvrirRepertoireTelechargement( self ):
		QtGui.QDesktopServices.openUrl( QtCore.QUrl.fromLocalFile( self.preferences.getPreference( "repertoireTelechargement" ) ) )
	
	## Methode qui rafraichit le plugin courant
	def rafraichirPlugin( self ):
		def threadRafraichirPlugin( self, nomPlugin ):
			self.signaux.signal( "debutActualisation", nomPlugin )
			self.api.pluginRafraichir( nomPlugin )
			self.signaux.signal( "finActualisation" )
			
		threading.Thread( target = threadRafraichirPlugin, args = ( self, self.nomPluginCourant ) ).start()		
	
	## Methode qui rafraichit tous les plugins
	# A utiliser au lancement du programme
	def rafraichirTousLesPlugins( self ):
		def threadRafraichirTousLesPlugins( self ):
			self.signaux.signal( "debutActualisation", "programme" )
			self.api.pluginRafraichirAuto()
			self.signaux.signal( "finActualisation" )
			self.signaux.signal( "actualiserListesDeroulantes" )
			
		threading.Thread( target = threadRafraichirTousLesPlugins, args = ( self, ) ).start()
	
	## Slot qui active/desactive des elements de l'interface pendant un telechargement
	# @param telechargementEnCours Indique si on telecharge ou pas
	def activerDesactiverInterface( self, telechargementEnCours = False ):
		# Les boutons
		self.pushButtonLancer.setEnabled( not telechargementEnCours )
		self.pushButtonStop.setEnabled( telechargementEnCours )
		self.pushButtonExtremiteMonter.setEnabled( not telechargementEnCours )
		self.pushButtonMonter.setEnabled( not telechargementEnCours )
		self.pushButtonDescendre.setEnabled( not telechargementEnCours )
		self.pushButtonExtremiteDescendre.setEnabled( not telechargementEnCours )
		self.pushButtonToutSupprimer.setEnabled( not telechargementEnCours )
		self.pushButtonNettoyer.setEnabled( not telechargementEnCours )
		
		# Le table widget
		self.tableWidgetTelechargement.setEnabled( not telechargementEnCours )

	## Slot appele lors ce qu'un le debut d'un telechargement commence
	# @param numero Position dans la liste des telechargement du telechargement qui commence
	def debutTelechargement( self, numero ):
		self.tableWidgetTelechargement.item( numero, TELECHARGEMENT_COLONNE_ETAT ).setText( stringToQstring( u"Téléchargement en cours..." ) )
		self.tableWidgetTelechargement.adapterColonnes()
		self.progressBarTelechargementFichier.setValue( 0 )

	## Slot appele lorsqu'un telechargement se finit
	# @param numero Position dans la liste des telechargement du telechargement qui se finit	
	def finTelechargement( self, numero ):
		# On ajoute le fichier a l'historique
		self.historique.ajouterHistorique( Fichier( qstringToString( self.tableWidgetTelechargement.item( numero, TELECHARGEMENT_COLONNE_EMISSION ).text() ),
													qstringToString( self.tableWidgetTelechargement.item( numero, TELECHARGEMENT_COLONNE_DATE ).text() ),
													qstringToString( self.tableWidgetTelechargement.item( numero, TELECHARGEMENT_COLONNE_LIEN ).text() ),
													qstringToString( self.tableWidgetTelechargement.item( numero, TELECHARGEMENT_COLONNE_NOM_FICHIER_SORTIE ).text() ) ) )
									
		# On modifie l'interface
		self.tableWidgetTelechargement.item( numero, TELECHARGEMENT_COLONNE_ETAT ).setText( stringToQstring( u"Fini !" ) )
		self.progressBarTelechargement.setValue( self.progressBarTelechargement.value() + 1 )
		self.tableWidgetTelechargement.adapterColonnes()
		self.progressBarTelechargementFichier.setValue( 100 )
	
	## Slot qui nettoie la liste des telechargements de tous les telechargements finis
	def nettoyer( self ):
		for i in range( self.tableWidgetTelechargement.rowCount() - 1, -1, -1 ): # [ nbLignes - 1, nbLignes - 2, ..., 1, 0 ]
			if( self.tableWidgetTelechargement.item( i, TELECHARGEMENT_COLONNE_ETAT ).text() == u"Fini !" ): # Si c'est telecharge
				self.tableWidgetTelechargement.removeRow( i )
