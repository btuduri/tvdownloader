#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import os
import unicodedata 

import logging
logger = logging.getLogger( __name__ )

#############
# Fonctions #
#############

## Cree un repertoire s'il n'existe pas
# @param chemin Chemin du repertoire a creer
def verifieRepertoire( chemin ):
	if( not os.path.exists( chemin ) ):
		logger.info( "verifieRepertoire : le repertoire %s n'existe pas ; creation" %( chemin ) )
		try :
			os.makedirs( chemin )
		except Exception, e :
			logger.error( "verifieRepertoire : impossible de creer le dossier %s" %( chemin ) )
			logger.error( e )

## Transforme une chaine de caracteres en chemin de fichier
# @param chaine Chaine de caracteres a traiter
# @return       Chaine de caracteres utilisable comme nom de fichier
def chaineToNomFichier( self, chaine ):
	if( isinstance( chaine, str ) ):
		chaine = unicode( chaine, "utf8" )
	# Supprime les accents
	chaineNettoyee = unicodedata.normalize( 'NFKD', chaine ).encode( 'ASCII', 'ignore' )
	# Supprimes les espaces
	chaineSansEspaces = chaineNettoyee.replace( " ", "_" )
	# Supprime les caracteres speciaux
	return "".join( [ x for x in chaineSansEspaces if x.isalpha() or x.isdigit() or x == "." ] )
