#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier LICENSE #
#########################################

#~ Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
#~ Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
#~ Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import os

from Plugin import Plugin
from Fichier import Fichier
from urllib import quote
import re,unicodedata,datetime

##########
# Classe #
##########

class Pluzz( Plugin ):
	"""Classe abstraite Plugin dont doit heriter chacun des plugins"""
	
	listeChainesEmissionsUrl = "http://www.pluzz.fr/appftv/webservices/video/catchup/getListeAutocompletion.php"
	listeChainesEmissionsPattern = re.compile("chaine_principale=\"(.*?)\".*?.\[CDATA\[(.*?)\]\]")
	
	lienEmissionBaseUrl = "http://www.pluzz.fr/"
	
	videoInfosBaseUrl = "http://www.pluzz.fr/appftv/webservices/video/getInfosVideo.php?src=cappuccino&video-type=simple&template=ftvi&template-format=complet&id-externe="
	videoTitrePattern = re.compile("titre.public><.\[CDATA\[(.*?)]]>", re.DOTALL)
	videoNomPattern = re.compile("nom><.\[CDATA\[(.*?)]]>", re.DOTALL)
	videoCheminPattern = re.compile("chemin><!\[CDATA\[(.*?)]]>", re.DOTALL)
	videoDatePattern = re.compile("date><!\[CDATA\[(.*?)]]>", re.DOTALL)
	
	def __init__( self):
		Plugin.__init__( self, "Pluzz", "http://www.pluzz.fr/")
		
		cache = self.chargerCache()
		if cache:
			self.listeChaines = cache
		else:
			self.listeChaines = {}
	
	def listerOptions(self):
		self.optionBouleen("france2", "Afficher France 2", True)
		t = []
		if self.listeChaines.has_key("france2"):
			t = self.listeChaines["france2"]
			t.sort()
		self.optionChoixMultiple("emissionsfrance2", "Liste des émissions à afficher pour France 2", t, t)
		
		self.optionBouleen("france3", "Afficher France 3", True)
		t = []
		if self.listeChaines.has_key("france3"):
			t = self.listeChaines["france3"]
			t.sort()
		self.optionChoixMultiple("emissionsfrance3", "Liste des émissions à afficher pour France 3", t, t)
		
		self.optionBouleen("france4", "Afficher France 4", True)
		t = []
		if self.listeChaines.has_key("france4"):
			t = self.listeChaines["france4"]
			t.sort()
		self.optionChoixMultiple("emissionsfrance4", "Liste des émissions à afficher pour France 4", t, t)
		
		self.optionBouleen("france5", "Afficher France 5", True)
		t = []
		if self.listeChaines.has_key("france5"):
			t = self.listeChaines["france5"]
			t.sort()
		self.optionChoixMultiple("emissionsfrance2", "Liste des émissions à afficher pour France 5", t, t)
		
		self.optionBouleen("franceo", "Afficher France O", True)
		t = []
		if self.listeChaines.has_key("franceo"):
			t = self.listeChaines["franceo"]
			t.sort()
		self.optionChoixMultiple("emissionsfranceo", "Liste des émissions à afficher pour France O", t, t)
	
	def rafraichir( self ):
		self.listeChaines = {}
		self.afficher("Récupération de la liste des émissions...")
		for item in re.findall(self.listeChainesEmissionsPattern, self.API.getPage(self.listeChainesEmissionsUrl)):
			if not(self.listeChaines.has_key(item[0])):
				self.listeChaines[item[0]] = []
			self.listeChaines[item[0]].append(item[1])
		self.sauvegarderCache(self.listeChaines)
	
	def getLienEmission(self, emission):
		s = re.sub("[,: !/'\.]+", "-", emission).replace( ',', '' ).lower()
		s = unicode( s, "utf8", "replace" )
		s = unicodedata.normalize( 'NFD',s )
		#~ return self.lienEmissionBaseUrl+unicodedata.normalize( 'NFD', s).encode( 'ascii','ignore' )+".html"
		return self.lienEmissionBaseUrl+quote(s.encode( 'ascii','ignore' ))+".html"
	
	def listerChaines( self ):
		t = self.listeChaines.keys()
		t.sort()
		for chaine in t:
			if self.getOption(chaine) == True:
				self.ajouterChaine(chaine)
	
	def listerEmissions( self, chaine ):
		#~ t = []
		#~ if self.listeChaines.has_key(chaine):
			#~ t = self.listeChaines[chaine]
			#~ t.sort()
		t = self.getOption("emissions"+chaine)
		if not(t):
			t = []
			if self.listeChaines.has_key(chaine):
				t = self.listeChaines[chaine]
				t.sort()
		for emission in t:
			self.ajouterEmission(chaine, emission)
	
	def listerFichiers( self, emission ):
		lien = self.getLienEmission(emission)
		base = lien.replace(".html", "")
		
		self.afficher("Récupération de la liste des fichiers pour \""+emission+"\"...")
		dejaVue = []
		nombre = 0
		videos = re.findall("("+base+".+?.html)", self.API.getPage(lien));
		if videos == None:
			return
		videos.append(lien)
		for fichier in videos:
			fichierInfosUrl_match = re.search(re.compile("info.francetelevisions.fr/\?id-video=(.+?)\"", re.DOTALL), self.API.getPage(fichier))
			if fichierInfosUrl_match == None:
				continue
			fichierInfos = self.API.getPage(self.videoInfosBaseUrl+fichierInfosUrl_match.group(1))
			
			titre = re.search(self.videoTitrePattern, fichierInfos)
			if titre != None:
				titre = titre.group(1)
			else:
				continue
			nom = re.search(self.videoNomPattern, fichierInfos)
			if nom != None:
				nom = nom.group(1)
			else:
				continue
			chemin = re.search(self.videoCheminPattern, fichierInfos)
			if chemin != None:
				chemin = chemin.group(1)
			else:
				continue
			date =  re.search(self.videoDatePattern, fichierInfos)
			if date != None:
				date = datetime.date.fromtimestamp(int(date.group(1))).strftime("%d/%m/%Y")
			else:
				continue
			
			if titre in dejaVue:
				continue
			else:
				dejaVue.append(titre)
			
			lien = None
			if( chemin.find( 'http' ) != -1 ):
				lien = chemin + titre
			elif( nom.find( 'wmv' ) != -1 ):
				lien = "mms://a988.v101995.c10199.e.vm.akamaistream.net/7/988/10199/3f97c7e6/ftvigrp.download.akamai.com/10199/cappuccino/production/publication" + chemin + nom
			elif( nom.find( 'mp4' ) != -1 ):
				lien = "rtmp://videozones-rtmp.francetv.fr/ondemand/mp4:cappuccino/publication" + chemin + nom
			if not(lien):
				continue
			self.ajouterFichier(emission, Fichier( titre, date, lien ) )
			nombre = nombre+1
		self.afficher(str(nombre)+" fichiers trouvés.")

