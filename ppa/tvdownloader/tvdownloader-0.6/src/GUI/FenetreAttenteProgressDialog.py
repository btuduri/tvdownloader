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

import threading
import time

##########
# Classe #
##########

## Fenetre d'attente du programme
class FenetreAttenteProgressDialog( QtGui.QProgressDialog ):
	
	## Constructeur
	# @param parent Fenetre parent
	def __init__( self, parent ):
		# Appel au constructeur de la classe mere
		QtGui.QProgressDialog.__init__( self,
										"Patientez pendant l'actualisation des informations de                     ",
										"Fermer",
										0,
										0,
										parent )		
		
		# La fenetre est modale
		self.setModal( True )
		# Titre de la fenetre
		self.setWindowTitle( u"Merci de patienter..." )
		# La fenetre ne peut pas changer de taille
		self.setFixedSize( self.size() )
		# On masque le bouton annuler						 										 
		self.setCancelButton( None ) 		
		
		# Signaux
		QtCore.QObject.connect( self, 
								QtCore.SIGNAL( "ouvrirFenetre(PyQt_PyObject)" ),
								self.ouvrirSiNecessaire )	
		
		# Etat dans lequel on veut que soit la fenetre
		# !!! : L'etat dans lequel on veut qu'elle soit n'est pas forcement l'etat dans lequel elle est
		self.etatOuvert = False
		
		# Mutex
		self.lock = threading.Lock()
	
	## Surcharge de la methode appelee lors de la fermeture du dialog
	# Ne doit pas etre appele explicitement
	# @param evenement Evenement qui a provoque la fermeture
	def closeEvent( self, evenement ):
		
		# Si la fenetre est masquee
		if( self.isHidden() ):
			# On accept la fermeture
			evenement.accept()
		else:
			# On refuse la fermeture
			evenement.ignore()
		
	## Methode pour afficher la fenetre d'attente
	# @param nomSite Nom du plugin (site) qui demande la fenetre d'attente	
	def ouvrirFenetreAttente( self, nomSite ):
		self.lock.acquire()
		
		# On veut que la fenetre soit ouverte
		self.etatOuvert = True
		
		self.lock.release()
		
		# On attent un peu puis on ouvre la fenetre si necessaire
		threading.Timer( 0.5, self.emit, ( QtCore.SIGNAL( "ouvrirFenetre(PyQt_PyObject)" ), nomSite ) ).start()

	## Methode lancee par le timer apres X seconde qui ouvre la fenetre d'attente si c'est necessaire
	# @param nomSite Nom du plugin (site) qui demande la fenetre d'attente
	def ouvrirSiNecessaire( self, nomSite ):
		self.lock.acquire()
		
		# Si on veut toujours que la fenetre soit ouverte, on l'ouvre !
		if( self.etatOuvert ):
			self.setLabelText( "Patientez pendant l'actualisation des informations de %s" %( nomSite ) )
			self.show()
		
		self.lock.release()
		
	## Methode pour fermer la fenetre d'attente
	def fermerFenetreAttente( self ):
		self.lock.acquire()
		
		self.etatOuvert = False
		# Si la fenetre est affiche, on la masque apres avoir un peu attendu
		if not ( self.isHidden() ):
			self.hide()

		self.lock.release()
