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

import re

########
# Code #
########

# RegEx de decoupage d'un lien RTMP
RTMP_URL_PATTERN = re.compile("(?P<scheme>[^:]*)://(?P<host>[^/^:]*):{0,1}(?P<port>[^/]*)/(?P<app>.*?)/(?P<playpath>\w*?\:.*)", re.DOTALL)

## Fonction qui transforme un lien RTMP en commande rtmpdump
# @param url URL RTMP a transformer
# @return Commande rtmpdump obtenue
def urlToRtmpdump( url ):
	match = re.match( RTMP_URL_PATTERN, url )
	comand = ""
	if match != None:
		comand = "rtmpdump --host %host% --port %port% --protocol %scheme% --app %app% --playpath %playpath%"
		comand = comand.replace( "%scheme%", match.group( "scheme" ) ).replace( "%host%", match.group( "host" ) ).replace( "%app%", match.group( "app" ) ).replace( "%playpath%", match.group( "playpath" ) )
		if( match.group( "port" ) != "" ):
			comand = comand.replace( "%port%", match.group( "port" ) )
		elif( url[ :6 ] == "rtmpte" ):
			comand = comand.replace( "%port%", "80" )
		elif( url[ :5 ] == "rtmpe" ):
			comand = comand.replace( "%port%", "1935" )
		elif( url[ :5 ] == "rtmps" ):
			comand = comand.replace( "%port%", "443" )
		elif( url[ :5 ] == "rtmpt" ):
			comand = comand.replace( "%port%", "80" )
		else:
			comand = comand.replace( "%port%", "1935" )
	else:
		comand = "rtmpdump -r " + url
	print comand
	return comand
