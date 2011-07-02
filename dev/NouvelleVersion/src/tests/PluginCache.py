#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import unittest

from core import PluginCache

##########
# Classe #
##########

class PluginCacheTest( unittest.TestCase ):
	
	def setUp( self ):
		self.pc = PluginCache()
		self.pc.clear()
		
	def testListesVides( self ):
		"""
		Les methodes de listage doivent retourner des listes vides si la BDD est vide
		"""
		self.assertEqual( self.pc.listerPlugins(), [] )
		self.assertEqual( self.pc.listerChaines( "test" ), [] )
		self.assertEqual( self.pc.listerEmissions( "test", "test" ), [] )
		self.assertEqual( self.pc.listerFichiers( "test", "test", "test" ), [] )
	
	def testListePlugins( self ):
		"""
		La liste des plugins doit etre correcte
		"""
		listePlugins = [ "France Tele", "Arte", "Radio France" ]
		for plugin in listePlugins:
			self.pc.ajouterPlugin( plugin )
		
		self.assertEqual( self.pc.listerPlugins(), listePlugins )
		
	def testListeChaines( self ):
		"""
		La liste des chaines doit etre correcte
		"""
		listePlugins = [ "France Tele", "Arte", "Radio France" ]
		for plugin in listePlugins:
			self.pc.ajouterPlugin( plugin )
		listeChainesFranceTele = [ "France 2", "France 3", "France 5" ]
		for chaine in listeChainesFranceTele:
			self.pc.ajouterChaine( chaine, "France Tele" )
		listeChainesRadioFrance = [ "France Inter", "France Bleu" ]
		for chaine in listeChainesRadioFrance:
			self.pc.ajouterChaine( chaine, "Radio France" )
		
		self.assertEqual( self.pc.listerChaines( "France Tele" ), listeChainesFranceTele )
		self.assertEqual( self.pc.listerChaines( "Arte" ), [] )
		self.assertEqual( self.pc.listerChaines( "Radio France" ), listeChainesRadioFrance )
		
	def testListeEmissions( self ):
		"""
		La liste des emissions doit etre correcte
		"""
		listePlugins = [ "France Tele", "Arte", "Radio France" ]
		for plugin in listePlugins:
			self.pc.ajouterPlugin( plugin )
		listeChainesFranceTele = [ "France 2", "France 3", "France 5" ]
		for chaine in listeChainesFranceTele:
			self.pc.ajouterChaine( chaine, "France Tele" )
		listeChainesRadioFrance = [ "France Inter", "France Bleu" ]
		for chaine in listeChainesRadioFrance:
			self.pc.ajouterChaine( chaine, "Radio France" )
		listeEmissionsFrance2 = [ "Motus", "Pyramide" ]
		for emission in listeEmissionsFrance2:
			self.pc.ajouterEmission( emission, "France 2", "France Tele" )
		listeEmissionsFrance5 = [ "C dans l'air", "Les Maternelles", "Silence ça pousse" ]
		for emission in listeEmissionsFrance5:
			self.pc.ajouterEmission( emission, "France 5", "France Tele" )
		listeEmissionsFranceInter = [ "le 6/7", "Le fou du roi", "Le jeu des mille euros" ]
		for emission in listeEmissionsFranceInter:
			self.pc.ajouterEmission( emission, "France Inter", "Radio France" )
			
		self.assertEqual( self.pc.listerEmissions( "France 2", "France Tele" ), listeEmissionsFrance2 )
		self.assertEqual( self.pc.listerEmissions( "France 3", "France Tele" ), [] )
		self.assertEqual( self.pc.listerEmissions( "France 5", "France Tele" ), listeEmissionsFrance5 )
		self.assertEqual( self.pc.listerEmissions( "France Inter", "Radio France" ), listeEmissionsFranceInter )
		self.assertEqual( self.pc.listerEmissions( "France Bleu", "Radio France" ), [] )
