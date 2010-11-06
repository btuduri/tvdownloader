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
from GUI.Signaux import Signaux

##########
# Classe #
##########

## Classe qui gere le dialog des preferences du logiciel
class PreferencesDialog( QtGui.QDialog ):
	
	## Constructeur
	# @param signaux Lanceur de signaux
	def __init__( self, signaux ):
		
		# Appel au constructeur de la classe mere
		QtGui.QDialog.__init__( self )
		
		self.preferences = Preferences()
		self.pluginManager = PluginManager()
		self.signaux = signaux
		
		###########
		# Fenetre #
		###########
		
		###
		# Reglages de la fenetre principale
		###
		
		# Nom de la fenetre
		self.setWindowTitle( u"Préférences" )
		# Dimensions la fenetre
		self.resize( 280, 340 )
		# Mise en place de son icone
		self.setWindowIcon( QtGui.QIcon( "ico/gtk-preferences.svg" ) )
		
		###
		# Mise en place des widgets dans la fenetre
		###
		
		# Layout de grille principal
		self.gridLayout = QtGui.QGridLayout( self )
		
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
		# Choix des plugins a activer
		#
		
		# Label
		self.labelPLugins = QtGui.QLabel( self )
		self.labelPLugins.setFont( fontTitres )
		self.labelPLugins.setText( "Plugins actifs :" )		
		
		# Liste des plugins
		self.listWidgetPlugin = QtGui.QListWidget( self )
		
		
		
		# Bouton pour enregistrer/annuler les preferences
		self.buttonBox = QtGui.QDialogButtonBox( self )
		self.buttonBox.addButton( "Enregistrer", QtGui.QDialogButtonBox.AcceptRole )
		self.buttonBox.addButton( "Fermer", QtGui.QDialogButtonBox.RejectRole )
		
		# On ajoute le tout au layout
		self.gridLayout.addWidget( self.labelRepertoire, 0, 0, 1, 2 )
		self.gridLayout.addWidget( self.lineEditRepertoireTelechargement, 1, 0, 1, 1 )
		self.gridLayout.addWidget( self.pushButtonSelectionDossier, 1, 1, 1, 1 )
		self.gridLayout.addWidget( self.labelPLugins, 2, 0, 1, 1 )
		self.gridLayout.addWidget( self.listWidgetPlugin, 3, 0, 1, 2 )
		self.gridLayout.addWidget( self.buttonBox, 4, 0, 1, 2 )
		
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
		# On met en place la liste des plugins
		self.afficherPlugins()
		# On affiche la fenetre
		self.exec_()
	
	## Methode pour enregistrer les preferences du logiciel
	def enregistrerPreferences( self ):
		# On sauvegarde les plugins actifs
		self.sauvegarderPlugins()
		# On sauivegarde le repertoire de telechargement
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
		if( os.path.isdir( rep ) ):
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
		self.signaux.signal( "actualiserListesDeroulantes" )
			
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
