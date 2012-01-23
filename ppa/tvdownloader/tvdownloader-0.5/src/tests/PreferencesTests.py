#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import unittest
import sys
sys.path.insert( 0, "../" )

from Preferences import Preferences

##########
# Classe #
##########

## Classe qui gere les tests de la classe Preferences
class PreferencesTest( unittest.TestCase ):
	
	## Initialisation
	def setUp( self ):
		self.preferences = Preferences()
		
	## Fin
	def tearDown( self ):
		pass
	
	def testSingleton( self ):
		"""Test si le pattern singleton est bien en place"""
		self.assertEqual( id( self.preferences ), id( Preferences() ) )
		
	def testSauvegarde( self ):
		"""Test si les preferences sont bien sauvegardees"""
		listePreferences = getattr( self.preferences, "preferences" )
		nomPreference = listePreferences.keys()[ 0 ]		
		nouvelleValeur = "ValeurDeTest"
		
		# On met en place la preference
		self.preferences.setPreference( nomPreference, nouvelleValeur )
		# On verifie qu'elle est bien en place
		self.assertEqual( nouvelleValeur, self.preferences.getPreference( nomPreference ) )

if __name__ == "__main__" :
	unittest.main()