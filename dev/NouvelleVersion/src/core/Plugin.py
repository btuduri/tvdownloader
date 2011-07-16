#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

from PluginCache import PluginCache

##########
# Classe #
##########

class Plugin :
	
	def __init__( self, nom, nomComplet, nomImage ) :
		self.nom        = nom                      # Nom du plugin (sans accents, espaces, caracteres speciaux, ...)
		self.nomComplet = nomComplet               # Nom complet du plugin
		self.image      = chargerImage( nomImage ) # Image representant le plugin
		
		# Cache
		self.cache      = PluginCache()
		# S'ajoute soit meme au cache
		self.cache.ajouterPlugin( self.nom )
	
	## Methode qui charge l'image du plugin
	# @param nomImage Nom de l'image a charger
	# @return         Image
	def chargerImage( self, nomImage ):
		pass
