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

##########
# Classe #
##########

## Classe heritant de QTableWidget a laquelle on va rajouter des methode specifiques
class MyQTableWidget( QtGui.QTableWidget ):
	
	## Constructeur
	# @param parent Parent (le plus souvent, c'est une fenetre ou un layout)
	def __init__( self, parent = None ):
		# Appel au constructeur de la classe mere
		QtGui.QTableWidget.__init__( self, parent )
		
		# On masque le numero des lignes
		self.verticalHeader().setVisible( False )
		# On masque le quadrillage
		self.setShowGrid( False )
		# Lorsque qu'on clique sur une ligne, on selectionne toute la ligne
		self.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
		# On ne peut selectionner qu'une ligne a la fois
		self.setSelectionMode( QtGui.QAbstractItemView.SingleSelection )
		# La derniere colonne visible prend toute la place restante
		self.horizontalHeader().setStretchLastSection( True )
		# On alterne les couleurs des lignes
		self.setAlternatingRowColors( True )
		
		# On accepte le drag'n drop
		#~ self.setAcceptDrops( True )
		#~ self.setDragDropMode( QtGui.QAbstractItemView.InternalMove )
		#~ self.setDropIndicatorShown( True )
		# Lorsqu'on fait un drag'n drop, on ne supprime rien
		#~ self.setDragDropOverwriteMode( False )
	
	## Methode pour creer un item
	# @param texte      Texte de l'item
	# @param modifiable Indique si le texte peut etre modifiable
	# @param checkBox   Indique si l'item doit comprendre une checkbox
	# @param cochee     Indique si la checkbox doit etre cochee par defaut
	# @return           L'item cree
	def creerItem( self, texte, modifiable = False, checkBox = False, cochee = False ):
		# On cree l'item avec le texte
		item = QtGui.QTableWidgetItem( stringToQstring( texte ) )
		# On centre le texte
		item.setTextAlignment( QtCore.Qt.AlignCenter )
		# L'item peut etre modifiable ?
		if not modifiable:
			item.setFlags( item.flags() & ~QtCore.Qt.ItemIsEditable )
		# L'item doit comprendre une checkbox ?
		if( checkBox ):
			# La checkBox doit etre cochee ?
			if( cochee ):
				item.setCheckState( QtCore.Qt.Checked )
			else:
				item.setCheckState( QtCore.Qt.Unchecked )
		# On renvoie l'item
		return item
	
	## Methode pour renvoyer une ligne (a utiliser avec #setLigne)
	# @param numeroLigne Numero de la ligne a renvoyer
	# @return            La liste des elements de la ligne
	def getLigne( self, numeroLigne ):
		liste = []
		for i in range( self.columnCount() ):
			liste.append( self.takeItem( numeroLigne, i ) )
		return liste

	## Methode pour copier une ligne (a utiliser avec #setLigne)
	# @param numeroLigne Numero de la ligne a copier
	# @return            La liste des elements de la ligne
	def copierLigne( self, numeroLigne ):
		liste = []
		for i in range( self.columnCount() ):
			liste.append( self.item( numeroLigne, i ).clone() )
		return liste		

	## Methode pour mettre en place une ligne (a utiliser avec #getLigne)
	# @param numeroLigne   Numero de la ligne que l'on va mettre en place
	# @param listeElements Liste des elements a mettre en place sur cette ligne
	def setLigne( self, numeroLigne, listeElements ):
		nbColonnes = self.columnCount()
		# Les lignes ont le meme nombre d'elements ?
		if( len( listeElements ) == nbColonnes ):
			for i in range( nbColonnes ):
				self.setItem( numeroLigne, i, listeElements[ i ] )
		else:
			logger.warn( "probleme avec les tailles des colonnes" )
	
	## Methode pour echanger 2 lignes
	# @param numeroLigne1 Numero de la 1ere ligne
	# @param numeroLigne2 Numero de la 2eme ligne
	def echangerLignes( self, numeroLigne1, numeroLigne2 ):
		# On s'assure qu'on essaye pas d'echanger les memes lignes
		if( numeroLigne1 != numeroLigne2 ):
			ligne1 = self.getLigne( numeroLigne1 )
			self.setLigne( numeroLigne1, self.getLigne( numeroLigne2 ) )
			self.setLigne( numeroLigne2, ligne1 )
		else:
			logger.warn( "pourquoi vouloir echanger une ligne avec elle meme ?!" )
	
	## Methode pour supprimer tous les elements
	def toutSupprimer( self ):
		for i in range( self.rowCount() - 1, -1, -1 ): # [ nbLignes - 1, nbLignes - 2, ..., 1, 0 ]
			self.removeRow( i )
		self.adapterColonnes()

	## Methode pour selectionner ou deselectionner toutes les checkbox d'une colonne
	# @param numeroColonne  Numero de la colonne qui contient les checkboxes
	# @param deselectionner Indique s'il faut tout selectionner ou tout deselectionner
	def cocherTout( self, numeroColonne, decocher = False ):
		# On regarde s'il faut tout selectionner ou tout deselectionner
		typeSelection = QtCore.Qt.Checked
		if decocher:
			typeSelection = QtCore.Qt.Unchecked
		# Pour chaque ligne
		for i in range( self.rowCount() ): 
			self.item( i, numeroColonne ).setCheckState( typeSelection )

	## Methode pour deplacer une ligne
	# La ligne est deplacee d'un element ou a une extremite de la liste
	# @param versLeHaut Indique si la ligne doit etre deplacee vers le haut ou vers le bas
	# @param extremite  Indique si la ligne doit etre deplacee a une extremite de la liste
	def deplacerLigne( self, versLeHaut = False, extremite = False ):
		# Si on a au moin un element selectionne
		if( len( self.selectedItems() ) > 0 ):
			numeroLigne = self.currentRow()
			nbLignes = self.rowCount()
			if( versLeHaut ):
				# On test si un deplacement est utile
				if( numeroLigne != 0 or not versLeHaut ):
					if extremite:
						for i in range( numeroLigne, 0, -1 ): # [ numeroLigne - 1, numeroLigne - 2, ..., 1 ]
							self.echangerLignes( i, i - 1 )
						self.selectRow( 0 )						
					else:
						self.echangerLignes( numeroLigne, numeroLigne - 1 )
						self.selectRow( numeroLigne - 1 )
			else:
				# On test si un deplacement est utile
				if( numeroLigne != nbLignes - 1 or versLeHaut ):
					if extremite:
						for i in range( numeroLigne, nbLignes - 1 ):
							self.echangerLignes( i, i + 1 )
						self.selectRow( nbLignes - 1 )						
					else:
						self.echangerLignes( numeroLigne, numeroLigne + 1 )
						self.selectRow( numeroLigne + 1 )
	
	## Methode qui adapte la taille des colonnes
	def adapterColonnes( self ):
		# On adapte la taille des colonnes
		self.resizeColumnsToContents()
		# Si on n'a pas la scroll bar
		if not self.isHorizontalScrollBarVisible():
			# La derniere colonne visible prend toute la place restante
			self.horizontalHeader().setStretchLastSection( True )

	## Methode qui determine si la scroll bar horizontale est visible
	# @return Si la scroll bar horizontale est visible
	def isHorizontalScrollBarVisible( self ):
		isVisible = False
		
		tailleColonnes = 0
		for i in range( self.columnCount() ):
			tailleColonnes += self.columnWidth( i )
			
		tailleWidget = self.width()
		
		if( tailleColonnes > tailleWidget ):
			isVisible = True
			
		return isVisible
			
