#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import re

import logging
logger = logging.getLogger( "TVDownloader" )

#############
# Fonctions #
#############

## Supprime les balises HTML d'une chaine de caracteres
# @param chaine Chaine a traiter
# @return Chaine traitee	
def supprimeBalisesHTML( chaine ):
	return re.sub( r'<.*?>', '', chaine )
