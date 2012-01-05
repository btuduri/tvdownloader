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

##########
# Classe #
##########

## Classe heritant de QPushButton
class MyQPushButton( QtGui.QPushButton ):
	
	## Constructeur
	# @param parent Parent (le plus souvent, c'est une fenetre ou un layout)
	def __init__( self, *args ):
		# Appel au constructeur de la classe mere
		nb = len( args )
		if( nb == 1 ):
			QtGui.QPushButton.__init__( self, args[ 0 ] )
		elif( nb == 2 ):
			QtGui.QPushButton.__init__( self, args[ 0 ], args[ 1 ] )
		else:
			QtGui.QPushButton.__init__( self, args[ 0 ], args[ 1 ], args[ 2 ] )
		
		# On fait en sorte que la taille du bouton s'adapte toute seule
		sizePolicy = self.sizePolicy()
		sizePolicy.setVerticalPolicy( QtGui.QSizePolicy.Expanding )
		self.setSizePolicy( sizePolicy )
	