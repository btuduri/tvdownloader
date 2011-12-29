#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import unittest
import sys
if not( "../" in sys.path ):
	sys.path.insert( 0, "../" )

from Historique import Historique
from Fichier import Fichier

##########
# Classe #
##########

## Classe qui gere les tests de la classe Historique
class HistoriqueTests( unittest.TestCase ):
	
	## Initialisation
	def setUp( self ):
		self.historique = Historique()
		
	## Fin
	def tearDown( self ):
		pass
	
	def testSingleton( self ):
		"""Test si le pattern singleton est bien en place"""
		self.assertEqual( id( self.historique ), id( Historique() ) )
	
	def testMauvaisType( self ):
		"""Test si l'historique renvoit bien faux si on lui demande s'il contient une variable qui n'est pas un fichier"""
		variable = "jeSuisUnString"
		self.assertEqual( self.historique.comparerHistorique( variable ), False )
	
	def testPresenceElement( self ):
		"""Test si l'historique est capable de retrouver un element"""
		element = Fichier( "Napoleon", "1804", "Notre Dame", "Sacre Napoleon" )
		# On ajoute l'element a l'historique
		self.historique.ajouterHistorique( element )
		# On verifie si l'element y est present
		self.assertEqual( self.historique.comparerHistorique( element ), True )

if __name__ == "__main__" :
	unittest.main()