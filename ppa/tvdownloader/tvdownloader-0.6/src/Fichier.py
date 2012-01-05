#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier COPYING #
#########################################

# Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
# Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
# Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import datetime
import os.path
import unicodedata 

import logging
logger = logging.getLogger( __name__ )

##########
# Classe #
##########

## Classe qui contient les informations d'un fichier
class Fichier:
	## @var nom
	# Nom du fichier (tel qu'affiché à l'utilisateur)
	
	## @var date
	# Date du fichier sous forme d'une chaîne
	
	## @var lien
	# Url où se trouve le fichier
	
	## @var nomFichierSortie
	# Nom du fichier en sortie
	
	## @var urlImage
	# URL de l'image a afficher avec le Fichier
	
	## @var descriptif
	# Texte descriptif du fichier
	
	## Contructeur.
	# @param self             L'objet courant
	# @param nom              Le nom du fichier (tel qu'affiché à l'utilisateur)
	# @param date             La date du fichier sous forme d'une chaîne
	# @param lien             L'url où se trouve le fichier
	# @param nomFichierSortie Nom du fichier de sortie
	# @param urlImage         URL de l'image a afficher
	# @param descriptif       Texte descriptif a afficher
	def __init__( self, nom = "", date = "", lien = "", nomFichierSortie = "", urlImage = "", descriptif = "" ):
		self.nom              = nom
		self.lien             = lien
		self.urlImage         = urlImage
		self.descriptif       = self.supprimeBaliseHTML( descriptif )
		
		if( nomFichierSortie == "" ):
			self.nomFichierSortie = self.stringToFileName( os.path.basename( self.lien ) )
		else:
			self.nomFichierSortie = self.stringToFileName( nomFichierSortie )
		
		if( isinstance( date, datetime.date ) ):
			self.date = date.isoformat()
		else:
			self.date = date
	
	## Surcharge de la methode ==
	# @param other L'autre Fichier a comparer
	# @return      Si les 2 Fichiers sont egaux	
	def __eq__( self, other ):
		if not isinstance( other, Fichier ):
			return False
		else:
			return ( self.nom  == getattr( other, "nom" ) and \
					 self.date == getattr( other, "date" ) and \
					 self.lien == getattr( other, "lien" ) )
	
	## Surcharge de la methode !=
	# @param other L'autre Fichier a comparer
	# @return      Si les 2 Fichiers sont differents
	def __ne__( self, other ):
		return not self.__eq__( other )
	
	## Methode qui transforme une chaine de caracteres en chaine de caracteres utilisable comme nom de fichiers
	# @param chaine Chaine de caracteres a transformer
	# @return Chaine de caracteres utilisable en nom de fichiers
	def stringToFileName( self, chaine ):
		if( isinstance( chaine, str ) ):
			chaine = unicode( chaine, "utf8" )
		# On supprime les accents
		chaineNettoyee = unicodedata.normalize( 'NFKD', chaine ).encode( 'ASCII', 'ignore' )
		# On supprimes les espaces
		chaineSansEspaces = chaineNettoyee.replace( " ", "_" )
		# On supprime les caracteres speciaux
		return "".join( [ x for x in chaineSansEspaces if x.isalpha() or x.isdigit() or x == "." ] )
		
	## Methode qui supprime les balises HTML courantes d'une chaine de caractere
	# @param chaine Chaine de caracteres a transformer
	# @return Chaine de caracteres utilisable en nom de fichiers	
	def supprimeBaliseHTML( self, chaine ):
		elmts = [ "<b>", "</b>", "<i>", "</i>" ]
		for elmt in elmts:
			chaine = chaine.replace( elmt, "" )
		return chaine
