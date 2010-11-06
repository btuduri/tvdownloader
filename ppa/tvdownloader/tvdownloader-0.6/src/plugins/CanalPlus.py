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

import re

from Fichier import Fichier
from Plugin import Plugin
from API import API
import pickle,os.path

##########
# Classe #
##########
#***
# Dernière mise à jour: 16/07/2010
class CanalPlus(Plugin):
	"""Plugin pour le site canalplus.fr."""
	listeEmissionsUrl = "http://www.canalplus.fr/"
	listeEmissionsPattern = re.compile("<div class=\"col[^\"]*\">.*?<h3>[\w ]+</h3>(.+?)</div>", re.IGNORECASE|re.DOTALL)
	listeEmissionsSubPattern0 = re.compile(" href=\"(http://www.canalplus.fr/pid\d+?.htm)\">(.+?)</", re.IGNORECASE|re.DOTALL)
	listeEmissionsSubPattern = re.compile(" href=\"(.+?)\">([^<]+?)</", re.IGNORECASE|re.DOTALL)
	emissions_NOM = 1
	emissions_LIEN = 0
	
	listeFichiersPattern = re.compile("switchVideoPlayer\(([0-9]+?)\)|switchTheVideo\(([0-9]+?)\)|aVideos\[.+?\]\[.CONTENT_ID.\] = \"([0-9]+?)\"|DisplayVideo\(([0-9]+?)\)",re.DOTALL)
	
	fichierInfosBaseUrl = "http://webservice.canal-plus.com/rest/bigplayer/getVideosLiees/"
	fichierInfosPattern0 = re.compile("VIDEO.*?ID>(.+?)</ID.*?DATE>(.+?)</DATE.*?TITRE>(.+?)</TITRE.*?SOUS_TITRE>(.+?)</SOUS.*?BAS_DEBIT>(.+?)</BAS", re.IGNORECASE|re.DOTALL)
	fichierInfosPattern = re.compile("VIDEO.*?ID>(?P<id>.+?)</ID.*?DATE>(?P<date>.+?)</DATE.*?TITRE>(?P<titre>.+?)</TITRE.*?SOUS_TITRE>(?P<sstitre>.+?)</SOUS.*?BAS_DEBIT>(?P<LQ>.+?)</BAS.*?(<HAUT_DEBIT>(?P<MQ>.+?)</HAUT_DEBIT>|<HAUT_DEBIT/>).*?(<HD>(?P<HQ>.+?)</HD>|<HD/>)", re.IGNORECASE|re.DOTALL)
	
	def __init__( self):
		Plugin.__init__(self, "Canal+", "http://www.canalplus.fr/", 30)
		self.listeEmissions = {}#clé: nom de l'émission, valeur: lien de la page sur canalplus.fr
		
		if os.path.exists(self.fichierCache):
			file = open(self.fichierCache, "r")
			self.listeEmissions = pickle.load(file)
			file.close()
	
	def listerOptions(self):
		self.optionChoixUnique("qualite", "Qualité maximales des vidéos", "Basse", ["Basse", "Normal", "Haute"])
		self.optionBouleen("tout_afficher", "Afficher plusieurs fois une diffusion si plusieurs qualité sont disponible", True)
		l = self.listeEmissions.keys()
		l.sort()
		self.optionChoixMultiple("emissions", "Liste des émissions à afficher", l, l)
		self.optionChoixUnique("Qpos", "Afficher la qualité dans le nom du fichier sauvegardé (LQ, MQ, HQ)", "Fin", ["Non", "Début", "Fin"])
	
	def rafraichir( self ):
		print self.nom+":","Récupération de la liste des émissions..."
		nomParUrl = {}
		self.listeEmissions = {}
		#~ for emission in re.findall(self.listeEmissionsSubPattern, self.API.getPage(self.listeEmissionsUrl)):
			#~ self.listeEmissions[emission[self.emissions_NOM]] = emission[self.emissions_LIEN]
			#~ nomParUrl[emission[self.emissions_LIEN]] = emission[self.emissions_NOM]
		for col in re.findall(self.listeEmissionsPattern, self.API.getPage(self.listeEmissionsUrl)):
			for emission in re.findall(self.listeEmissionsSubPattern, col):
				lien = emission[self.emissions_LIEN]
				if lien[0] == "/":
					lien = "http://www.canalplus.fr"+lien
				self.listeEmissions[emission[self.emissions_NOM]] = lien
				nomParUrl[lien] = emission[self.emissions_NOM]
				#~ print '"'+lien+'",'
		
		import sys
		print len(self.listeEmissions),len(nomParUrl)
		#~ for k in self.listeEmissions.keys():
			#~ print k,self.listeEmissions[k]
		#~ print ''
		#~ for k in nomParUrl.keys():
			#~ print k,nomParUrl[k]
		#~ crash()
		
		print self.nom+":",len(self.listeEmissions),"émissions trouvées."
		print self.nom+":","Vérification de la présence de fichier..."
		pages = self.API.getPages(self.listeEmissions.values())
		for url in pages.keys():
			if re.search(self.listeFichiersPattern, pages[url]) != None:
				self.afficher("\""+nomParUrl[url]+"\" conservé.")
				self.ajouterEmission(self.nom, nomParUrl[url])
			else:
				self.afficher("\""+nomParUrl[url]+"\" ignoré.")
		
		file = open(self.fichierCache, "w")
		pickle.dump(self.listeEmissions, file)
		file.close()
		print self.nom+":",len(self.listeEmissions),"émissions concervées."
	
	def listerChaines( self ):
		self.ajouterChaine(self.nom)

	def listerEmissions( self, chaine ):
		#~ t = self.listeEmissions.keys()
		t = self.getOption("emissions")
		if t == None:
			t = []
		else:
			t.sort()
		for emission in t:
			self.ajouterEmission(chaine, emission)
	
	def listerFichiers( self, emission ):
		print emission
		if not self.listeEmissions.has_key(emission):
			self.afficher("l'émission \""+emission+"\" est inconnu")
			return
		
		opt_ttaff = self.getOption("tout_afficher")
		opt_qual = self.getOption("qualite")
		opt_qpos = self.getOption("Qpos")
		
		liste = {}
		dejaVue = {}
		self.afficher("Récupération de la liste des fichiers pour \""+emission+"\"...")
		page = self.API.getPage(self.listeEmissions[emission])
		self.afficher("Analyse...\r", False)
		for tuple in re.findall(self.listeFichiersPattern, page):
			id = tuple[0]+tuple[1]+tuple[2]+tuple[3]
			if dejaVue.has_key(id):
				continue
			elif liste.has_key(id):
				self.ajouterFichier(emission, liste[id])
			else:
				for fichier in re.finditer(self.fichierInfosPattern, self.API.getPage(self.fichierInfosBaseUrl+id)):
					if opt_ttaff:
						id2 = fichier.group("id")+"LQ"
						if not(liste.has_key(id2)):
							nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
							nomAfficher = nomFichier
							nomFichier = nomFichier.replace("/", "-")
							if opt_qpos == "Début":
								nomFichier = "LQ "+nomFichier
							elif opt_qpos == "Fin":
								nomFichier = nomFichier+" LQ"
							nomFichier = nomFichier+".flv"
							f = Fichier("[LQ]"+nomAfficher, fichier.group("date"), fichier.group("LQ"), nomFichier)
							#~ f = Fichier("[SD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("SD"))
							liste[id2] = f
						if not dejaVue.has_key(id2):
							self.ajouterFichier(emission, liste[id2])
						dejaVue[id2] = True
						
						if opt_qual == "Haute":
							if fichier.group("HQ"):
								id2 = fichier.group("id")+"HQ"
								if not(liste.has_key(id2)):
									nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
									nomAfficher = nomFichier
									nomFichier = nomFichier.replace("/", "-")
									if opt_qpos == "Début":
										nomFichier = "HQ "+nomFichier
									elif opt_qpos == "Fin":
										nomFichier = nomFichier+" HQ"
									nomFichier = nomFichier+".mp4"
									f = Fichier("[HQ]"+nomAfficher, fichier.group("date"), fichier.group("HQ"), nomFichier)	
									#~ f = Fichier("[HD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("HD"))
									liste[id2] = f
								if not dejaVue.has_key(id2):
									self.ajouterFichier(emission, liste[id2])
								dejaVue[id2] = True
							
							if fichier.group("MQ"):
								id2 = fichier.group("id")+"MQ"
								if not(liste.has_key(id2)):
									nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
									nomAfficher = nomFichier
									nomFichier = nomFichier.replace("/", "-")
									if opt_qpos == "Début":
										nomFichier = "MQ "+nomFichier
									elif opt_qpos == "Fin":
										nomFichier = nomFichier+" MQ"
									nomFichier = nomFichier+".flv"
									f = Fichier("[MQ]"+nomAfficher, fichier.group("date"), fichier.group("MQ"), nomFichier)	
									#~ f = Fichier("[MD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("MD"))
									liste[id2] = f
								if not dejaVue.has_key(id2):
									self.ajouterFichier(emission, liste[id2])
								dejaVue[id2] = True
						elif opt_qual == "Normal":
							if fichier.group("MQ"):
								id2 = fichier.group("id")+"MD"
								if not(liste.has_key(id2)):
									nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
									nomAfficher = nomFichier
									nomFichier = nomFichier.replace("/", "-")
									if opt_qpos == "Début":
										nomFichier = "MQ "+nomFichier
									elif opt_qpos == "Fin":
										nomFichier = nomFichier+" MQ"
									nomFichier = nomFichier+".flv"
									f = Fichier("[MQ]"+nomAfficher, fichier.group("date"), fichier.group("MQ"), nomFichier)	
									#~ f = Fichier("[MD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("MD"))
									liste[id2] = f
								if not dejaVue.has_key(id2):
									self.ajouterFichier(emission, liste[id2])
								dejaVue[id2] = True
					else:
						if opt_qual == "Haute":
							if fichier.group("HQ"):
								id2 = fichier.group("id")+"HQ"
								if not(liste.has_key(id2)):
									nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
									nomAfficher = nomFichier
									nomFichier = nomFichier.replace("/", "-")
									if opt_qpos == "Début":
										nomFichier = "HQ "+nomFichier
									elif opt_qpos == "Fin":
										nomFichier = nomFichier+" HQ"
									nomFichier = nomFichier+".mp4"
									f = Fichier("[HQ]"+nomAfficher, fichier.group("date"), fichier.group("HQ"), nomFichier)
									#~ f = Fichier("[HD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("HD"))
									liste[id2] = f
								if not dejaVue.has_key(id2):
									self.ajouterFichier(emission, liste[id2])
								dejaVue[id2] = True
						elif opt_qual == "Normal":
							if fichier.group("MQ"):
								id2 = fichier.group("id")+"MQ"
								if not(liste.has_key(id2)):
									nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
									nomAfficher = nomFichier
									nomFichier = nomFichier.replace("/", "-")
									if opt_qpos == "Début":
										nomFichier = "MQ "+nomFichier
									elif opt_qpos == "Fin":
										nomFichier = nomFichier+" MQ"
									nomFichier = nomFichier+".flv"
									f = Fichier("[MQ]"+nomAfficher, fichier.group("date"), fichier.group("MQ"), nomFichier)	
									#~ f = Fichier("[MD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("MD"))
									liste[id2] = f
								if not dejaVue.has_key(id2):
									self.ajouterFichier(emission, liste[id2])
								dejaVue[id2] = True
						else:
							if fichier.group("LQ"):
								id2 = fichier.group("id")+"LQ"
								if not(liste.has_key(id2)):
									nomFichier = (fichier.group("titre")+" ("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>","")
									nomAfficher = nomFichier
									nomFichier = nomFichier.replace("/", "-")
									if opt_qpos == "Début":
										nomFichier = "LQ "+nomFichier
									elif opt_qpos == "Fin":
										nomFichier = nomFichier+" LQ"
									nomFichier = nomFichier+".flv"
									f = Fichier("[LQ]"+nomAfficher, fichier.group("date"), fichier.group("LQ"), nomFichier)
									#~ f = Fichier("[SD]"+(fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("SD"))
									liste[id2] = f
								if not dejaVue.has_key(id2):
									self.ajouterFichier(emission, liste[id2])
								dejaVue[id2] = True
					#~ print fichier.group("MD")
					#~ print fichier.group("HD")
					#~ if not(liste.has_key(fichier.group("id"))):
						#~ f = Fichier((fichier.group("titre")+"("+fichier.group("sstitre")+")").replace("<![CDATA[","").replace("]]>",""), fichier.group("date"), fichier.group("SD"))
						#~ liste[fichier.group("id")] = f
					#~ if not dejaVue.has_key(fichier.group("id")):
						#~ self.ajouterFichier(emission, liste[fichier.group("id")])
					#~ dejaVue[fichier.group("id")] = True
			dejaVue[id] = True
		self.afficher(str(len(liste))+" fichiers trouvés.")

