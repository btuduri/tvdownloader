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
	
	## Contructeur.
	# @param self             L'objet courant
	# @param nom              Le nom du fichier (tel qu'affiché à l'utilisateur)
	# @param date             La date du fichier sous forme d'une chaîne
	# @param lien             L'url où se trouve le fichier
	# @param nomFichierSortie Nom du fichier de sortie
	def __init__( self, nom = "", date = "", lien = "", nomFichierSortie = "" ):
		self.nom              = nom
		self.date             = date
		self.lien             = lien
		self.nomFichierSortie = nomFichierSortie
	
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
