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

## Classe qui envoie differents signaux
class Signaux( QtCore.QObject ):

	## Constructeur
	def __init__( self ):
		QtCore.QObject.__init__( self )
		# Liste des signaux
		self.listeSignaux = {
							"actualiserListesDeroulantes" : QtCore.SIGNAL( "actualiserListesDeroulantes()" ),
							"debutActualisation"          : QtCore.SIGNAL( "debutActualisation(PyQt_PyObject)" ),
							"finActualisation"            : QtCore.SIGNAL( "finActualisation()" ),
							"listeChaines"                : QtCore.SIGNAL( "listeChaines(PyQt_PyObject)" ),
							"listeEmissions"              : QtCore.SIGNAL( "listeEmissions(PyQt_PyObject)" ),
							"listeFichiers"               : QtCore.SIGNAL( "listeFichiers(PyQt_PyObject)" ),
							"debutTelechargement"         : QtCore.SIGNAL( "debutTelechargement(int)" ),
							"pourcentageFichier"          : QtCore.SIGNAL( "pourcentageFichier(int)" ),
							"finTelechargement"           : QtCore.SIGNAL( "finTelechargement(int)" ),
							"finDesTelechargements"       : QtCore.SIGNAL( "finDesTelechargements()" ),
							}
	
	## Methode qui envoie le signal
	# @param nomSignal  Le nom du signal a envoyer
	# @param parametres Les parametres du signal	
	def signal( self, nomSignal, *parametres ):	
		if( self.listeSignaux.has_key( nomSignal ) ):
			self.emit( self.listeSignaux[ nomSignal ], *parametres )
		else:
			print "Signaux.signal() : le signal %s n'existe pas" %( nomSignal )
	
