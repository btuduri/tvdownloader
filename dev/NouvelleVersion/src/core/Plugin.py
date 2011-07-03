#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########



##########
# Classe #
##########

class Plugin :
	def __init__( self, nom, nomComplet ) :
		self.nom        = nom        # Nom du plugin (sans accents, espaces, caracteres speciaux, ...)
		self.nomComplet = nomComplet # Nom complet du plugin

