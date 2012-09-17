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
import os.path
import threading
import subprocess
import shlex
import re
import fcntl
import select
import time
import sys
import unicodedata
import logging
logger = logging.getLogger( __name__ )

from Preferences import Preferences
from fonctions.urlToRtmpdump import urlToRtmpdump

##########
# Classe #
##########

## Classe qui gere le telechargement des fichiers
class Downloader( object ):
	
	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( Downloader, self ).__new__( self )
		return self.instance
	
	## Constructeur
	# @param signaux Lanceur de signaux. Si on le precise pas, aucun signal n'est lance (mode CLI).
	def __init__( self, signaux = None ):
		self.preferences = Preferences()
		self.signaux = signaux
		
		self.arreter = True
		self.process = None

	## Methode pour afficher un pourcentage à l'ecran
	# @param pourcentage Pourcentage actuel a afficher
	def afficherPourcentage( self, pourcentage ):
		
		# On s'assure que le pourcentage soit bien entre 0 et 100
		if( pourcentage < 0 ):
			pourcentage = 0
		elif( pourcentage > 100 ):
			pourcentage = 100
		
		message = str( pourcentage ) + " %"
		
		print '\r', # Permet d'écrire au même endroit
		sys.stdout.write( message )
		sys.stdout.flush()
		
	## Methode pour lancer le telecharger des fichiers
	# @param listeFichiers Liste des fichiers a telecharger
	def lancerTelechargement( self, listeFichiers ):
		self.arreter = False
		for ( numero, fichier, nomFichierSortie ) in listeFichiers:
			logger.info( "Telechargement de %s" %( fichier ) )
			# Si on demande de s'arreter, on sort
			if self.arreter:
				break
			# Si on a le lanceur de signal
			if self.signaux :
				# On envoie le signal de debut de telechargement d'un fichier
				self.signaux.signal( "debutTelechargement", numero )
			else:
				print "Debut telechargement", nomFichierSortie
			# On ajoute le repertoire de destination au nom du fichier
			fichierSortie = self.preferences.getPreference( "repertoireTelechargement" ) + "/" + nomFichierSortie
			# On telecharge de differentes manieres selon le protocole
			if( fichier[ :4 ] == "rtmp" ):
				if( fichier.find( "swfVfy" ) == -1 ):
					commande = urlToRtmpdump( fichier )
				else:
					commande = "rtmpdump -r " + fichier
				self.telecharger( commande + " -o \"" + fichierSortie + "\"" )
			elif( fichier[ :4 ] == "http" or fichier[ :3 ] == "ftp" or fichier[ :3 ] == "mms" ):
				self.telecharger( "msdl -c " + fichier + " -o \"" + fichierSortie + "\"" )
			else:
				logger.warn( "le protocole du fichier %s n'est pas gere" %( fichier ) )	
			# Si on a le lanceur de signal
			if self.signaux :
				# On envoie le signal de fin de telechargement d'un fichier
				self.signaux.signal( "finTelechargement", numero )
			else:
				print "\n\tFin telechargement"
		# Si on a le lanceur de signal
		if self.signaux :
			# On envoie le signal de fin de telechargement des fichiers
			self.signaux.signal( "finDesTelechargements" )
		
	## Methode qui telecharge un fichier
	# @param commande Commande a lancer pour telecharger le fichier
	def telecharger( self, commande ):
		# Commande mise au bon format pour Popen
		if( not isinstance( commande, str ) ):
			commande = str( commande )
		arguments = shlex.split( commande )

		# On lance la commande en redirigeant stdout et stderr (stderr va dans stdout)
		self.process = subprocess.Popen( arguments, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
		# On recupere le flux stdout
		stdoutF = self.process.stdout
		# On recupere le descripteur de fichier de stdout
		stdoutFD = stdoutF.fileno()
		# On recupere les flags existants
		stdoutFlags = fcntl.fcntl( stdoutFD, fcntl.F_GETFL )
		# On modifie les flags existants en ajoutant le flag NoDelay
		fcntl.fcntl( stdoutFD, fcntl.F_SETFL, stdoutFlags | os.O_NDELAY )

		# Tant que le subprocess n'est pas fini
		while( self.process.poll() == None ):
			# On attent que stdout soit lisible
			if( stdoutFD in select.select( [ stdoutFD ],[],[] )[ 0 ] ):
				# On lit stdout
				ligne = stdoutF.read()
				# On affiche que les textes non vides
				if ligne:
					pourcentListe = re.findall( "(\d{1,3}\.{0,1}\d{0,1})%", ligne )
					if( pourcentListe != [] ):
						pourcent = int( float( pourcentListe[ -1 ] ) )
						if( pourcent >= 0 and pourcent <= 100 ):
							# Si on a le lanceur de signal
							if not self.signaux :
								self.afficherPourcentage( pourcent )
							elif self.signaux :
								# On envoit le pourcentage d'avancement a l'interface
								self.signaux.signal( "pourcentageFichier", pourcent )

			# On attent avant de recommencer a lire
			time.sleep( 3 )		
		   	
	## Methode pour stopper le telechargement des fichiers
	def stopperTelechargement( self ):
		if not self.arreter:
			# On sort de la boucle principale
			self.arreter = True
			# On stop le process s'il est lance
			if( self.process.poll() == None ):
				self.process.terminate() 
				#~ self.process.kill()
