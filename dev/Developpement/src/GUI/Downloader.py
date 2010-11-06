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

import os
import re
import shlex
import subprocess
import sys
import time

from fonctions.urlToRtmpdump import urlToRtmpdump

from PyQt4 import QtGui, QtCore

import logging
logger = logging.getLogger( __name__ )

##########
# Classe #
##########

## Classe qui gere le telechargement des fichiers
class Downloader( QtCore.QObject ):
	
	repertoireTelechargement = ""
	
	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( Downloader, self ).__new__( self )
		return self.instance
	
	## Constructeur
	def __init__( self ):
		QtCore.QObject.__init__( self )
		
		self.arreter = True
		self.process = None
	
	## Methode pour telecharger un fichier
	# @param   fichier Fichier a telecharger
	# @return  Booleen qui indique si le telechargement a reussi
	def telecharger( self, fichier ):
		# Chemin complet du fichier de sortie
		fichierSortie = os.path.join( self.repertoireTelechargement, getattr( fichier, nomFichierSortie ) )
		# URL du fichier
		urlFichier = getattr( fichier, lien )
		logger.info( u"téléchargement de %s" %( urlFichier ) )
		
		# On va creer la commande a executer pour telecharger le fichier
		# L'outil va dependre du protocol
		if( urlFichier[ :4 ] == "rtmp" ):
			commande = '%s -o "%s"' %( urlToRtmpdump( urlFichier ), fichierSortie )
		elif( urlFichier[ :4 ] == "http" or urlFichier[ :3 ] == "ftp" or urlFichier[ :3 ] == "mms" ):
			commande = "msdl -c " + urlFichier + ' -o "' + fichierSortie + '"'
		else:
			logger.warn( u"le protocole du fichier %s n'est pas géré" %( urlFichier ) )
			return False
		# Commande mise au bon format pour Popen
		if( not isinstance( commande, str ) ):
			commande = str( commande )
		
		# Arguments a donner a Popen
		arguments = shlex.split( commande )
		# On commence
		self.arreter = False
		# On lance la commande en redirigeant stdout et stderr (stderr va dans stdout)
		self.process = subprocess.Popen( arguments, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True )
		# On recupere le flux stdout
		stdoutF = self.process.stdout
		# Tant que le subprocess n'est pas fini
		while( self.process.poll() == None ):
			# On lit stdout
			ligne = stdoutF.readline()
			# On recupere le pourcentage (s'il est affiche)
			pourcentListe = re.findall( "(\d{1,3}\.{0,1}\d{0,1})%", ligne )
			if( pourcentListe != [] ):
				pourcent = int( float( pourcentListe[ -1 ] ) )
				if( pourcent >= 0 and pourcent <= 100 ):
					# On envoit le pourcentage d'avancement a l'interface
					self.emit( QtCore.SIGNAL( "pourcentageFichier(int)" ), pourcent )

					# On attent avant de recommencer a lire
					time.sleep( 1 )		

		# On a fini
		self.arreter = True
		self.process = None
		
		# Le telechargement s'est bien passe
		return True

	## Methode pour stopper le telechargement d'un fichier
	def stopperTelechargement( self ):
		if not self.arreter:
			self.arreter = True
			# On stop le process s'il est lance
			if( self.process != None and self.process.poll() == None ):
				self.process.terminate() 
				#~ self.process.kill()
