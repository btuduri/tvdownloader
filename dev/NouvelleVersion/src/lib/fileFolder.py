#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import os

import logging
logger = logging.getLogger( __name__ )

#############
# Fonctions #
#############

## Creer un repertoire s'il n'existe pas
# @param chemin Chemin du repertoire a creer
def verifieRepertoire( chemin ):
	if( not os.path.exists( chemin ) ):
		logger.info( "verifieRepertoire : le repertoire %s n'existe pas ; creation" %( chemin ) )
		try :
			os.makedirs( chemin )
		except Exception, e :
			logger.error( "verifieRepertoire : impossible de creer le dossier %s" %( chemin ) )
			logger.error( e )
