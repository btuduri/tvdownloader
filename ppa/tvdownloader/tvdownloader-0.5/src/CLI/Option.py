#/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from CLI.Screen import header,footer
from Downloader import Downloader
from Preferences import Preferences
from Historique import Historique
from getch import getch

class dl:
	def __init__(self, DLlist):
		# On instancie le gestionnaire de preferences et sa fenetre
		self.preferences = Preferences()
		# On instancie le gestionnaire de download
		self.downloader = Downloader()
		# On instancie le gestionnaire d'historique et sa fenetre
		self.historique = Historique()
		current=0
		global choice
		choice=''
		while choice!='r' and choice!='R':	
			if choice=='s' or choice=='S':
				os.system(['clear','cls'][os.name == 'nt'])
				header ('','','Liste de telechargement')
				print "\n\n\n\tSupprimer tous les fichiers de la liste de telchargement"
				#pour chaque fichier de la liste  ***(len(DLlist))!=0
				while len(DLlist)>0:
					print "Supprimer le fichier :",DLlist[0].nom
					#supprimer le fichier de la liste
					DLlist.remove(DLlist[0])
					#ajouter le fichier au log
					time.sleep (1)	
			if choice=='t' or choice=='T':
				os.system(['clear','cls'][os.name == 'nt'])
				header ('','','Liste de telechargement')
				print "\n\n\n\ttelecharger tous les fichiers"
				#pour chaque fichier de la liste  ***(len(DLlist))!=0
				while len(DLlist)>0:
					if not self.historique.comparerHistorique(DLlist[0]):
						os.system(['clear','cls'][os.name == 'nt'])
						header ('','','Liste de telechargement')
						print "\n\n\n\ttelecharger le fichier :",DLlist[0].nom
						if(DLlist[0].nomFichierSortie=="" ):
							DLlist[0].nomFichierSortie=os.path.basename(getattr(DLlist[0],"lien" ))
						#telecharger le fichier
						self.downloader.lancerTelechargement([[0,DLlist[0].lien,DLlist[0].nomFichierSortie]])
						#ajouter le fichier a l'historique de telechargement
						self.historique.ajouterHistorique(DLlist[0])		
					else:
						os.system(['clear','cls'][os.name == 'nt'])
						header ('','','Liste de telechargement')
						print "\n\n\n\tFichier deja telecharge"
					#supprimer le fichier de la liste
					DLlist.remove(DLlist[0])
					time.sleep (1)
			elif choice=='q' or choice=='Q':
				quitter()
			elif choice.isdigit() and len(DLlist)>int(choice)+10*current and int(choice)>=0:
				value=''
				while (value!='r' and value!='t' and value!='s'):
					os.system(['clear','cls'][os.name == 'nt'])
					header ('','','Liste de telechargement')
					print "\n\n\n\tFichier :",DLlist[int(choice)+10*current].nom,"\n\n\tQue voulez vous faire?\n\n\t\tt:telecharger le fichier\n\t\ts:supprimer le fichier de la liste de telechargement\n\t\tr:retour a liste de telechargement\n\n\n\n\n"
					value=getch()
				if value=='t':
					if not self.historique.comparerHistorique(DLlist[int(choice)+10*current]):
						os.system(['clear','cls'][os.name == 'nt'])
						header ('','','Liste de telechargement')
						print "\n\n\n\ttelecharger le fichier :",DLlist[int(choice)].nom
						# Si le nom du fichier de sortie n'existe pas, on l'extrait de l'URL
						if(DLlist[int(choice)+10*current].nomFichierSortie=="" ):
							DLlist[int(choice)+10*current].nomFichierSortie=os.path.basename(getattr(DLlist[int(choice)+10*current],"lien" ))
						#telecharger le fichier
						self.historique.ajouterHistorique(DLlist[int(choice)+10*current])
						self.downloader.lancerTelechargement([[0,DLlist[int(choice)].lien,DLlist[int(choice)].nomFichierSortie]])
						#ajouter le fichier a l'historique de telechargement
					else:
						os.system(['clear','cls'][os.name == 'nt'])
						header ('','','Liste de telechargement')
						print "\n\n\n\tFichier deja telecharge"
					time.sleep(1)
					#supprimer le fichier de la liste
					DLlist.remove(DLlist[int(choice)])
				elif value=='s':
					os.system(['clear','cls'][os.name == 'nt'])
					header ('','','Liste de telechargement')
					print "\n\n\n\tSuppression de la liste de telechargement du fichier :\n\n\t\t",DLlist[int(choice)].nom
					#supprimer le fichier de la liste
					DLlist.remove(DLlist[int(choice)])
				elif value=='r':
					os.system(['clear','cls'][os.name == 'nt'])
					header ('','','Liste de telechargement')
					print "\n\n\n\tRetour a la liste de telechargement"
				#ajouter le fichier au log
				time.sleep(1)
			elif choice=='*' :
				value=''
				os.system(['clear','cls'][os.name == 'nt'])
				header ('','','Liste de telechargement')
				print "\n\n\n\n\n\tQue voulez vous faire?\n\n\t\tt:telecharger les fichiers\n\t\ts:supprimer les fichiers de la liste de telechargement\n\n\n\n\n\n"
				value=getch()
				while len(DLlist)>0:
					if value=='t':
						if not self.historique.comparerHistorique(DLlist[0]):
							os.system(['clear','cls'][os.name == 'nt'])
							header ('','','Liste de telechargement')
							print "\n\n\n\ttelecharger le fichier :",DLlist[0].nom
							# Si le nom du fichier de sortie n'existe pas, on l'extrait de l'URL
							if(DLlist[0].nomFichierSortie=="" ):
								DLlist[0].nomFichierSortie=os.path.basename(getattr(DLlist[0],"lien" ))
							#telecharger le fichier
							self.downloader.lancerTelechargement([[0,DLlist[0].lien,DLlist[0].nomFichierSortie]])
							#ajouter le fichier a l'historique de telechargement
							self.historique.ajouterHistorique(DLlist[0])
						else:
							os.system(['clear','cls'][os.name == 'nt'])
							header ('','','Liste de telechargement')
							print "\n\n\n\tFichier deja telecharge"	
							time.sleep(0.5)
					#supprimer le fichier de la liste
					DLlist.remove(DLlist[0])
					#ajouter le fichier au log
			elif choice=='+':
				if len(DLlist)>current*10+10: current+=1
			elif choice=='-':
				if current!=0: current-=1
			choice=''
			#sauvegarder l'historique de telechargement
			self.historique.sauverHistorique()
			#affichage a l'ecran de la liste
			header ('','','Liste de telechargement')
			for i in range(10):
				if len(DLlist)>i+10*current:
					if len(DLlist[int(i+10*current)].nom)>74: print " ",i,":",DLlist[int(i+10*current)].nom[:71]+"..."
					elif len(DLlist[int(i+10*current)].nom)<=74: print " ",i,":",DLlist[int(i+10*current)].nom
				else: print ""
			if len(DLlist)>10:print "\n\t+:fichiers suivants\t-:fichiers precedents  (page",current+1,"/",len(DLlist)/10+1,",",len(DLlist),"chaines)"
			else:print"\n"
			print "\n\tt:telecharger tous les fichiers  s:supprimer tous les fichiers"
			footer()
			if len(DLlist)==0:
				os.system(['clear','cls'][os.name == 'nt'])
				header ('','','Liste de telechargement')
				print "\n\n\n\n\n\t\tAucun fichier dans la liste"
				footer()
				choice='r'
				time.sleep(1)
			if not choice:choice=getch()

class prefs:
	def __init__(self):

		from API import API
		from APIPrive import APIPrive
		from PluginManager import PluginManager

		################################################
		# Instanciations + initialisation de variables #
		################################################
		# On instancie le plugin manager
		self.pluginManager = PluginManager()
		# On instancie le gestionnaire de preferences et sa fenetre
		self.preferences = Preferences()
		# On instancie le gestionnaire de download
		self.downloader = Downloader()
		# On instancie seulement les plugins qui sont selectionnes dans les preferences
		#~ self.pluginManager.activerPlugins( self.preferences.getPreference( "pluginsActifs" ) )		
		# On recupere l'instance de API
		self.api = API.getInstance()
		# On met en place la liste des plugins dans API

		current=0
		global choice
		choice=''
		while choice!='r' and choice!='R':
		
	#		self.api.setListeInstance( getattr( self.pluginManager, "listeInstances" ) )
			pluginsActifs = self.pluginManager.listeInstances
			plugins = self.pluginManager.getListeSites()
			rep= self.preferences.getPreference( "repertoireTelechargement" )
		
			if choice=='q' or choice=='Q':
				quitter()
			elif choice.isdigit():
				if plugins[int(choice)-1] in pluginsActifs:
					self.pluginManager.desactiverPlugin(plugins[int(choice)-1])
				else:
					self.pluginManager.activerPlugin(plugins[int(choice)-1])
				self.preferences.sauvegarderConfiguration()
		
			elif choice=='m' or choice =='M':
				os.system(['clear','cls'][os.name == 'nt'])
				header ('','','Repertoire de telechargement')
				choice=raw_input('\n\n\n\n\n\n\n\tVeuillez saisir un repertoire valide\n\n\t\t')
				if not os.path.isdir(choice):
					os.system(['clear','cls'][os.name == 'nt'])
					header ('','','Repertoire de telechargement')
					print "\n\n\n\n\n\n\n\trepertoire ",choice," inexistant\n\n\t\tRepertoire courant:",rep
				else :
					os.system(['clear','cls'][os.name == 'nt'])
					header ('','','Repertoire de telechargement')
					rep=choice
					print "\n\n\n\n\n\n\n\tModification du repertoire de telechargement :\n\n\t\tNouveau repertoire :",choice
					self.preferences.setPreference( "repertoireTelechargement", str(rep))
				time.sleep(1)
			elif choice=='+':
				if len(DLlist)>current*15+15: current+=1
			elif choice=='-':
				if current!=0: current-=1
		
			#affichage a l'ecran de la liste
			header ('','','Menus des options')
			print "  Repertoire de telechargement :",rep
			for i in range(10) :
				if i+10*current<len(plugins):
					print "\n ",i+10*current+1,":",plugins[i+14*current],
					if len(plugins[i+10*current])<=8:print"\t\t",
					elif len(plugins[i+10*current])<=15:print"\t",
					for j in pluginsActifs:
						if j==plugins[i+10*current]:
							print "\t",i+10*current+1,"actif",
				else: print ""
			print "\n\n  m:modifier le repertoire de telechargement"
			footer()
			choice=getch()
		self.preferences.sauvegarderConfiguration()

def info():
	choice=''
	while choice!='r' and choice!='R':
		header ('','','Credits & license')
		print "\t\t\tGNU GENERAL PUBLIC LICENSE"                       
		print "\t\t\tVersion 2, June 1991"
		print ""
		print ""
		print ""
		print "\t\t\tDéveloppeurs :"
		print "\t\t\t\t- chaoswizard"
		print "\t\t\t\t- ggauthier.ggl"
		print "\t\t\t\t"
		print "\t\t\tDéveloppeur CLI :"
		print "\t\t\t\ttvelter"
		print ""
		print "\t\t\tPlugins :"
		print "\t\t\t\tBmD_Online"
		print ""
		print ""
		footer()
		if choice=='q' or choice=='Q':
			quitter()
		choice=getch()

def quitter():
	#quitter program apres confirmation utilisateur
	choice = ""
	if not choice :
		os.system(['clear','cls'][os.name == 'nt'])
		sys.exit()
		header ('','Quitter ?','')
		print "\n\n\n\n\n\t\tAre you sure you want to quit ? (y/n)"
		choice=getch()
	if choice=='y' or choice=='Y': 
		os.system(['clear','cls'][os.name == 'nt'])
		sys.exit()
	elif choice!='y' and choice!='Y':
		os.system(['clear','cls'][os.name == 'nt'])
		header ('','Quitter ?','')
		print "\n\n\n\n\n\t\tRetour a l'interface du programme"
		print "#"
		time.sleep(1)
		print "#"
		os.system(['clear','cls'][os.name == 'nt'])

# @param time: duree d'affichage du message d'attente
def wait(duree):
        #Affichage d'un message d'attente pendant le chargement des infos ou le telechargmeent des fichiers
        # Fenetre d'attente
        os.system(['clear','cls'][os.name == 'nt'])
        print "Patientez pendant l'actualisation des informations"
        #while get info not finished
	for i in range(duree):
	 	time.sleep(1)
        	print "#",
        #os.system(['clear','cls'][os.name == 'nt'])
