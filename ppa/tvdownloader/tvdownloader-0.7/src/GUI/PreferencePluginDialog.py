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

import logging
logger = logging.getLogger( __name__ )

from PyQt4 import QtGui, QtCore

from GUI.ConvertQString import *
from API import API
from Option import Option

##########
# Classe #
##########

## Classe qui gere l'affichage des fenetres de dialog pour les preferences des plugins
class PreferencePluginDialog:
	
	OPTION_TEXTE      = 0
	OPTION_CHECKBOX   = 1
	OPTION_LISTE      = 2
	OPTION_COMBOBOX   = 3
	
	## Constructeur
	# @param parent Fenetre parent (MainWindow)
	def __init__( self, parent ):
		self.parent = parent # Dans ce cas, parent = MainWindow
		self.api    = API.getInstance()
	
	##########################################################################
	# Fonctions pour creer le dialog, l'afficher et en recuperer les valeurs #
	##########################################################################

	## Methode qui ouvre la fenetre de preference d'un plugin
	# @param nomPlugin    Nom du plugin pour lequel on va ouvrir la fenetre
	# @param listeOptions Listes des options du plugin
	def ouvrirDialogPreferences( self, nomPlugin, listeOptions ):
		self.nomPluginCourant = nomPlugin
		self.initDialogPreferences( nomPlugin, listeOptions )
		self.dialogPreferences.exec_()

	## Methode pour creer la fenetre de preference d'un plugin
	# @param nomPlugin    Nom du plugin pour lequel on va creer la fenetre
	# @param listeOptions Listes des options du plugin
	def initDialogPreferences( self, nomPlugin, listeOptions ):
		# On cree un nouveau dialog
		self.dialogPreferences = QtGui.QDialog( self.parent )
		# On met le nom du plugin dans le titre de la fenetre
		self.dialogPreferences.setWindowTitle( stringToQstring( u"Préférences de %s" %( nomPlugin ) ) )
		# Change la taille
		self.dialogPreferences.resize( 500, 340 )
		
		# La liste des widgets est vide
		self.listeWidget       = []		
		
		# Layout du dialog (il ne contiendra que la scroll area)
		self.layoutPrincipal = QtGui.QVBoxLayout()
		
		# Scroll Area (elle ne contiendra que le widget centreal )
		self.scrollArea = QtGui.QScrollArea()
		self.layoutPrincipal.addWidget( self.scrollArea )

		# Widget central
		self.widgetCentral = QtGui.QWidget()

		# On cree un layout de grille (layout du widget central)
		self.layoutGrille  = QtGui.QGridLayout()
		
		# On ajoute les options
		for option in listeOptions:
			typeOption      = getattr( option, "type" )
			nomOption       = getattr( option, "nom" )
			texteDescriptif = getattr( option, "description" )
			valeurParDefaut = getattr( option, "valeur" )
			valeurs         = getattr( option, "choix", None )
			
			if( typeOption == Option.TYPE_TEXTE ):
				self.ajoutTexte( nomOption, texteDescriptif, valeurParDefaut )
			elif( typeOption == Option.TYPE_BOULEEN ):
				self.ajoutCheckBox( nomOption, texteDescriptif, valeurParDefaut )
			elif( typeOption == Option.TYPE_CHOIX_MULTIPLE ):
				valeursBonFormat = []
				for val in valeurs:
					valeursBonFormat.append( [ val, val in valeurParDefaut ] )
				self.ajoutListe( nomOption, texteDescriptif, valeursBonFormat )
			elif( typeOption == Option.TYPE_CHOIX_UNIQUE ):
				self.ajoutComboBox( nomOption, texteDescriptif, valeurs, valeurParDefaut )
			else:
				logger.warn( "type d'option inconnu" )
		
		# On ajoute les bouton Sauvegarder et Annuler
		buttonBox = QtGui.QDialogButtonBox( self.dialogPreferences )
		buttonBox.addButton( "Sauvegarder", QtGui.QDialogButtonBox.AcceptRole )
		buttonBox.addButton( "Annuler",     QtGui.QDialogButtonBox.RejectRole )
		self.layoutPrincipal.addWidget( buttonBox )
		# On connecte les signaux
		QtCore.QObject.connect( buttonBox, QtCore.SIGNAL( "accepted()" ), self.sauvegarderPreferences )
		QtCore.QObject.connect( buttonBox, QtCore.SIGNAL( "rejected()" ), self.dialogPreferences.reject )
		
		# Le widget central contient le layout de grille
		self.widgetCentral.setLayout( self.layoutGrille )
		# On adapte la taille du widget
		self.widgetCentral.adjustSize()
		# On ajoute le widget central a la scroll area
		self.scrollArea.setWidget( self.widgetCentral )
		# On met en place le layout principal qui contient la scroll area dans le dialog
		self.dialogPreferences.setLayout( self.layoutPrincipal )		

	## Methode pour envoyer les nouvelles valeurs des options du plugin a API
	def sauvegarderPreferences( self ):
		# Pour chaque widget
		for( typeWidget, widget ) in self.listeWidget:
			# On recupere le nom de la preference
			nomPreference = qstringToString( widget.objectName() )

			# On recupere l'information qui nous interesse dans le widget et on la retourne
			if( typeWidget == self.OPTION_TEXTE ):
				valeurWidget = qstringToString( widget.text() )
			elif( typeWidget == self.OPTION_CHECKBOX ):
				valeurWidget = ( widget.checkState() == QtCore.Qt.Checked )
			elif( typeWidget == self.OPTION_LISTE ):
				liste = []
				for i in range( widget.count() ): # Pour chaque ligne
					if( widget.item( i ).checkState() == QtCore.Qt.Checked ): # Si elle est selectionnee
						liste.append( qstringToString( widget.item( i ).text() ) )
				valeurWidget = liste
			elif( typeWidget == self.OPTION_COMBOBOX ):
				valeurWidget = qstringToString( widget.currentText() )
			else:
				logger.warn( "type d'option inconnu" )
				continue

			# On envoit la nouvelle valeur
			self.api.setPluginOption( self.nomPluginCourant, nomPreference, valeurWidget )
		
		# On ferme la fenetre
		self.dialogPreferences.hide()
	
	###############################################
	# Fonctions pour creer les elements du dialog #
	###############################################

	## Methode pour ajouter une zone de texte
	# A ne pas appeler implicitement
	# @param nom             Nom unique de la preference
	# @param texteDescriptif Texte qui presente la preference
	# @param texteParDefaut  Valeur par defaut du texte
	def ajoutTexte( self, nom, texteDescriptif, texteParDefaut ):
		# On cree le widget
		widget = QtGui.QLineEdit( self.dialogPreferences )
		# On met en place son nom
		widget.setObjectName( stringToQstring( nom ) )
		# On met en place son texte par defaut
		widget.setText( stringToQstring( texteParDefaut ) )
		# On l'ajoute a la liste des widgets du dialog
		self.listeWidget.append( [ self.OPTION_TEXTE, widget ] )	
		# On cree le label qui le decrit
		label = QtGui.QLabel( stringToQstring( texteDescriptif ), self.dialogPreferences )
		# On ajoute le texte et le widget au layout
		numeroLigne = self.layoutGrille.rowCount()
		self.layoutGrille.addWidget( label, numeroLigne, 0, 1, 1 )
		self.layoutGrille.addWidget( widget, numeroLigne, 1, 1, 1 )

	## Methode pour ajouter une case a cocher
	# A ne pas appeler implicitement
	# @param nom             Nom unique de la preference
	# @param texteDescriptif Texte qui presente la preference
	# @param valeurParDefaut Valeur par defaut (True ou False)
	def ajoutCheckBox( self, nom, texteDescriptif, valeurParDefaut ):	
		# On cree le widget
		widget = QtGui.QCheckBox( self.dialogPreferences )
		#~ widget = QtGui.QCheckBox( u"Activer ?", self.dialogPreferences )
		# On met en place son nom
		widget.setObjectName( stringToQstring( nom ) )
		# On met en place sa valeur par defaut (cochee ou non)
		if( valeurParDefaut ):
			widget.setCheckState( QtCore.Qt.Checked )
		else:
			widget.setCheckState( QtCore.Qt.Unchecked )
		# On l'ajoute a la liste des widgets du dialog
		self.listeWidget.append( [ self.OPTION_CHECKBOX, widget ] )
		# On cree le label qui le decrit
		label = QtGui.QLabel( stringToQstring( texteDescriptif ), self.dialogPreferences )
		# On ajoute le texte et le widget au layout
		numeroLigne = self.layoutGrille.rowCount()
		self.layoutGrille.addWidget( label, numeroLigne, 0, 1, 1 )
		self.layoutGrille.addWidget( widget, numeroLigne, 1, 1, 1 )				

	## Methode pour ajouter une liste
	# A ne pas appeler implicitement
	# @param nom             Nom unique de la preference
	# @param texteDescriptif Texte qui presente la preference
	# @param valeurs         Valeurs par defaut [ [ Element1, Cochee1 ? ], [ ... ] , ... ]
	def ajoutListe( self, nom, texteDescriptif, valeurs ):
		# On cree le widget
		widget = QtGui.QListWidget( self.dialogPreferences )
		# On met en place son nom
		widget.setObjectName( stringToQstring( nom ) )
		# On met en place ses valeurs
		for( nom, cochee ) in valeurs:
			widget.addItem( self.creerItem( nom, cochee ) )
		# On l'ajoute a la liste des widgets du dialog
		self.listeWidget.append( [ self.OPTION_LISTE, widget ] )
		# On cree le label qui le decrit
		label = QtGui.QLabel( stringToQstring( texteDescriptif ), self.dialogPreferences )
		# On ajoute le texte et le widget au layout
		numeroLigne = self.layoutGrille.rowCount()
		self.layoutGrille.addWidget( label,  numeroLigne,     0, 1, 2 )
		self.layoutGrille.addWidget( widget, numeroLigne + 1, 0, 1, 2 )	

	## Methode pour ajouter une liste deroulante
	# A ne pas appeler implicitement
	# @param nom             Nom unique de la preference
	# @param texteDescriptif Texte qui presente la preference
	# @param elements        Element de la liste
	# @param valeurParDefaut Element selectionne dans la liste
	def ajoutComboBox( self, nom, texteDescriptif, elements, valeurParDefaut ):
		# On cree le widget
		widget = QtGui.QComboBox( self.dialogPreferences )
		# On met en place son nom
		widget.setObjectName( stringToQstring( nom ) )
		# On ajoute tous les elements a la combo box
		for elmt in elements:
			widget.addItem( stringToQstring( elmt ) )
		# On met en place la valeur par defaut
		if not( valeurParDefaut in elements ): # Si on a pas deja la valeur par defaut dans la liste
			# On l'ajoute
			widget.addItem( stringToQstring( valeurParDefaut ) )
		# On selectionne la valeur par defaut
		widget.setCurrentIndex( widget.findText( stringToQstring( valeurParDefaut ) ) )
		# On l'ajoute a la liste des widgets du dialog
		self.listeWidget.append( [ self.OPTION_COMBOBOX, widget ] )
		# On cree le label qui le decrit
		label = QtGui.QLabel( stringToQstring( texteDescriptif ), self.dialogPreferences )
		# On ajoute le texte et le widget au layout
		numeroLigne = self.layoutGrille.rowCount()
		self.layoutGrille.addWidget( label, numeroLigne, 0, 1, 1 )
		self.layoutGrille.addWidget( widget, numeroLigne, 1, 1, 1 )	

	####################
	# Autres fonctions #
	####################
	
	## Fonction qui creer un item pour un QListWidget
	# @param texte    Texte de l'element
	# @param checkBox La checkbox doit-elle etre cochee ?
	# @return L'element cree
	def creerItem( self, texte, checkBox ):
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
	
