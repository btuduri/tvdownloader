#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from tvdcore import Fichier
from tvdcore import Plugin

class DevPlugin( Plugin ):
	
	DATA = {
		"Image Google": {
			"Lapins": [
				Fichier("Lapin mignon",
					lien="http://www.bestioles.ca/mammiferes/images/lapin.jpg",
					nomFichierSortie="Lapin mignon.jpg",
					urlImage = "http://www.bestioles.ca/mammiferes/images/lapin.jpg",
					descriptif = "Le lapin est un petit mammifère qui nous vient d'Europe. Les moines du Moyen Age l'ont domestiqué, pour sa chair et sa fourrure. Cependant, le lapin Angora et la Zibeline sont élevés pour leur poil soyeux."),
				Fichier("Bugs bunny",
					lien="http://www.cuniculture.info/Docs/Phototheque/Dessins/BugsBunny/Bugs-dessins/bugs-dessin-083.jpg",
					nomFichierSortie="Bugs Bunny.jpg",
					urlImage="http://www.cuniculture.info/Docs/Phototheque/Dessins/BugsBunny/Bugs-dessins/bugs-dessin-083.jpg",
					descriptif="On ne le présente plus.")
			],
			"Chats": [
				Fichier("Bébé chat :)",
					lien="http://images.doctissimo.fr/1/animaux/passion-fonds-ecrans/photo/hd/1914725191/1799052ade/passion-fonds-ecrans-chat-big.jpg",
					nomFichierSortie="Chaton.jpg",
					urlImage="http://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Cat_silhouette.svg/150px-Cat_silhouette.svg.png",
					descriptif="Un bébé chat tout mimi."
				)
			]
		},
		"Fichier divers": {
			"Logiciel": [
				Fichier("Avast 7",
					lien="http://ftp01net.telechargement.fr/avast_free_antivirus_setup.exe",
					nomFichierSortie="Avast_7.exe",
					urlImage="http://videonoob.fr/wp-content/uploads/logo-avast-antivirus-5.png",
					descriptif="Antivirus gratuit !"
				)
			]
		}
	}
	
	def __init__( self ):
		Plugin.__init__( self, "DevPlugin", "http://www.google.fr/", 7 )
	
	def listerChaines( self ):
		for nom in DevPlugin.DATA.keys():
			self.ajouterChaine(nom)
	
	def listerEmissions( self, chaine ):
		if DevPlugin.DATA.has_key(chaine):
			for emission in DevPlugin.DATA[chaine].keys():
				self.ajouterEmission(chaine, emission)
	
	def listerFichiers( self, emission ):
		for chaine in DevPlugin.DATA.keys():
			if DevPlugin.DATA[chaine].has_key(emission):
				for fichier in DevPlugin.DATA[chaine][emission]:
					self.ajouterFichier(emission, fichier)
	
	
