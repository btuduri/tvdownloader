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

from PyQt4 import QtGui, QtCore

from Preferences import Preferences
from PluginManager import PluginManager

from GUI.ConvertQString import *

##########
# Classe #
##########

## Classe qui gere le dialog des preferences du logiciel
class PreferencesDialog( QtGui.QDialog ):
	
	## Constructeur
	def __init__( self, parent ):
		
		# Appel au constructeur de la classe mere
		QtGui.QDialog.__init__( self, parent )
		
		self.preferences = Preferences()
		self.pluginManager = PluginManager()
		
		###########
		# Fenetre #
		###########
		
		###
		# Reglages de la fenetre principale
		###
		
		# Nom de la fenetre
		self.setWindowTitle( u"Préférences" )
		# Dimensions la fenetre
		self.resize( 325, 510 )
		# Mise en place de son icone
		self.setWindowIcon( QtGui.QIcon( "ico/gtk-preferences.svg" ) )
		
		###
		# Mise en place des widgets dans la fenetre
		###
		
		# Layout du dialog (il ne contiendra que la scroll area)
		self.layoutPrincipal = QtGui.QVBoxLayout( self )
		
		# Scroll Area (elle ne contiendra que le widget central)
		self.scrollArea = QtGui.QScrollArea( self )
		self.layoutPrincipal.addWidget( self.scrollArea )

		# Widget central
		self.widgetCentral = QtGui.QWidget( self.scrollArea )
		
		# Layout de grillequi contient les elements
		self.gridLayout = QtGui.QGridLayout( self.widgetCentral )
		
		# Font pour les titres
		fontTitres = QtGui.QFont()
		fontTitres.setPointSize( 11 )
		fontTitres.setWeight( 75 )
		fontTitres.setBold( True )
		
		#
		# Choix du repertoire telechargement
		#
		
		# Label
		self.labelRepertoire = QtGui.QLabel( self )
		self.labelRepertoire.setFont( fontTitres )
		self.labelRepertoire.setText( u"Répertoire de téléchargement :" )
		
		# Repertoire de telechargement
		self.lineEditRepertoireTelechargement = QtGui.QLineEdit( self )
		
		# Bouton pour ouvrir la fenetre de selection de repertoire
		self.pushButtonSelectionDossier = QtGui.QPushButton( self )
		self.pushButtonSelectionDossier.setIcon( QtGui.QIcon( "ico/gtk-folder.svg" ) )
		
		#
		# Choix du plugin par defaut
		#
		
		# Label
		self.labelPluginDefaut = QtGui.QLabel( self )
		self.labelPluginDefaut.setFont( fontTitres )
		self.labelPluginDefaut.setText( u"Plugin par défaut :" )		
		
		# Liste de choix du plugin par defaut
		self.comboBoxPluginDefaut = QtGui.QComboBox( self )
		
		#
		# Choix des plugins a activer
		#
		
		# Label
		self.labelPlugins = QtGui.QLabel( self )
		self.labelPlugins.setFont( fontTitres )
		self.labelPlugins.setText( "Plugins actifs :" )		
		
		# Liste des plugins
		self.listWidgetPlugin = QtGui.QListWidget( self )
		
		#
		# Choix des parametres Internet
		#
		
		# Label
		self.labelInternet = QtGui.QLabel( self )
		self.labelInternet.setFont( fontTitres )
		self.labelInternet.setText( u"Paramètres Internet :" )
		
		# Layout formulaire
		self.layoutInternet = QtGui.QFormLayout()
		
		# SpinBox pour choisir le timeOut
		self.spinBoxTimeOut = QtGui.QSpinBox()
		self.spinBoxTimeOut.setMinimum( 1 )
		self.spinBoxTimeOut.setMaximum( 60 )
		self.layoutInternet.addRow( u"Time out (en s) :", self.spinBoxTimeOut )
		
		# SpinBox pour choisir le nombre de threads max
		self.spinBoxNbThread = QtGui.QSpinBox()
		self.spinBoxNbThread.setMinimum( 1 )
		self.spinBoxNbThread.setMaximum( 100 )
		self.layoutInternet.addRow( u"Nombre de threads max :", self.spinBoxNbThread )
		
		# Bouton pour enregistrer/annuler les preferences
		self.buttonBox = QtGui.QDialogButtonBox( self )
		self.buttonBox.addButton( "Enregistrer", QtGui.QDialogButtonBox.AcceptRole )
		self.buttonBox.addButton( "Fermer", QtGui.QDialogButtonBox.RejectRole )
		
		# On ajoute le tout au layout
		self.gridLayout.addWidget( self.labelRepertoire, 0, 0, 1, 2 )
		self.gridLayout.addWidget( self.lineEditRepertoireTelechargement, 1, 0, 1, 1 )
		self.gridLayout.addWidget( self.pushButtonSelectionDossier, 1, 1, 1, 1 )
		self.gridLayout.addWidget( self.labelPluginDefaut, 2, 0, 1, 2 )
		self.gridLayout.addWidget( self.comboBoxPluginDefaut, 3, 0, 1, 2 )
		self.gridLayout.addWidget( self.labelPlugins, 4, 0, 1, 2 )
		self.gridLayout.addWidget( self.listWidgetPlugin, 5, 0, 1, 2 )
		self.gridLayout.addWidget( self.labelInternet, 6, 0, 1, 2 )
		self.gridLayout.addLayout( self.layoutInternet, 7, 0, 1, 2 )
		
		
		# Les boutons sont ajoutes au layout principal
		self.layoutPrincipal.addWidget( self.buttonBox )
		
		# On adapte la taille du widget
		self.widgetCentral.adjustSize()
		# On ajoute le widget central a la scroll area
		self.scrollArea.setWidget( self.widgetCentral )	
		
		###
		# Signaux provenants de l'interface
		###
		
		QtCore.QObject.connect( self.pushButtonSelectionDossier, QtCore.SIGNAL( "clicked()" ), self.afficherSelecteurDossier )
		QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL( "accepted()" ), self.enregistrerPreferences )
		QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL( "rejected()" ), self.reject )
	
	## Methode pour afficher la fenetre des preferences
	def afficher( self ):
		# On met en place dans le textEdit le repertoire
		self.lineEditRepertoireTelechargement.setText( stringToQstring( self.preferences.getPreference( "repertoireTelechargement" ) ) )
		# On met en place le plugin par defaut
		self.remplirPluginParDefaut()
		# On met en place la liste des plugins
		self.afficherPlugins()
		# On met en place les valeurs des SpinBox
		self.spinBoxTimeOut.setValue( self.preferences.getPreference( "timeOut" ) )
		self.spinBoxNbThread.setValue( self.preferences.getPreference( "nbThreadMax" ) )
		# On affiche la fenetre
		self.exec_()
	
	## Methode pour enregistrer les preferences du logiciel
	def enregistrerPreferences( self ):
		# On sauvegarde les valeurs des SpinBox
		self.preferences.setPreference( "nbThreadMax", self.spinBoxNbThread.value() )
		self.preferences.setPreference( "timeOut", self.spinBoxTimeOut.value() )
		# On sauvegarde les plugins actifs
		self.sauvegarderPlugins()
		# On sauvegarde le plugin par defaut
		self.preferences.setPreference( "pluginParDefaut", qstringToString( self.comboBoxPluginDefaut.currentText() ) )
		# On sauvegarde le repertoire de telechargement
		self.preferences.setPreference( "repertoireTelechargement", qstringToString( self.lineEditRepertoireTelechargement.text() ) )
		# On sauvegarde dans le fichier
		self.preferences.sauvegarderConfiguration()
		# On masque la fenetre
		self.hide()

	####################################################################
	# Methodes qui gerent l'emplacement de telechargement des fichiers #
	####################################################################
	
	## Methode qui affiche le selecteur de dossier
	def afficherSelecteurDossier( self ):
		rep = QtGui.QFileDialog.getExistingDirectory( None,
													  u"Sélectionnez le répertoire de téléchargement",
													  self.lineEditRepertoireTelechargement.text(),
													  QtGui.QFileDialog.ShowDirsOnly 
													)
		# Si le repertoire existe
		if( os.path.isdir( qstringToString( rep ) ) ):
			self.lineEditRepertoireTelechargement.setText( rep ) # On modifie la zone de texte qui affiche le repertoire
	
	################################################
	# Methodes qui gerent la partie plugins actifs #
	################################################
	
	## Methode qui liste les plugins actif dans le listWidgetPlugin
	def afficherPlugins( self ):
		# On recupere les listes de plugins
		listePluginsDisponibles = self.pluginManager.getListeSites()
		listePluginsDisponibles.sort() # On trie cette liste
		listePluginsActives	 = self.preferences.getPreference( "pluginsActifs" )
		
		# On remet a 0 le listWidget
		self.listWidgetPlugin.clear()
		
		# On affiche les plugins
		for plugin in listePluginsDisponibles:
			# On met en place l'item
			self.listWidgetPlugin.addItem( self.creerItem( plugin, plugin in listePluginsActives ) )
	
	## Methode qui remplie la combo box du plugin par defaut
	def remplirPluginParDefaut( self ):
		# On efface la liste
		self.comboBoxPluginDefaut.clear()
		# On ajoute les plugins actifs
		for plugin in self.preferences.getPreference( "pluginsActifs" ):
			self.comboBoxPluginDefaut.addItem( stringToQstring( plugin ) )
		# On selectionne le plugin par defaut
		index = self.comboBoxPluginDefaut.findText( stringToQstring( self.preferences.getPreference( "pluginParDefaut" ) ) )
		if( index != -1 ):
			self.comboBoxPluginDefaut.setCurrentIndex( index )
	
	## Methode qui sauvegarde les plugins actifs
	def sauvegarderPlugins( self ):
		# On liste les plugins actifs
		liste = []
		for i in range( self.listWidgetPlugin.count() ): # Pour chaque ligne
			if( self.listWidgetPlugin.item( i ).checkState() == QtCore.Qt.Checked ): # Si elle est selectionnee
				liste.append( qstringToString( self.listWidgetPlugin.item( i ).text() ) )
		# On met cela en place dans les preferences
		self.preferences.setPreference( "pluginsActifs", liste )
		# On relance l'actualisation de l'affichage
		self.emit( QtCore.SIGNAL( "actualiserListesDeroulantes()" ) )
			
	####################
	# Autres methodes #
	####################

	## Methode qui creer une element pour un listeWidget
	# @param texte    Texte de l'element
	# @param checkBox Si la checkBox de l'element est cochee ou non
	# @return L'element cree
	def creerItem( self, texte, checkBox = False ):
		# On cree l'item avec le texte
		item = QtGui.QListWidgetItem( stringToQstring( texte ) )
		# On centre le texte
		item.setTextAlignment( QtCore.Qt.AlignCenter )
		# L'item ne doit pas etre modifiable
		item.setFlags( item.flags() & ~QtCore.Qt.ItemIsEditable )
		# L'item doit avoir sa checkBox cochee ?
		if( checkBox ):
			item.setCheckState( QtCore.Qt.Checked )
		else:
			item.setCheckState( QtCore.Qt.Unchecked )
		# On renvoie l'item
		return item
