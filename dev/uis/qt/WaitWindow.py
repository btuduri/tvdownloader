#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import threading

from PyQt4 import QtCore
from PyQt4 import QtGui

#
# Classe
#

class WaitWindow( QtGui.QProgressDialog ):
	"""
	Fenetre d'attente
	"""
	
	def __init__( self, parent = None ):
		"""
		Constructeur
		"""
		QtGui.QProgressDialog.__init__( self,
										"Patientez pendant l'actualisation des informations de                             ",
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
		# Masque le bouton annuler						 										 
		self.setCancelButton( None ) 		
		# Signal
		QtCore.QObject.connect( self, 
								QtCore.SIGNAL( "ouvrirFenetre(PyQt_PyObject)" ),
								self.ouvrirSiNecessaire )	
		# Etat dans lequel on veut que soit la fenetre
		# N.B. : L'etat dans lequel on veut qu'elle soit n'est pas forcement l'etat dans lequel elle est
		self.etatOuvert = False
		# Mutex
		self.mutex = threading.Lock()		

	def closeEvent( self, evenement ):
		"""
		La fenetre ne peut etre fermee que si elle est masquee
		"""
		# Si la fenetre est masquee
		if( self.isHidden() ):
			# Accept la fermeture
			evenement.accept()
		else:
			# Refuse la fermeture
			evenement.ignore()

	def ouvrirFenetreAttente( self, nomSite ):
		"""
		Demande d'ouverture de la fenetre
		
		Elle n'est reelement ouverte si necessaire qu'au bout d'un certain temps
		"""
		with self.mutex:
			self.etatOuvert = True
		
		# Attent un peu puis ouvre la fenetre si necessaire
		threading.Timer( 0.5, self.emit, ( QtCore.SIGNAL( "ouvrirFenetre(PyQt_PyObject)" ), nomSite ) ).start()

	def ouvrirSiNecessaire( self, nomSite ):
		"""
		Ouvre la fenetre d'attente (si c'est toujours necessaire
		"""
		with self.mutex:
			if( self.etatOuvert ):
				self.setLabelText( "Patientez pendant l'actualisation des informations de %s" %( nomSite ) )
				self.show()

	def fermerFenetreAttente( self ):
		"""
		Ferme la fenetre d'attente
		"""
		with self.mutex:
			self.etatOuvert = False
			if not ( self.isHidden() ):
				self.hide()

