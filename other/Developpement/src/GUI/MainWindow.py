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

import threading

import Constantes

from PyQt4 import QtGui, QtCore
from GUI.Qt.MyQPushButton  import MyQPushButton
from GUI.Qt.MyQTableWidget import MyQTableWidget

from API                              import API
from Fichier                          import Fichier
from GUI.AProposDialog                import AProposDialog
from GUI.ConvertQString               import *
from GUI.Downloader                   import Downloader
from GUI.FenetreAttenteProgressDialog import FenetreAttenteProgressDialog
from GUI.PreferencePluginDialog       import PreferencePluginDialog
from GUI.PreferencesDialog            import PreferencesDialog
from GUI.UpdateManagerDialog          import UpdateManagerDialog
from Historique                       import Historique
from PluginManager                    import PluginManager
from Preferences                      import Preferences

import logging
logger = logging.getLogger( __name__ )

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
		self.setWindowTitle( "%s %s" %( Constantes.TVD_NOM, Constantes.TVD_VERSION ) )
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
		# Onglets
		#
		
		# Gestionnaire onglets
		self.tabWidget = QtGui.QTabWidget( self.centralWidget )
		
		# Onglet Fichiers
		self.tabFichiers = QtGui.QSplitter( self.centralWidget ) # L'onglet Fichier contient un splitter
		self.tabWidget.addTab( self.tabFichiers, u"Choix des fichiers" )
		
		# Onglet Telechargements
		self.tabTelechargements = QtGui.QWidget( self.centralWidget )
		self.tabWidget.addTab( self.tabTelechargements, u"Téléchargements" )
		
		#
		# Liste des fichiers
		#
		
		# Layout de grille qui contient le tableau qui liste les fichiers et ses boutons
		self.gridLayoutFichiers = QtGui.QGridLayout( self.tabFichiers )
		
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
		# La liste est triable
		#~ self.tableWidgetFichier.setSortingEnabled( True )
		# On l'ajoute au layout
		self.gridLayoutFichiers.addWidget( self.tableWidgetFichier, 0, 1, 6, 1 )
		
		# Icones du tableWidget
		self.iconeFichier     = QtGui.QIcon( "ico/gtk-file.svg" )
		self.iconeAjoute      = QtGui.QIcon( "ico/gtk-add.svg" )
		self.iconeTelecharge  = QtGui.QIcon( "ico/gtk-apply.svg" )
		
		# Bouton pour ajouter tous les fichiers a la liste des telechargements
		self.pushButtonToutAjouter = MyQPushButton( self.tabFichiers )
		self.pushButtonToutAjouter.setIcon( QtGui.QIcon( "ico/gtk-add.svg" ) )
		self.pushButtonToutAjouter.setToolTip( u"Ajouter tous les fichiers à la liste des téléchargements" )
		self.gridLayoutFichiers.addWidget( self.pushButtonToutAjouter, 0, 0, 2, 1 )
		
		# Bouton pour rafraichir le plugin courant
		self.pushButtonRafraichirPlugin = MyQPushButton( self.tabFichiers )
		self.pushButtonRafraichirPlugin.setIcon( QtGui.QIcon( "ico/gtk-refresh.svg" ) )
		self.pushButtonRafraichirPlugin.setToolTip( "Rafraichir le plugin" )
		self.gridLayoutFichiers.addWidget( self.pushButtonRafraichirPlugin, 2, 0, 2, 1 )

		# Bouton pour ouvrir la fenetre des preferences du plugin courant
		self.pushButtonPreferencesPlugin = MyQPushButton( self.tabFichiers )
		self.pushButtonPreferencesPlugin.setIcon( QtGui.QIcon( "ico/gtk-preferences.svg" ) )
		self.pushButtonPreferencesPlugin.setToolTip( u"Ouvrir les préférences du plugin" )
		self.gridLayoutFichiers.addWidget( self.pushButtonPreferencesPlugin, 4, 0, 2, 1 )
		
		# On met en place ce layout sur un widget (pour le splitter)
		self.widgetFichiers = QtGui.QWidget( self.tabFichiers )
		self.widgetFichiers.setLayout( self.gridLayoutFichiers )
		
		#
		# Descriptif des fichiers
		#
		
		# Splitter pour separer image et texte
		self.splitterDescriptif = QtGui.QSplitter( self.tabFichiers )
		
		# Label pour afficher un logo
		self.logoFichierDefaut = QtGui.QPixmap()
		self.logoFichierDefaut.load( "img/gtk-dialog-question.svg" )
		
		self.labelLogo = QtGui.QLabel( self.tabFichiers )
		self.labelLogo.setScaledContents( True )
		self.labelLogo.setPixmap( self.logoFichierDefaut.scaled( QtCore.QSize( 150, 150 ), QtCore.Qt.KeepAspectRatio ) )
		self.splitterDescriptif.addWidget( self.labelLogo )
		
		# Zone de texte pour afficher un descriptif
		self.plainTextEdit = QtGui.QPlainTextEdit( self.tabFichiers )
		self.splitterDescriptif.addWidget( self.plainTextEdit )
		

		# Onrientation verticale du splitter
		self.tabFichiers.setOrientation( QtCore.Qt.Vertical )
		
		# On ajoute les 2 elements au splitter (qui est notre onglet)
		self.tabFichiers.addWidget( self.widgetFichiers )
		self.tabFichiers.addWidget( self.splitterDescriptif )
		
		#
		# Liste des telechargements
		#
		
		# Layout de grille qui contient le tableau qui liste les fichiers a telecharger + les boutons pour le controller
		self.gridLayoutTelechargement = QtGui.QGridLayout( self.tabTelechargements )
		
		# Tableau qui contient la liste des fichiers a telecharger
		self.tableWidgetTelechargement = MyQTableWidget( self.tabTelechargements, True )
		# Il a 3 colonnes et 0 ligne (pour l'instant)
		self.tableWidgetTelechargement.setColumnCount( 3 )
		self.tableWidgetTelechargement.setRowCount( 0 )
		# On ajoute le titre des 3 colonnes
		self.tableWidgetTelechargement.setHorizontalHeaderItem( 0,
																self.tableWidgetTelechargement.creerItem( "Date" ) )
		self.tableWidgetTelechargement.setHorizontalHeaderItem( 1,
																self.tableWidgetTelechargement.creerItem( "Emission" ) )
		self.tableWidgetTelechargement.setHorizontalHeaderItem( 2,
																self.tableWidgetTelechargement.creerItem( "Etat" ) )
		# On l'ajoute au layout
		self.gridLayoutTelechargement.addWidget( self.tableWidgetTelechargement, 0, 1, 2, 1 )
		
		# Bouton pour supprimer tous les elements de la liste
		self.pushButtonToutSupprimer = MyQPushButton( self.tabTelechargements )
		self.pushButtonToutSupprimer.setIcon( QtGui.QIcon( "ico/gtk-cancel.svg" ) )
		self.pushButtonToutSupprimer.setToolTip( u"Supprimer tous les téléchargements de la liste" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonToutSupprimer, 0, 0, 1, 1 )
		
		# Bouton pour ouvrir le dossier des telechargements
		self.pushButtonOuvrirDossierTelechargement = MyQPushButton( self.tabTelechargements )
		self.pushButtonOuvrirDossierTelechargement.setIcon( QtGui.QIcon( "ico/gtk-folder.svg" ) )
		self.pushButtonOuvrirDossierTelechargement.setToolTip( u"Ouvrir le dossier des téléchargements" )
		self.gridLayoutTelechargement.addWidget( self.pushButtonOuvrirDossierTelechargement, 1, 0, 1, 1 )
		
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
		# On ajoute le gestionnaire d'onglets
		self.gridLayout.addWidget( self.tabWidget, 1, 0, 1, 3 )
		# On ajoute la barre de progression de telechargement d'un fichier
		self.gridLayout.addWidget( self.progressBarTelechargementFichier, 2, 0, 1, 3 )
		# On ajoute la barre de progression de telechargement des fichiers
		self.gridLayout.addWidget( self.progressBarTelechargement, 3, 0, 1, 3 )
		# On ajoute les boutons ajouter/supprimer/lancer
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
	
		################################################
		# Instanciations + initialisation de variables #
		################################################
		
		# Fenetre About
		self.aProposDialog = None
		# Fenetre des preferences du logiciel
		self.preferencesDialog = None
		# Fenetre de mise a jour des plugins
		self.updateManagerDialog = None
		# Nom plugin courant
		self.nomPluginCourant = ""
		# Cache des images descriptive
		# Clef : urlImage Valeur : image (binaire)
		self.cacheImage = {}
		
		# On instancie le gestionnaire de preferences
		self.preferences = Preferences()
		# On instancie le gestionnaire de preferences des plugins
		self.preferencesPluginDialog = PreferencePluginDialog( self )
		# On instancie le gestionnaire de download
		self.downloader = Downloader()	
		# On recupere l'instance de API
		self.api = API.getInstance()
		# On instancie le gestionnaire d'historique
		self.historique = Historique()
		# On instancie la fenetre d'attente
		self.fenetreAttenteProgressDialog = FenetreAttenteProgressDialog( self )
		# On instancie le gest								 
		
		#
		# Fenetre de confirmation pour quitter le logiciel
		#
		self.quitterMessageBox = QtGui.QMessageBox( self )
		self.quitterMessageBox.setWindowTitle( "Fermeture de TVDownloader" )
		self.quitterMessageBox.setText( u"Voulez-vous réellement quitter TVDownloader ?" )
		self.quitterMessageBox.setInformativeText( u"Votre liste de téléchargement sera perdue" )
		self.quitterMessageBox.addButton( "Oui", QtGui.QMessageBox.AcceptRole )
		self.quitterMessageBox.addButton( "Non", QtGui.QMessageBox.RejectRole )
		
		###########
		# Signaux #
		###########

		QtCore.QObject.connect( self.comboBoxSite,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerChaines )
		
		QtCore.QObject.connect( self.comboBoxChaine,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerEmissions )
		
		QtCore.QObject.connect( self.comboBoxEmission,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerFichiers )

		QtCore.QObject.connect( self.tableWidgetFichier,
								QtCore.SIGNAL( "cellClicked(int,int)" ),
								self.afficherInformationsFichier )	
		
		QtCore.QObject.connect( self.tableWidgetFichier,
								QtCore.SIGNAL( "cellDoubleClicked(int,int)" ),
								self.gererTelechargement )	
								
		QtCore.QObject.connect( self.pushButtonToutAjouter,
								QtCore.SIGNAL( "clicked()" ),
								self.ajouterTousLesFichiers )								

		QtCore.QObject.connect( self.pushButtonRafraichirPlugin,
								QtCore.SIGNAL( "clicked()" ),
								self.rafraichirPlugin )

		QtCore.QObject.connect( self.pushButtonPreferencesPlugin,
								QtCore.SIGNAL( "clicked()" ),
								self.ouvrirPreferencesPlugin )

		QtCore.QObject.connect( self.tableWidgetTelechargement,
								QtCore.SIGNAL( "cellDoubleClicked(int,int)" ),
								self.supprimerTelechargement )	
		
		QtCore.QObject.connect( self.pushButtonToutSupprimer,
								QtCore.SIGNAL( "clicked()" ),
								self.supprimerTousLesTelechargements )

		QtCore.QObject.connect( self.pushButtonOuvrirDossierTelechargement,
								QtCore.SIGNAL( "clicked()" ),
								self.ouvrirRepertoireTelechargement )
		
		QtCore.QObject.connect( self.pushButtonLancer,
								QtCore.SIGNAL( "clicked()" ),
								self.lancerTelechargement )

		QtCore.QObject.connect( self.pushButtonStop,
								QtCore.SIGNAL( "clicked()" ),
								self.stopperTelechargement )

		QtCore.QObject.connect( self.actionQuitter,
								QtCore.SIGNAL( "triggered()" ),
								self.close )

		QtCore.QObject.connect( self.actionMAJ,
								QtCore.SIGNAL( "triggered()" ),
								self.ouvrirFenetreMiseAJour )

		QtCore.QObject.connect( self.actionPreferences,
								QtCore.SIGNAL( "triggered()" ),
								self.ouvrirPreferencesLogiciel )

		QtCore.QObject.connect( self.actionAPropos,
								QtCore.SIGNAL( "triggered()" ),
								self.ouvrirFenetreAPropos )
		
		QtCore.QObject.connect( self, QtCore.SIGNAL( "listeChaines(PyQt_PyObject)" ) , self.ajouterChaines )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "listeEmissions(PyQt_PyObject)" ) , self.ajouterEmissions )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "listeFichiers(PyQt_PyObject)" ) , self.ajouterFichiers )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "nouvelleImage(PyQt_PyObject)" ) , self.mettreEnPlaceImage )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ) , self.fenetreAttenteProgressDialog.ouvrirFenetreAttente )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "finActualisation()" ) , self.fenetreAttenteProgressDialog.fermerFenetreAttente )		
		QtCore.QObject.connect( self, QtCore.SIGNAL( "actualiserListesDeroulantes()" ) , self.actualiserListesDeroulantes )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "debutTelechargement(PyQt_PyObject)" ) , self.debutTelechargement )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "finTelechargement(PyQt_PyObject,bool)" ) , self.finTelechargement )
		QtCore.QObject.connect( self, QtCore.SIGNAL( "finDesTelechargements()" ) , self.activerDesactiverInterface )
		
		QtCore.QObject.connect( self.downloader, QtCore.SIGNAL( "pourcentageFichier(int)" ) , self.progressBarTelechargementFichier.setValue )

		#########
		# Début #
		#########			
		
		# La fenetre prend la dimension qu'elle avait a sa fermeture
		taille = self.preferences.getPreference( "tailleFenetre" )
		self.resize( taille[ 0 ], taille[ 1 ] )
		
		# Si aucun plugin n'est active, on ouvre la fenetre des preferences
		if( len( self.preferences.getPreference( "pluginsActifs" ) ) == 0 ):
			self.ouvrirPreferencesLogiciel()
		
		# On actualise tous les plugins
		self.rafraichirTousLesPlugins()

	## Methode qui execute les actions necessaires avant de quitter le programme
	def actionsAvantQuitter( self ):
		# On sauvegarde les options des plugins
		self.api.fermeture()
		# On sauvegarde la taille de la fenetre
		taille = self.size()
		self.preferences.setPreference( "tailleFenetre", [ taille.width(), taille.height() ] )
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
			self.emit( QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ), nomPlugin )
			try:
				listeChaines = self.api.getPluginListeChaines( nomPlugin )
			except:
				listeChaines = []
				logger.error( u"impossible de récupérer la liste des chaines de %s" %( nomPlugin ) )
			self.emit( QtCore.SIGNAL( "listeChaines(PyQt_PyObject)" ), listeChaines )
			self.emit( QtCore.SIGNAL( "finActualisation()" ) )
			
		if( site != "" ):
			self.nomPluginCourant = qstringToString( site )
			threading.Thread( target = threadListerChaines, args = ( self, self.nomPluginCourant ) ).start()
			# On active (ou pas) le bouton de preference du plugin
			self.pushButtonPreferencesPlugin.setEnabled( self.api.getPluginListeOptions( self.nomPluginCourant ) != [] )
		
	## Methode qui lance le listage des emissions
	# @param chaine Nom de la chaine pour laquelle on va lister les emissions
	def listerEmissions( self, chaine ):
		def threadListerEmissions( self, nomPlugin, chaine ):
			self.emit( QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ), nomPlugin )
			try:
				listeEmissions = self.api.getPluginListeEmissions( nomPlugin, chaine )
			except:
				listeEmissions = []
				logger.error( u"impossible de récupérer la liste des emissions de %s" %( nomPlugin ) )
			self.emit( QtCore.SIGNAL( "listeEmissions(PyQt_PyObject)" ), listeEmissions )
			self.emit( QtCore.SIGNAL( "finActualisation()" ) )
			
		if( chaine != "" ):
			threading.Thread( target = threadListerEmissions, args = ( self, self.nomPluginCourant, qstringToString( chaine ) ) ).start()
		
	## Methode qui lance le listage des fichiers
	# @param emission Nom de l'emission pour laquelle on va lister les fichiers
	def listerFichiers( self, emission ):
		def threadListerFichiers( self, nomPlugin, emission ):
			self.emit( QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ), nomPlugin )
			try:
				listeFichiers = self.api.getPluginListeFichiers( nomPlugin, emission )
			except:
				listeFichiers = []
				logger.error( u"impossible de récupérer la liste des fichiers de %s" %( nomPlugin ) )
			self.emit( QtCore.SIGNAL( "listeFichiers(PyQt_PyObject)" ), listeFichiers )
			self.emit( QtCore.SIGNAL( "finActualisation()" ) )
			
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
		# On selectionne par defaut celui choisis dans les preference
		index = self.comboBoxSite.findText( stringToQstring( self.preferences.getPreference( "pluginParDefaut" ) ) )
		if( index != -1 ):
			self.comboBoxSite.setCurrentIndex( index )
		# On lance l'ajout des chaines
		self.listerChaines( self.comboBoxSite.currentText() )
	
	## Methode qui met en place une liste de chaines sur l'interface
	# @param listeChaines Liste des chaines a mettre en place
	def ajouterChaines( self, listeChaines ):
		# On trie la liste des chaines
		listeChaines.sort()
		# On efface la liste des chaines
		self.comboBoxChaine.clear()
		# On efface la liste des emissions
		self.comboBoxEmission.clear()
		# On efface la liste des fichiers
		self.tableWidgetFichier.toutSupprimer()		
		# On met en place les chaines
		for chaine in listeChaines:
			self.comboBoxChaine.addItem( stringToQstring( chaine ) )
		# Si on a juste une seule chaine
		if( self.comboBoxChaine.count() == 1 ):
			# On lance l'ajout des emissions
			self.listerEmissions( self.comboBoxChaine.currentText() )
		else:
			# On ne selectionne pas de chaine
			self.comboBoxChaine.setCurrentIndex( -1 )			

	## Methode qui met en place une liste d'emissions sur l'interface
	# @param listeEmissions Liste des emissions a mettre en place	
	def ajouterEmissions( self, listeEmissions ):
		# On trie la liste des emissions
		listeEmissions.sort()
		# On efface la liste des emissions
		self.comboBoxEmission.clear()
		# On efface la liste des fichiers
		self.tableWidgetFichier.toutSupprimer()
		# On met en place la liste des emissions
		for emission in listeEmissions:
			self.comboBoxEmission.addItem( stringToQstring( emission ) )
		# Si on a juste une seule emission
		if( self.comboBoxEmission.count() == 1 ):
			# On lance l'ajout des fichiers
			self.listerFichiers( self.comboBoxEmission.currentText() )
		else:
			# On ne selectionne pas d'emission
			self.comboBoxEmission.setCurrentIndex( -1 )
	
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
			# On ajoute les informations au tableWidgetFichier
			liste = []
			liste.append( self.tableWidgetFichier.creerItem( "" ) )
			liste.append( self.tableWidgetFichier.creerItem( getattr( fichier, "date" ) ) )
			liste.append( self.tableWidgetFichier.creerItem( getattr( fichier, "nom" ) ) )
			self.tableWidgetFichier.setLigne( ligneCourante, [ liste, fichier ] )
			# On met en place l'icone qui va bien
			self.gererIconeListeFichier( fichier )
			ligneCourante += 1
		# On adapte la taille des colonnes
		self.tableWidgetFichier.adapterColonnes()

	## Methode qui rafraichit le plugin courant
	def rafraichirPlugin( self ):
		def threadRafraichirPlugin( self, nomPlugin ):
			self.emit( QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ), nomPlugin )
			try:
				self.api.pluginRafraichir( nomPlugin )
			except:
				logger.error( "impossible de rafraichir le plugin %s" %( nomPlugin ) )
			self.emit( QtCore.SIGNAL( "finActualisation()" ) )
			
		threading.Thread( target = threadRafraichirPlugin, args = ( self, self.nomPluginCourant ) ).start()	

	## Methode qui met en place l'image de la description d'un fichier
	# @param image Image a mettre en place (binaire)
	def mettreEnPlaceImage( self, image ):
		logoFichier = QtGui.QPixmap()
		logoFichier.loadFromData( image )
		self.labelLogo.setPixmap( logoFichier.scaled( QtCore.QSize( 150, 150 ), QtCore.Qt.KeepAspectRatio ) )
	
	## Methode qui affiche des informations sur le fichier selectionne	
	def afficherInformationsFichier( self, ligne, colonne ):
		def threadRecupererImage( self, urlImage ):
			image = self.api.getPicture( urlImage )
			if( image != "" ):
				self.cacheImage[ urlImage ] = image
				self.emit( QtCore.SIGNAL( "nouvelleImage(PyQt_PyObject)" ), image )
			else:
				# Afficher image par defaut
				pass
		
		fichier = self.tableWidgetFichier.getClasse( ligne )
		# On recupere le lien de l'image et le texte descriptif
		urlImage        = getattr( fichier, "urlImage" )
		texteDescriptif = getattr( fichier, "descriptif" )
		
		self.plainTextEdit.clear()
		# Si on a un texte descriptif, on l'affiche
		if( texteDescriptif != "" ):
			self.plainTextEdit.appendPlainText( stringToQstring( texteDescriptif ) )
		else:
			self.plainTextEdit.appendPlainText( u"Aucune information disponible" )
		
		# Si on n'a pas d'image
		if( urlImage == "" ):
			# On met en place celle par defaut
			self.logoFichier = self.logoFichierDefaut
			self.labelLogo.setPixmap( self.logoFichier.scaled( QtCore.QSize( 150, 150 ), QtCore.Qt.KeepAspectRatio ) )
		else: # Si on en a une
			# Si elle est dans le cache des images
			if( self.cacheImage.has_key( urlImage ) ):
				self.mettreEnPlaceImage( self.cacheImage[ urlImage ] )
			else: # Sinon
				# On lance le thread pour la recuperer
				threading.Thread( target = threadRecupererImage, args = ( self, urlImage ) ).start()

	## Methode qui gere l'icone d'un fichier dans la liste des telechargements
	# Il y a 3 icones possible :
	#  - C'est un fichier
	#  - C'est un fichier present dans l'historique (donc deja telecharge)
	#  - C'est un fichier present dans la liste des telechargements
	# @param fichier Fichier a gerer
	def gererIconeListeFichier( self, fichier ):
		if( fichier in self.tableWidgetFichier.getListeClasse() ):
			ligneFichier = self.tableWidgetFichier.getListeClasse().index( fichier )
			# On cherche quel icone mettre en place
			if( fichier in self.tableWidgetTelechargement.getListeClasse() ):
				icone = self.iconeAjoute
			elif( self.historique.comparerHistorique( fichier ) ):
				icone = self.iconeTelecharge
			else:
				icone = self.iconeFichier
			# On met en place l'icone
			self.tableWidgetFichier.item( ligneFichier, 0 ).setIcon( icone )	

	######################################################
	# Methodes pour remplir la liste des telechargements #
	######################################################
	
	## Methode qui gere la liste des telechargements
	# @param ligne   Numero de la ligne (dans la liste des fichiers) de l'element a ajouter
	# @param colonne Numero de colonne (inutile, juste pour le slot)
	def gererTelechargement( self, ligne, colonne = 0 ):
		fichier = self.tableWidgetFichier.getClasse( ligne )
		# Si le fichier est deja dans la liste des telechargements
		if( fichier in self.tableWidgetTelechargement.getListeClasse() ):
			ligneTelechargement = self.tableWidgetTelechargement.getListeClasse().index( fichier )
			self.supprimerTelechargement( ligneTelechargement )
		else: # S'il n'y est pas, on l'ajoute
			numLigne = self.tableWidgetTelechargement.rowCount()
			# On insere une nouvelle ligne dans la liste des telechargements
			self.tableWidgetTelechargement.insertRow( numLigne )
			# On y insere les elements qui vont biens
			self.tableWidgetTelechargement.setLigne( numLigne, 
													 [ 
													  [ self.tableWidgetTelechargement.creerItem( getattr( fichier, "date" ) ),
													    self.tableWidgetTelechargement.creerItem( getattr( fichier, "nom" ) ),
													    self.tableWidgetTelechargement.creerItem( u"En attente de téléchargement" )
													  ],
													  fichier
													 ]
												   )
			# On adapte la taille des colonnes
			self.tableWidgetTelechargement.adapterColonnes()
			# On modifie l'icone dans la liste des fichiers
			self.gererIconeListeFichier( fichier )
	
	## Methode qui ajoute tous les fichiers a la liste des telechargements
	def ajouterTousLesFichiers( self ):
		for i in range( self.tableWidgetFichier.rowCount() ):
			self.gererTelechargement( i )
	
	## Methode qui supprime un fichier de la liste des telechargements
	# @param ligne   Numero de la ligne a supprimer
	# @param colonne Numero de colonne (inutile, juste pour le slot)	
	def supprimerTelechargement(  self, ligne, colonne = 0 ):
		fichier = self.tableWidgetTelechargement.getClasse( ligne )
		# On supprime l'element du tableWidgetTelechargement
		self.tableWidgetTelechargement.supprimerLigne( ligne )
		# On modifie l'icone dans la liste des fichiers
		self.gererIconeListeFichier( fichier )
	
	## Methode qui supprime tous les telechargement de la liste des telechargements
	def supprimerTousLesTelechargements( self ):
		for i in range( self.tableWidgetTelechargement.rowCount() -1, -1, -1 ):
			self.supprimerTelechargement( i )
		
	## Methode qui lance le telechargement des fichiers	
	def lancerTelechargement( self ):	
		def threadTelechargement( self, listeFichiers ):
			for fichier in listeFichiers:
				# On debute un telechargement
				self.emit( QtCore.SIGNAL( "debutTelechargement(PyQt_PyObject)" ), fichier )
				# On le lance
				retour = self.downloader.telecharger( fichier )
				# On a fini le telechargement
				self.emit( QtCore.SIGNAL( "finTelechargement(PyQt_PyObject,bool)" ), fichier, retour )
			# On a fini les telechargements
			self.emit( QtCore.SIGNAL( "finDesTelechargements()" ) )	
		
		# On liste les fichiers a telecharger
		listeFichiers = []
		for i in range( self.tableWidgetTelechargement.rowCount() ): # Pour chaque ligne
			listeFichiers.append( self.tableWidgetTelechargement.getClasse( i ) )
		nbATelecharger = len( listeFichiers )	
		
		# Si on a des elements a charger
		if( nbATelecharger > 0 ):
			# On met en place la valeur du progressBar
			self.progressBarTelechargement.setMaximum( nbATelecharger )
			self.progressBarTelechargement.setValue( 0 )
			# On active/desactive ce qui va bien sur l'interface
			self.activerDesactiverInterface( True )
			# On lance le telechargement
			threading.Thread( target = threadTelechargement, args = ( self, listeFichiers ) ).start()
			
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
			# On cree l'instance
			self.preferencesDialog = PreferencesDialog( self )
			# On connecte le signal qui va bien
			QtCore.QObject.connect( self.preferencesDialog, QtCore.SIGNAL( "actualiserListesDeroulantes()" ) , self.actualiserListesDeroulantes )
		self.preferencesDialog.afficher()
	
	#
	# Fenetre de mise a jour des plugins
	#
	
	## Methode pour ouvrir la fenetre de mise a jour des plugins
	def ouvrirFenetreMiseAJour( self ):
		if( self.updateManagerDialog == None ):
			self.updateManagerDialog = UpdateManagerDialog( self )
		self.updateManagerDialog.afficher()	
	
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
		QtGui.QDesktopServices.openUrl( QtCore.QUrl.fromLocalFile( stringToQstring( self.preferences.getPreference( "repertoireTelechargement" ) ) ) )
	
	## Methode qui rafraichit le plugin courant
	def rafraichirPlugin( self ):
		def threadRafraichirPlugin( self, nomPlugin ):
			self.emit( QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ), nomPlugin )
			self.api.pluginRafraichir( nomPlugin )
			self.emit( QtCore.SIGNAL( "finActualisation()" ) )
			
		threading.Thread( target = threadRafraichirPlugin, args = ( self, self.nomPluginCourant ) ).start()		
	
	## Methode qui rafraichit tous les plugins
	# A utiliser au lancement du programme
	def rafraichirTousLesPlugins( self ):
		def threadRafraichirTousLesPlugins( self ):
			self.emit( QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ), "TVDownloader" )
			self.api.pluginRafraichirAuto()
			self.emit( QtCore.SIGNAL( "finActualisation()" ) )
			self.emit( QtCore.SIGNAL( "actualiserListesDeroulantes()" ) )
			
		threading.Thread( target = threadRafraichirTousLesPlugins, args = ( self, ) ).start()
	
	## Slot qui active/desactive des elements de l'interface pendant un telechargement
	# @param telechargementEnCours Indique si on telecharge ou pas
	def activerDesactiverInterface( self, telechargementEnCours = False ):
		# Les boutons
		self.pushButtonLancer.setEnabled( not telechargementEnCours )
		self.pushButtonStop.setEnabled( telechargementEnCours )
		self.pushButtonToutSupprimer.setEnabled( not telechargementEnCours )
		
		# Le table widget
		self.tableWidgetTelechargement.setEnabled( not telechargementEnCours )

	## Slot appele lors ce qu'un le debut d'un telechargement commence
	# @param fichier Fichier dont le telechargement vient de commencer
	def debutTelechargement( self, fichier ):
		ligneTelechargement = self.tableWidgetTelechargement.getListeClasse().index( fichier )
		self.tableWidgetTelechargement.item( ligneTelechargement, 2 ).setText( stringToQstring( u"Téléchargement en cours..." ) )
		self.tableWidgetTelechargement.adapterColonnes()
		self.progressBarTelechargementFichier.setValue( 0 )

	## Slot appele lorsqu'un telechargement se finit
	# @param fichier Fichier du telechargement qui vient de se finir
	# @param reussi  Indique si le telechargement s'est fini sans problemes
	def finTelechargement( self, fichier, reussi = True ):
		ligneTelechargement = self.tableWidgetTelechargement.getListeClasse().index( fichier )
		# On ajoute le fichier a l'historique
		self.historique.ajouterHistorique( fichier )
		# On modifie l'icone dans la liste des fichiers
		self.gererIconeListeFichier( fichier )	
		# On modifie l'interface
		self.tableWidgetTelechargement.item( ligneTelechargement, 2 ).setText( stringToQstring( u"Fini !" ) )
		self.progressBarTelechargement.setValue( self.progressBarTelechargement.value() + 1 )
		self.tableWidgetTelechargement.adapterColonnes()
		self.progressBarTelechargementFichier.setValue( 100 )
