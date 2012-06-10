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

import os,os.path,pickle
from tvdcore import *


##########
# Classe #
##########

## Classe abstraite Plugin dont doit heriter chacun des plugins.
#
# Les plugins doivent hériter de cette classe et redéfinir les méthodes #listerChaines, #listerEmissions et #listerFichiers. Dans ces méthodes il faut procéder au téléchargement des données demandées et les ajouter si ce n'est déjà fait via les méthodes #ajouterChaine, #ajouterEmission et #ajouterFichier.
# La méthode #listerOptions est optionnellement à redéfinir (dans le cas où il y aurai des options).
class Plugin(object):
	
	NAVIGATEUR = Navigateur()
	
	## @var nom
	# Nom du plugin
	
	## @var url
	# Url du site internet du plugin
	
	## @var frequence
	# Nombre de jour avant le rafraichissement automatique du plugin
	
	
	## @var fichierConfiguration
	# Chemin du fichier de configuration
	
	## @var fichierCache
	# Chemin du fichier de cache
	
	## Constructeur
	# @param self le plugin courant
	# @param nom le nom du plugin
	# @param url l'url du site internet
	# @param frequence la fréquence (en jour) de rafraichissement, 0 pour ne jamais rafraichir
	def __init__(self, nom=None, url=None, frequence=7, logo = None):
		self.pluginDatas = {"chaines":[],
			"emissions":{},
			"fichiers":{}}
		self.pluginOptions = []
		
		if nom == None:
			logger.warn("DEPRECATED: il faut préciser le nom du plugin au constructeur")
		else:
			self.nom = nom
		
		if url == None:
			logger.warn("DEPRECATED: il faut préciser l'url du site du plugin au constructeur")
		else:
			self.url = url
		
		self.frequence = frequence		
		self.fichierConfiguration = os.path.join( Constantes.REPERTOIRE_CONFIGURATION, self.nom.replace( " ", "_" )+ ".conf" )
		self.fichierCache = os.path.join( Constantes.REPERTOIRE_CACHE, self.nom.replace( " ", "_" ) + ".cache" )
		self.logo = os.path.join( "plugins", "img", logo )#FIXME Le logo peut être None
	
	## Efface les informations mémorisées.
	# @param self l'objet courant
	def vider(self):
		self.pluginDatas = {"chaines":[],
			"emissions":{},
			"fichiers":{}}
		self.pluginOptions = []
	
	## Effectue le listage des options.
	# Utiliser #optionTexte, #optionCheckbox, #optionListeMultiple et #optionListeUnique pour ajouter des options
	# @param self le plugin courant
	# @return rien
	def listerOptions(self):
		pass
	
	## Rafraichie les informations durable du plugins comme la liste des émissions.
	# Y placer les traitements lourd n'ayant pas besoin d'être fait souvent.
	# @param self le plugin courant
	# @return Rien
	def rafraichir( self ):
		pass
	
	## Effectue le listage des chaînes.
	# Utiliser #ajouterChaine pour ajouter une chaîne à la liste.
	# @param self le plugin courant
	# @return rien
	def listerChaines( self ):
		pass
	
	## Effectue le listage des émissions.
	# Utiliser #ajouterEmission pour ajouter une émission à la liste.
	# @param self le plugin courant
	# @param chaine la chaine
	# @return rien
	def listerEmissions( self, chaine ):
		pass
	
	## Effectue le listage des fichiers.
	# Utiliser #ajouterFichier pour ajouter un fichier à la liste.
	# @param self le plugin courant
	# @param emission l'emission
	# @return Rien
	def listerFichiers( self, emission ):
		pass
	
	## Ajoute une chaine à celle disponible pour ce plugin.
	# A utiliser dans #listerChaines et en remplacement d'un retour de paramètre.
	# @param self le plugin courant
	# @param chaine le nom de la chaine
	# @return Rien
	def ajouterChaine(self, chaine):
		self.pluginDatas["chaines"].append(chaine)
	
	## Ajoute une émission à celle disponible pour ce plugin.
	# A utiliser dans #listerEmissions et en remplacement d'un retour de paramètre.
	# @param self le plugin courant
	# @param chaine le nom de la chaine de l'émission
	# @param emission le nom de l'émission
	# @return Rien
	def ajouterEmission(self, chaine, emission):
		if not self.pluginDatas["emissions"].has_key(chaine):
			self.pluginDatas["emissions"][chaine] = []
		self.pluginDatas["emissions"][chaine].append(emission)
	
	## Ajoute un fichier à ceux disponible pour ce plugin.
	# A utiliser dans #listerFichiers et en remplacement d'un retour de paramètre.
	# @param self le plugin courant
	# @param emission l'emission du fichier
	# @param fichier le fichier
	# @return Rien
	def ajouterFichier(self, emission, fichier):
		if not self.pluginDatas["fichiers"].has_key(emission):
			self.pluginDatas["fichiers"][emission] = []
		self.pluginDatas["fichiers"][emission].append(fichier)
	
	## Affiche le texte "text" dans la console avec en préfixe le nom du plugin.
	# Facilite le déboguage, utilisé cette méthode plutôt que "print".
	# @param self le plugin courant
	# @param text le texte à afficher en console
	# @param ligne paramètre inutile, conservé par rétrocompatibilité
	# @return Rien
	def afficher(self, text, ligne=None):
		if ligne != None:
			logger.warn("Le paramètre ligne n'a plus aucun effet.")
		logger.info(self.nom+":"+text)
	
	## Sauvegarde les options.
	#
	# Sauvegarde les options dans le fichier de configuration, ne pas utiliser.
	# Les options sont sauvegardées automatiquement.
	# @param self le plugin courant
	# @return Rien
	# @deprecated Ne fait plus rien. Ne pas uiliser.
	def sauvegarderPreference(self):
		logger.warn("Plugin.sauvegarderPreference(): DEPRECATED: ne fait plus rien.")
		return
		try:
			file = open(self.fichierConfiguration, "w")
			pickle.dump(self.pluginOptions, file)
			file.close()
		except:
			print "Plugin.sauvegarderPreference(): Erreur de sauvegarde"
	
	## Charge les préférences.
	#
	# Charge les préférences du fichier de configuration, ne pas utiliser.
	# Les options sont chargées automatiquement.
	# @param self le plugin courant
	# @return Rien
	# @deprecated Ne fait plus rien. Ne pas uiliser.
	def chargerPreference(self):
		logger.warn("Plugin.chargerPreference(): DEPRECATED: ne fait plus rien.")
		return
		if os.path.exists(self.fichierConfiguration):
			try:
				file = open(self.fichierConfiguration, "r")
				tmp = pickle.load(file)
				file.close()
				self.pluginOptions = tmp
			except:
				print "Plugin.chargerPreference(): Erreur de chargement"
	
	## Sauvegarde un objet dans le cache.
	#
	# Attention, cette méthode écrase le cache déjà enregistré.
	# @param self le plugin courant
	# @param objet l'objet à sauvegarder
	# @return Rien
	def sauvegarderCache(self, objet):
		try:
			file = open(self.fichierCache, "w")
			pickle.dump(objet, file)
			file.close()
		except:
			logger.error("Plugin.sauvegarderCache(): Erreur de sauvegarde")
	
	## Charge le fichier de cache.
	# @param self le plugin courant
	# @return l'objet sauvegardé dans le cache ou None en cas d'échec
	def chargerCache(self):
		if os.path.exists(self.fichierCache):
			try:
				file = open(self.fichierCache, "r")
				tmp = pickle.load(file)
				file.close()
				return tmp
			except:
				logger.error("Plugin.chargerCache(): Erreur de chargement")
				return None
		else:
			return None
	
	## Renvoie la valeur d'une option
	#
	# L'option doit être ajouter dans #listerOptions pour que cela renvoie une valeur.
	# @param self le plugin courant
	# @param nom le nom de l'option
	# @return la valeur de l'option, None en cas d'échec
	def getOption(self, nom):
		for option in self.pluginOptions:
			if option.getNom() == nom:
				return option.getValeur()
		return None
	
	## Ajoute une option texte.
	# @param self le plugin courant
	# @param nom le nom de l'option (sert d'identifiant)
	# @param description la description de l'option
	# @param defaut la valeur par défaut (celle qui sera présente lors de l'affichage des options)
	# @return rien
	def optionTexte(self, nom, description, defaut):
		self.pluginOptions.append(Option(Option.TYPE_TEXTE, nom, description, defaut))
	
	## Ajoute une option bouléen.
	# @param self le plugin courant
	# @param nom le nom de l'option (sert d'identifiant)
	# @param description la description de l'option
	# @param defaut la valeur par défaut, True pour coché, faut pour décoché
	# @return rien
	def optionBouleen(self, nom, description, defaut):
		self.pluginOptions.append(Option(Option.TYPE_BOULEEN, nom, description, defaut))
	
	## Ajoute une option liste (choix multiple).
	# @param self le plugin courant
	# @param nom le nom de l'option (sert d'identifiant)
	# @param description la description de l'option
	# @param valeurs les valeurs possibles (liste)
	# @param defauts les valeurs sélectionnées (liste)
	# @return rien
	def optionChoixMultiple(self, nom, description, defauts, valeurs):
		self.pluginOptions.append(Option(Option.TYPE_CHOIX_MULTIPLE, nom, description, defauts, valeurs))
	
	## Ajoute une option liste (choix unique).
	# @param self le plugin courant
	# @param nom le nom de l'option (sert d'identifiant)
	# @param description la description de l'option
	# @param valeurs les valeurs possibles (liste)
	# @param defaut la valeur par défaut
	# @return rien
	def optionChoixUnique(self, nom, description, defaut, valeurs):
		self.pluginOptions.append(Option(Option.TYPE_CHOIX_UNIQUE, nom, description, defaut, valeurs))
	
	## Récupère une page web sur internet et remplace les caractères spéciaux (code HTML ou ISO).
	# @param self le plugin courant
	# @param url l'url de la page web
	# @return la page web sous forme d'une chaîne ou la chaîne vide en cas d'échec
	def getPage(self, url):
		return Plugin.NAVIGATEUR.getPage( url )
	
	## Récupère des pages webs sur internet et remplace les caractères spéciaux (code HTML ou ISO).
	# Cette méthode reste connecté au serveur si il y a plusieurs page à y télécharger,
	# elle est plus rapide que plusieurs appel à getPage.
	# @param self le plugin courant
	# @param urls une liste d'url des pages à télécharger
	# @return un dictionnaire avec comme clé les urls et comme valeur les pages sous forme de chaîne
	def getPages(self, urls):
		#FIXME Navigateur (téléchargement full threadé) vraiment efficace ?
		reponses = Plugin.NAVIGATEUR.getPages( urls )
		return reponses

