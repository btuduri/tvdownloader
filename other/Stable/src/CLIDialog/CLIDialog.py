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

import sys
import os.path
import atexit

from lib.dialog import Dialog

from API import API
from Downloader import Downloader
from Historique import Historique
from Preferences import Preferences

##########
# Classe #
##########

## Classe qui gere la version CLI de TVDownloader
class CLIDialog():
	
	## Constructeur
	def __init__( self ):
		
		# On cree l'instance de la classe dialog
		self.dialog = Dialog()
		self.dialog.setBackgroundTitle( "TVDownloader" )
		
		# On recupere l'instance de API
		self.api = API.getInstance()
		# On instancie le gestionnaire de download
		self.downloader = Downloader()
		# On instancie le gestionnaire d'historique
		self.historique = Historique()
		# On instancie le gestionnaire de preferences
		self.preferences = Preferences()

		# Liste des telechargements
		self.listeTelechargements = []

		# Quand le programme se termine, on execute la fonction actionsAvantQuitter
		atexit.register( self.actionsAvantQuitter )

		# On commence
		self.bouclePrincipale()
		
	## Debut
	def bouclePrincipale( self ):
		
		choix = ( 1, "" )
		while( choix != ( 0, "Quitter" ) ):
			# On affiche le menu principal
			choix = self.dialog.menu( text = "Menu Principal" ,
									  choices = [ [ "Commencer", "Afficher la liste des plugins" ],
												  [ "Téléchargements", "Gérer les téléchargements" ],
												  [ "Préférences", "Modifier les préférences" ],
												  [ "Quitter", "Quitter TVDownloader" ],
												]
									)
			# On lance la methode qui va bien
			if( choix == ( 0, "Commencer" ) ):
				self.utilisationPlugins()
			elif( choix == ( 0, "Téléchargements" ) ):
				self.utlisationTelechargements()
			elif( choix == ( 0, "Préférences" ) ):
				pass
			elif( choix == ( 0, "Quitter" ) ):
				# Rien a faire, atexit gere cela
				pass

	## Methode pour selectionner les fichiers a telecharger avec les plugins
	def utilisationPlugins( self ):
		
		# Liste des plugins actifs
		listePlugins = []
		for nomPlugin in self.preferences.getPreference( "pluginsActifs" ):
			listePlugins.append( [ nomPlugin, "" ] )
		
		choixPlugin = ( 0, "" )
		while( choixPlugin[ 0 ] != 1 ):
			# On affiche le menu de selection de plugins
			choixPlugin = self.dialog.menu( text = "De quelle plugin voulez-vous voir les chaines ?",
											choices = listePlugins
										  )			
		
			if( choixPlugin[ 0 ] != 1 ):
				# Liste des chaines du plugin
				listeChaines = []
				for nomChaine in self.api.getPluginListeChaines( choixPlugin[ 1 ] ):
					listeChaines.append( [ nomChaine, "" ] )
				
				choixChaine = ( 0, "" )
				while( choixChaine[ 0 ] != 1 ):
					# On affiche le menu de selection de la chaine
					choixChaine = self.dialog.menu( text = "De quelle chaine voulez-vous voir les emissions ?",
													choices = listeChaines
												  )
					
					if( choixChaine[ 0 ] != 1 ):
						# Liste des emissions de la chaine
						listeEmissions = []
						for nomEmission in self.api.getPluginListeEmissions( choixPlugin[ 1 ], choixChaine[ 1 ] ):
							listeEmissions.append( [ nomEmission, "" ] )
						
						choixEmission = ( 0, "" )
						while( choixEmission[ 0 ] != 1 ):
							# On affiche le menu de selection de l'emission
							choixEmission = self.dialog.menu( text = "De quelle emission voulez-vous voir les fichiers ?",
															  choices = listeEmissions
															)
							
							if( choixEmission[ 0 ] != 1 ):
								listeFichiersAAfficher = []
								listeFichiersCoches = []
								listeFichiersPrecedementCoches = []
								listeFichiersAPI = self.api.getPluginListeFichiers( choixPlugin[ 1 ], choixEmission[ 1 ] )
								i = 0
								for fichier in listeFichiersAPI:
									texteAAfficher = "(%s) %s" %( getattr( fichier, "date" ), getattr( fichier, "nom" ) )
									if( fichier in self.listeTelechargements ):
										listeFichiersPrecedementCoches.append( fichier )
										cochee = 1
									else:
										cochee = 0
									listeFichiersAAfficher.append( [ str( i ), texteAAfficher, cochee ] )
									i+=1
								
								choixFichiers = ( 0, [] )
								while( choixFichiers[ 0 ] != 1 ):
									choixFichiers = self.dialog.checklist( text = "Quels fichiers voulez-vous ajouter à la liste des téléchargements ?",
																		   choices = listeFichiersAAfficher
																		 )
									
									if( choixFichiers[ 0 ] != 1 ):
										for numeroFichier in choixFichiers[ 1 ]:
											fichier = listeFichiersAPI[ int( numeroFichier ) ]
											listeFichiersCoches.append( fichier )
											
										for fichier in listeFichiersCoches:
											if not ( fichier in listeFichiersPrecedementCoches ):
												self.listeTelechargements.append( fichier )
										
										for fichier in listeFichiersPrecedementCoches:
											if not ( fichier in listeFichiersCoches ):
												self.listeTelechargements.remove( fichier )
										
										# On retourne au menu precedent
										choixFichiers = ( 1, "" )

	## Methode qui gere le gestionnaire de telechargement
	def utlisationTelechargements( self ):
		
		choix = ( 0, "" )
		while( choix[ 0 ] != 1 ):
			# On affiche le menu principal
			choix = self.dialog.menu( text = "Gestionnaire de téléchargement" ,
									  choices = [ [ "Consulter", "Consulter la liste" ],
												  [ "Lancer", "Lancer les téléchargements" ]
												]
									)
			
			# On lance la methode qui va bien
			if( choix == ( 0, "Consulter" ) ):

				if( len( self.listeTelechargements ) > 0 ):
					texte = ""
					for fichier in self.listeTelechargements:
						texte += "(%s) %s\n" %( getattr( fichier, "date" ), getattr( fichier, "nom" ) )
				else:
					texte = "La liste des téléchargements est vide"
				
				# On affiche la liste des fichiers a telecharger
				self.dialog.msgbox( text = texte )			
				
			elif( choix == ( 0, "Lancer" ) ):
				
				if( len( self.listeTelechargements ) > 0 ):
					liste = []
					
					for fichier in self.listeTelechargements:
						lien = getattr( fichier , "lien" )
						nomFichierSortie = getattr( fichier , "nomFichierSortie" )
						if( nomFichierSortie == "" ): # Si le nom du fichier de sortie n'existe pas, on l'extrait de l'URL
							nomFichierSortie = os.path.basename( lien )
						
						liste.append( [ 0, lien, nomFichierSortie ] )
					
					# On lance le telechargement
					self.downloader.lancerTelechargement( liste )
					
					self.dialog.msgbox( text = "Fin du téléchargement des fichiers" )
					del self.listeTelechargements[ : ]
				else:
					self.dialog.msgbox( text = "Aucun fichier à télécharger" )

	## Methode qui execute les actions necessaires avant de quitter le programme
	def actionsAvantQuitter( self ):
		print "Fermeture"
		# On sauvegarde les options des plugins
		self.api.fermeture()
		# On sauvegarde l'historique
		self.historique.sauverHistorique()
		# On sauvegarde les options du logiciel
		self.preferences.sauvegarderConfiguration()