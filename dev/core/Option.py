#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier LICENSE #
#########################################

#~ Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
#~ Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
#~ Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import os.path
import pickle

import logging
logger = logging.getLogger( "TVDownloader" )

##########
# Classe #
##########

class Option():
	
	def __init__(self, type, nom, description, valeur, choix=None):
		self.type = type
		self.nom= nom
		self.description= description
		self.valeur = valeur
		
		if type == Option.TYPE_CHOIX_MULTIPLE and not isinstance(valeur, list):
			raise Exception("La valeur doit être une liste pour le type spécifié.")
		
		if choix != None:
			if self.type != Option.TYPE_CHOIX_MULTIPLE and self.type != Option.TYPE_CHOIX_UNIQUE:
				raise Exception("Liste des choix inutile pour le type d'option spécifié.")
			elif not isinstance(choix, list):
				raise Exception("La liste des choix doit être une liste.")
			self.choix = choix
		elif self.type == Option.TYPE_CHOIX_MULTIPLE or self.type == Option.TYPE_CHOIX_UNIQUE:
			raise Exception("Liste des choix obligatoire pour le type d'option spécifié.")
	
	
	#/*******************
	# *	CONSTANTES *
	# *******************/
	TYPE_TEXTE = "texte"
	TYPE_BOULEEN = "bouleen"
	TYPE_CHOIX_MULTIPLE = "choixmult"
	TYPE_CHOIX_UNIQUE = "choixuniq"
	
	
	def setValeur(self, valeur):
		if self.type == Option.TYPE_TEXTE and not isinstance(valeur, str):
			raise Exception("La valeur d'une option texte doit être une chaîne.")
		elif self.type == Option.TYPE_BOULEEN and not isinstance(valeur, bool):
			raise Exception("La valeur d'une option bouléen doit être un bouléen.")
		elif self.type == Option.TYPE_CHOIX_MULTIPLE and not isinstance(valeur, list):
			raise Exception("La valeur d'une option choix multiple doit être une liste.")
		elif self.type == Option.TYPE_CHOIX_UNIQUE and not isinstance(valeur, str):
			raise Exception("La valeur d'une option choix unique doit être une liste.")
		self.valeur = valeur
	
	def setChoix(self, choix):
		if self.type == Option.TYPE_TEXTE:
			raise Exception("Pas de choix pour les options de type texte.")
		elif self.type == Option.TYPE_BOULEEN:
			raise Exception("Pas de choix pour les options de type booléen.")
		elif not isinstance(choix, list):
			raise Exception("La liste des choix doit être une liste.")
		self.choix = choix
	
	
	def getType(self):
		return self.type
	
	def getNom(self):
		return self.nom
	
	def getDescription(self):
		return self.description
	
	def getValeur(self):
		return self.valeur
	
	def getChoix(self):
		if self.type == Option.TYPE_TEXTE:
			raise Exception("Pas de choix pour les options de type texte.")
		elif self.type == Option.TYPE_BOULEEN:
			raise Exception("Pas de choix pour les options de type booléen.")
		return self.choix
