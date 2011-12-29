#/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time

from CLI.Option import dl,prefs,quitter,wait,info
from CLI.Screen import header,footer,plugin,chaine,program,fichier

from getch import getch
from API import API
from APIPrive import APIPrive
from PluginManager import PluginManager
from Preferences import Preferences
from Downloader import Downloader

class show:
	def __init__(self,selectedPlugin,selectedChaine,selectedProgram,temp):
		#affichage de la barre du programme en haut de l'ecran
		header(selectedPlugin,selectedChaine,selectedProgram)
		#selon l'avancement dans la navigation on affichage les plugins, chaines, programmes ou fichiers
		if len(selectedPlugin)==0:
			plugin(plugins,temp)
		elif len(selectedChaine)==0:
			chaine(chaines,temp)
		elif len(selectedProgram)==0:
			program(programs,temp)
		elif len(selectedPlugin)!=0 and len(selectedChaine)!=0 and len(selectedProgram)!=0:
			fichier(fichiers,temp)
		footer()


class cli:
	def __init__(self):
		#declaration des variables
		global choice, temp, plugins, chaines, programs, fichiers, DLlist
		chaines=''
		programs=''
		fichiers=''
		temp = 0
		choice = ""
		selectedPlugin =''
		selectedChaine =''
		selectedProgram = ''
		DLlist=[]

		################################################
		# Instanciations + initialisation de variables #
		################################################

		# On instancie le plugin manager
		self.pluginManager = PluginManager()
		# On instancie le gestionnaire de preferences
		self.preferences = Preferences()
		# On instancie le gestionnaire de download
		self.downloader = Downloader()  
		# On recupere l'instance de API
		self.api = API.getInstance()
#		# On instancie le gestionnaire d'historique
#		self.historique = Historique()

		# Si aucun plugin n'est active, on ouvre la fenetre des preferences
		if( len( self.preferences.getPreference( "pluginsActifs" ) ) == 0 ):
			choice = 'p'
			self.api.pluginRafraichirAuto()
    

		# On met en place la liste des plugins dans API
		plugins = self.preferences.getPreference( "pluginsActifs" )
		plugins.sort()

		# On actualise tous les plugins
		self.api.pluginRafraichirAuto()
		

		#boucle qui raffraichit l'affichage apres chaque interaction utilisateur
		while choice != 'exit':
			#ouverture du menu de preferences
			if choice == 'p' or choice == 'P':
				prefs()
				# On met en place la liste des plugins dans API
				plugins = self.preferences.getPreference( "pluginsActifs" )
				plugins.sort()
				# On actualise tous les plugins
				self.api.pluginRafraichirAuto()
			#ouverture du menu de telechargement
			elif choice == 't' or choice == 'T': dl(DLlist)	
			#ouverture de l'invite de fermeture		
			elif choice == 'q' or choice == 'Q': quitter()
			#actualisation de l'affichage ecran
			elif choice == 'i' or choice == 'I': info()
			#actualisation de l'affichage ecran
			elif choice == 'a' or choice == 'A':
				header(selectedPlugin,selectedChaine,selectedProgram)
				print  "\n\n\n\n\t\tRafraichissement\n\n\n"
				self.api.pluginRafraichirAuto()
				#recharger les listes 
				if len(selectedProgram)!=0:
					fichiers = self.api.getPluginListeFichiers(selectedPlugin,selectedProgram)
				elif len(selectedChaine)!=0:
					programs = self.api.getPluginListeEmissions(selectedPlugin,selectedChaine)
				elif len(selectedPlugin)!=0:
					chaines = self.api.getPluginListeChaines(selectedPlugin)
				elif len(selectedPlugin)==0 and len(selectedChaine)==0 and len(selectedProgram)==0:
					plugins = self.preferences.getPreference( "pluginsActifs" )
					plugins.sort()
				#mise a jour de l'affichage
				header(selectedPlugin,selectedChaine,selectedProgram)
				print  "\n\n\n\n\t\tVeuillez patientez pendant la mise a jour des informations\n\n\n"
				time.sleep(1)
				show(selectedPlugin,selectedChaine,selectedProgram,temp)
			elif choice == 'r' or choice == 'R':
				temp=0
				if len(selectedProgram)!=0:
					selectedProgram=""
				elif len(selectedChaine)!=0:
					selectedChaine=""
					if len(chaines)==1:
						selectedPlugin=""
				elif len(selectedPlugin)!=0:
					selectedPlugin=""
			elif choice.isdigit() and int(choice)>=0:
				choice=10*temp+int(choice)
				if len(selectedPlugin)==0 and len(plugins)>choice:
					temp=0
					selectedPlugin = plugins[choice]
					chaines = self.api.getPluginListeChaines(selectedPlugin)
					if len(chaines)==1:
						header(selectedPlugin,'','')
						print "Une seule chaine :",chaines
						time.sleep (0.5)
						selectedChaine=chaines[0]
						programs = self.api.getPluginListeEmissions(selectedPlugin,selectedChaine)
				elif len(selectedChaine)==0 and len(chaines)>choice:
					temp=0
					selectedChaine=chaines[choice]
					programs = self.api.getPluginListeEmissions(selectedPlugin,selectedChaine)
				elif len(selectedProgram)==0 and len(programs)>choice:
					selectedProgram=programs[choice]
					header(selectedPlugin,selectedChaine,selectedProgram)
					print  "\n\n\n\n\t\tVeuillez patientez pendant le chargement des informations\n\n\n"
					fichiers = self.api.getPluginListeFichiers(selectedPlugin,selectedProgram)
					if len(fichiers)==0:
						header (selectedPlugin,selectedChaine,selectedProgram)
						print "\n\n\n\n\n\n\n\t\tAucun fichier dans le programme :",selectedProgram
						time.sleep (1)
						selectedProgram=''
					else:temp=0
				elif len(selectedPlugin)!=0 and len(selectedChaine)!=0 and len(selectedProgram)!=0 and len(fichiers)>choice:
					header(selectedPlugin,selectedChaine,selectedProgram)
					if fichiers[choice] not in DLlist:
						print  "\n\n\n\n\n\n\najout",fichiers[choice].nom,"a la liste de telechargement\n\n\n\n\n\n\n\n\n"
						DLlist.append(fichiers[choice])
					else: print  "\n\n\n\n\n\n\n\t\tFichier deja dans la liste de telechargement\n\n\n\n\n\n\n\n\n"
					time.sleep(1)
					os.system(['clear','cls'][os.name == 'nt'])

			elif choice=='*':
#				if len(selectedPlugin)==0:
#					temp=0
#					selectedPlugin = 'None'
#					chaines = self.api.getPluginListeChaines()
#				elif len(selectedChaine)==0:
#					temp=0
#					selectedChaine='None'
#					programs = self.api.getPluginListeEmissions(selectedPlugin,selectedChaine)
#				el
				if len(selectedProgram)==0:
					selectedProgram='Tous'
					header(selectedPlugin,selectedChaine,selectedProgram)
					print  "\n\n\n\n\t\tVeuillez patientez pendant le chargement des informations\n\n\n"
#					for choice in range(len(programs)) :
					fichiers = self.api.getPluginListeFichiers(selectedPlugin,None)#programs[choice])
				elif len(selectedPlugin)!=0 and len(selectedChaine)!=0 and len(selectedProgram)!=0:
					header(selectedPlugin,selectedChaine,selectedProgram)
					for choice in range(len(fichiers)) :
						if fichiers[int(choice)] not in	DLlist:
							header(selectedPlugin,selectedChaine,selectedProgram)
							print "\n\n\n\n\t\tajout",fichiers[int(choice)].nom,"a la liste de telechargement"
							DLlist.append(fichiers[int(choice)])
						else: print "\t\tFichier deja dans la liste de telechargement"
						time.sleep(0.5)

				#afficher la suite de la liste
			elif choice=='+':
				if len(selectedPlugin) ==  0:
					if len(plugins)>temp*10+10: temp+=1
				elif len(selectedChaine) ==  0:
					if len(chaines)>temp*10+10: temp+=1
				elif len(selectedProgram) ==  0:
					if len(programs)>temp*10+10: temp+=1
				elif len(selectedPlugin) !=  0 and len(selectedChaine) !=  0 and len(selectedProgram) !=  0:
					if len(fichiers)>temp*10+10: temp+=1
				#afficher le debut de la liste
			elif choice=='-':
				if temp!=0: temp-=1
			show(selectedPlugin,selectedChaine,selectedProgram,temp)
			choice=''
#			if not choice:choice=raw_input("\n\t\tEntrez votre choix : ")
			if not choice:choice=getch()
#			if len(choice)>1:choice=choice[0]
	#			if choice:print choice[0]
	#split
if __name__=="__main__": 
	main()
