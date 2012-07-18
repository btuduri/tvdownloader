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

from PyQt4 import QtCore

import re
import unicodedata

#############
# Fonctions #
#############

## Fonction qui transforme un string Python en QString
# @param texte Le string a transformer
# @return Le string transforme en QString
def stringToQstring( texte ):
	if( isinstance( texte, str ) ):
		return QtCore.QString( unicode( texte, "utf-8", "replace" ) )
	else:
		return QtCore.QString( texte )

## Fonction qui transforme un QString en string Python
# @param texte Le QString a transformer
# @return Le QString tranforme en string	
def qstringToString( texte ):
	try:
		return str( texte.toUtf8() )
	except UnicodeDecodeError:
		return unicode( texte.toUtf8(), "utf-8" )
