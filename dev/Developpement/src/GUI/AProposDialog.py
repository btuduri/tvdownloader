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

from PyQt4 import QtGui, QtCore

from GUI.ConvertQString import *

#########
# Texte #
#########

texteCredits = \
u"""Développeurs :
- chaoswizard
- ggauthier.ggl

Développeur CLI :
tvelter

Plugins :
BmD_Online : Arte

Remerciements :
- wido (packager Archlinux)
- devil505 (packager Frugalware)
- paulk (packager Fedora)
"""

##########
# Classe #
##########

## Dialog A propos du programme
class AProposDialog( QtGui.QDialog ):
	
	## Constructeur
	def __init__( self ):
		# Appel au constructeur de la classe mere
		QtGui.QDialog.__init__( self )
		
		###########
		# Fenetre #
		###########
		
		###
		# Reglages de la fenetre principale
		###
		
		# Nom de la fenetre
		self.setWindowTitle( "A propos de TVDownloader" )
		# Dimensions la fenetre
		self.resize( 430, 360 )
		# Mise en place de son icone
		self.setWindowIcon( QtGui.QIcon( "ico/gtk-about.svg" ) )
		
		###
		# Mise en place des widgets dans la fenetre
		###
		
		# Layout de grille principal
		self.gridLayout = QtGui.QGridLayout( self )
		
		# Banniere
		self.labelBanniere = QtGui.QLabel()
		self.labelBanniere.setPixmap( QtGui.QPixmap( "img/banniere.png" ) )
		
		# Onglets
		self.tabWidget = QtGui.QTabWidget( self )
		
		# Onglet Infos
		#~ self.tabInfos = QtGui.QWidget()
		#~ self.tabWidget.addTab( self.tabInfos, "Infos" )
		
		#
		# Onglet Crédits
		#
		self.tabCredits = QtGui.QWidget()
		
		# On ajoute une zone de texte dans laquelle on ajoute les credits
		self.gridLayoutCredits = QtGui.QGridLayout( self.tabCredits )
		self.plainTextEditCredits = QtGui.QPlainTextEdit( self.tabCredits )
		self.plainTextEditCredits.appendPlainText( texteCredits )
		self.gridLayoutCredits.addWidget( self.plainTextEditCredits, 0, 0, 1, 1 )
		self.tabWidget.addTab( self.tabCredits, u"Crédits" )
		
		#
		# Onglet Licence
		#
		self.tabLicence = QtGui.QWidget()
		
		# On ajoute une zone de texte dans laquelle on ajoute la licence
		self.gridLayoutLicence = QtGui.QGridLayout( self.tabLicence )
		self.plainTextEditLicence = QtGui.QPlainTextEdit( self.tabLicence )
		fichier = open( "COPYING", "rt" )
		self.plainTextEditLicence.appendPlainText( fichier.read() )
		fichier.close()
		self.gridLayoutLicence.addWidget( self.plainTextEditLicence, 0, 0, 1, 1 )
		self.tabWidget.addTab( self.tabLicence, "Licence" )
		
		# Bouton pour fermer la fenetre
		self.buttonBox = QtGui.QDialogButtonBox( self )
		self.buttonBox.addButton( "Fermer", QtGui.QDialogButtonBox.AcceptRole )
		
		# On ajoute le tout au layout
		self.gridLayout.addWidget( self.labelBanniere, 0, 0, 1, 1 )
		self.gridLayout.addWidget( self.tabWidget    , 1, 0, 1, 1 )
		self.gridLayout.addWidget( self.buttonBox    , 2, 0, 1, 1 )
		
		###
		# Signaux provenants de l'interface
		###
		
		QtCore.QObject.connect( self.buttonBox, QtCore.SIGNAL( "accepted()" ), self.accept )
		
		# On selectionne le premier onglet
		self.tabWidget.setCurrentIndex( 0 )
		
