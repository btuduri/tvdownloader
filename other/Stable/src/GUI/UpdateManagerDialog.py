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

from PyQt4 import QtGui, QtCore
from GUI.Qt.MyQTableWidget import MyQTableWidget
from GUI.Qt.MyQPushButton import MyQPushButton

from UpdateManager import UpdateManager

from GUI.ConvertQString import *

##########
# Classe #
##########

## Classe qui gere le dialog du gestionnaire de mise a jour
class UpdateManagerDialog( QtGui.QDialog ):
	
	## Constructeur
	def __init__( self, parent ):
		
		# Appel au constructeur de la classe mere
		QtGui.QDialog.__init__( self, parent )
		
		self.updateManager = UpdateManager()
		
		###########
		# Fenetre #
		###########
		
		###
		# Reglages de la fenetre principale
		###
		
		# Nom de la fenetre
		self.setWindowTitle( u"Mise à jour des plugins" )
		# Dimensions la fenetre
		self.resize( 1, 190 )
		# Mise en place de son icone
		self.setWindowIcon( QtGui.QIcon( "ico/gtk-refresh.svg" ) )
		
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
		# Choix du miroir pour la mise a jour
		#
		
		# Label
		self.labelMiroir = QtGui.QLabel( self )
		self.labelMiroir.setFont( fontTitres )
		self.labelMiroir.setText( u"Miroir :" )
		
		# Choix du miroir
		self.comboBoxMiroir = QtGui.QComboBox( self )
		self.comboBoxMiroir.setEditable( True )
		for miroir in UpdateManager.listeSites:
			self.comboBoxMiroir.addItem( stringToQstring( miroir ) )
		
		# Bouton pour lancer la recherche
		self.pushButtonRecherche = QtGui.QPushButton( self )
		self.pushButtonRecherche.setIcon( QtGui.QIcon( "ico/gtk-refresh.svg" ) )
		self.pushButtonRecherche.setToolTip( u"Rechercher les mises à jour des plugins" )
		
		# Label info
		self.labelInfo = QtGui.QLabel( self )
		self.labelInfo.setText( u"(il faut redémarer le logiciel pour que les mises à jour soient prises en compte)" )
		
		#
		# Affichage des plugins a mettre a jour
		#
		
		# Table widget qui contient la liste des plugins a mettre a jour
		self.tableWidgetPlugins = MyQTableWidget( self )
		# Il a 2 colonnes et 0 ligne (pour l'instant)
		self.tableWidgetPlugins.setColumnCount( 2 )
		self.tableWidgetPlugins.setRowCount( 0 )
		# On ajoute les titres
		self.tableWidgetPlugins.setHorizontalHeaderItem( 0,
														 self.tableWidgetPlugins.creerItem( "" ) )
		self.tableWidgetPlugins.setHorizontalHeaderItem( 1,
														 self.tableWidgetPlugins.creerItem( "Nom du plugin" ) )
														 
		# Icones du tableWidget
		self.iconeMAJ         = QtGui.QIcon( "ico/gtk-add.svg" )
		self.iconeMAJReussie  = QtGui.QIcon( "ico/gtk-apply.svg" )
		self.iconeMAJEchouee  = QtGui.QIcon( "ico/gtk-cancel.svg" )
		
		# Bouton pour lancer l'installation des plugins a mettre a jour
		self.pushButtonLancerInstallation = MyQPushButton( self )
		self.pushButtonLancerInstallation.setIcon( QtGui.QIcon( "ico/gtk-media-play-ltr.svg" ) )
		self.pushButtonLancerInstallation.setToolTip( u"Installer les mises à jour des plugins" )
		
		
		# Bouton pour redemarrer/fermer la fenetre
		self.buttonBox = QtGui.QDialogButtonBox( self )
		#~ self.buttonBox.addButton( "Redemmarer programme", QtGui.QDialogButtonBox.AcceptRole )
		self.buttonBox.addButton( "Fermer", QtGui.QDialogButtonBox.RejectRole )
		
		
		# On ajoute le tout au layout
		self.gridLayout.addWidget( self.labelMiroir, 0, 0, 1, 1 )
		self.gridLayout.addWidget( self.comboBoxMiroir, 0, 1, 1, 1 )
		self.gridLayout.addWidget( self.pushButtonRecherche, 0, 2, 1, 1 )
		self.gridLayout.addWidget( self.labelInfo, 1, 0, 1, 3 )
		self.gridLayout.addWidget( self.tableWidgetPlugins, 2, 0, 1, 2 )
		self.gridLayout.addWidget( self.pushButtonLancerInstallation, 2, 2, 1, 1 )
		self.gridLayout.addWidget( self.buttonBox, 3, 0, 1, 3 )
		
		###
		# Signaux
		###
		
		QtCore.QObject.connect( self.pushButtonRecherche, QtCore.SIGNAL( "clicked()" ), self.rechercheMiseAJour )
		QtCore.QObject.connect( self.pushButtonLancerInstallation, QtCore.SIGNAL( "clicked()" ), self.mettreAJourPlugins )
		
		#~ QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL( "accepted()" ), self.??? )
		QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL( "rejected()" ), self.reject )
		
		QtCore.QObject.connect( self, QtCore.SIGNAL( "finRechercheMAJ(PyQt_PyObject)" ), self.afficherMiseAJour )
		
		self.listePluginAMettreAJour = []
	
	## Methode pour afficher la fenetre des preferences
	def afficher( self ):
		# On n'active pas le bouton d'installation
		self.pushButtonLancerInstallation.setEnabled( False )
		# On affiche la fenetre
		self.exec_()
	
	## Methode qui va lancer la recherche de mise a jour sur le site actuellement selectionne
	def rechercheMiseAJour( self ):
		def threadRechercheMiseAJour( self, site ):
			listePluginAMettreAJour = self.updateManager.verifierMiseAjour( site )
			self.emit( QtCore.SIGNAL( "finRechercheMAJ(PyQt_PyObject)" ), listePluginAMettreAJour )
			
		site = qstringToString( self.comboBoxMiroir.currentText() )
		threading.Thread( target = threadRechercheMiseAJour, args = ( self, site ) ).start()
	
	## Methode qui affiche les mise a jour
	# @param listePluginAMettreAJour Liste des plugins a mettre a jour [ Nom du plugin, URL ou charger le plugin, SHA1 du plugin ]
	def afficherMiseAJour( self, listePluginAMettreAJour ):
		self.listePluginAMettreAJour = listePluginAMettreAJour
		self.tableWidgetPlugins.toutSupprimer()
		# Si on n'a rien recuperer
		if( len( listePluginAMettreAJour ) == 0 ):
			QtGui.QMessageBox.information( self,
										   u"Mise à jour des plugins",
										   u"Aucune mise à jour disponible."
										 )
			# On n'active pas le bouton d'installation
			self.pushButtonLancerInstallation.setEnabled( False )
		else:
			ligneCourante = 0
			for( nom, url, sha1 ) in self.listePluginAMettreAJour:
				# On ajoute une ligne
				self.tableWidgetPlugins.insertRow( ligneCourante )
				self.tableWidgetPlugins.setLigne( ligneCourante, [ self.tableWidgetPlugins.creerItem( "" ),
																   self.tableWidgetPlugins.creerItem( stringToQstring( nom ) )
																 ] 
												)
				self.tableWidgetPlugins.item( ligneCourante, 0 ).setIcon( self.iconeMAJ )
				ligneCourante += 1
			# On active le bouton d'installation
			self.pushButtonLancerInstallation.setEnabled( True )
	
	## Methode qui met a jour tous les plugins
	def mettreAJourPlugins( self ):
		def threadMettreAJour( self ):
			ligne = 0
			for( nom, url, sha1 ) in self.listePluginAMettreAJour:
				retour = self.updateManager.mettreAJourPlugin( nom, url, sha1 )
				if( retour ):
					self.tableWidgetPlugins.item( ligne, 0 ).setIcon( self.iconeMAJReussie )
				else:
					self.tableWidgetPlugins.item( ligne, 0 ).setIcon( self.iconeMAJEchouee )
				ligne += 1
			# On n'active pas le bouton d'installation
			self.pushButtonLancerInstallation.setEnabled( False )
				
		threading.Thread( target = threadMettreAJour, args = ( self, ) ).start()
	