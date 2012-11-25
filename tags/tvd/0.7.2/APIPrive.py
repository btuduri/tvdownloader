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
import httplib,re,zlib, os.path, time, pickle
from random import choice
from traceback import print_exc

import logging
logger = logging.getLogger( __name__ )

from htmlentitydefs import codepoint2name
SPECCAR_CODE = {}
type = []
for code in codepoint2name:
	SPECCAR_CODE[codepoint2name[code]] = unicode(unichr(code)).encode("UTF-8", "replace")


from Fichier import Fichier
from Option import Option

##########
# Classe #
##########


class APIPrive():
	
	## Contructeur
	# @param self l'objet courant
	def __init__(self):
		self.listePluginActif = {}
		self.listePlugin = {}
	
	## Active un plugin (il faut qu'il ait déjà été ajouté).
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return Rien
	def activerPlugin(self, nomPlugin):
		if self.listePlugin.has_key(nomPlugin):
			self.listePluginActif[nomPlugin] = self.listePlugin[nomPlugin]
	
	## Désactive un plugin (il faut qu'il ait déjà été ajouté).
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return Rien
	def desactiverPlugin(self, nomPlugin):
		if self.listePluginActif.has_key(nomPlugin):
			self.listePluginActif.pop(nomPlugin)
	
	## Ajoute un plugin.
	# @param self l'objet courant
	# @param instance l'instance du plugin
	# @return Rien
	def ajouterPlugin(self, instance):
		if not self.listePlugin.has_key(instance.nom):
			self.listePluginActif[instance.nom] = instance
			self.listePlugin[instance.nom] = instance
	
	## Spécifie la liste des instances des plugins.
	# @param self l'objet courant
	# @param liste la liste des instances
	# @return Rien
	# @deprecated Utiliser #ajouterPlugin à la place.
	def setListeInstance(self, liste):
		logger.warn("DEPRECATED: APIPrive.setListeInstance: utilisez #ajouterPlugin")
		self.listePluginActif = {}
		for instance in liste:
			self.ajouterPlugin(instance)
	
	#/*******************
	# *	CONSTANTES *
	# *******************/
	DATA_CHAINE = "chaines"
	DATA_EMISSION = "emissions"
	DATA_FICHIER = "fichiers"
	
	#/**************
	# *	GETTERS *
	# **************/
	
	## Renvoie la liste des plugins (leur nom)
	# @param self l'objet courant
	# @return la liste des noms des plugins
	def getPluginListe(self):
		return self.listePluginActif.keys()
	
	## Renvoie la liste des chaînes.
	#
	# Si nomPlugin est égal à None, la liste des chaînes de tout les plugins est renvoyée, sinon c'est celle du plugin portant le nom passé en paramètre.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return la liste des chaînes du plugin
	def getPluginListeChaines(self, nomPlugin=None):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return []
			
		liste = []
		if nomPlugin == None:
			for nom in self.listePluginActif.keys():
				plugin = self.listePluginActif[nom]
				if len(plugin.pluginDatas[APIPrive.DATA_CHAINE]) == 0:
					plugin.listerChaines()
				liste+=plugin.pluginDatas[APIPrive.DATA_CHAINE]
		else:
			plugin = self.listePluginActif[nomPlugin]
			if len(plugin.pluginDatas[APIPrive.DATA_CHAINE]) == 0:
				plugin.listerChaines()
			liste+=plugin.pluginDatas[APIPrive.DATA_CHAINE]
		return liste

	## Renvoie la liste des émissions pour un plugin et une chaîne donné.
	#
	# Si nomPlugin est égal à None, la liste des émissions de tout les plugins est renvoyée, sinon c'est celle du plugin portant le nom passé en paramètre. Si chaine est égal à None, la liste des émissions de toute les chaines du plugin est renvoyée.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param chaine le nom de la chaîne
	# @return la liste des émissions
	def getPluginListeEmissions(self, nomPlugin=None, chaine=None):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return []
		
		liste= []
		if nomPlugin == None:
			for nom in self.listePluginActif.keys():
				plugin = self.listePluginActif[nom]
				for chaine in self.getPluginListeChaines(nom):
					if not plugin.pluginDatas[APIPrive.DATA_EMISSION].has_key(chaine):
						plugin.pluginDatas[APIPrive.DATA_EMISSION][chaine] = []
						plugin.listerEmissions(chaine)
					liste+=plugin.pluginDatas[APIPrive.DATA_EMISSION][chaine]
		elif chaine == None:
			plugin = self.listePluginActif[nomPlugin]
			for chaine in self.getPluginListeChaines(nomPlugin):
				if not plugin.pluginDatas[APIPrive.DATA_EMISSION].has_key(chaine):
					plugin.pluginDatas[APIPrive.DATA_EMISSION][chaine] = []
					plugin.listerEmissions(chaine)
				liste+=plugin.pluginDatas[APIPrive.DATA_EMISSION][chaine]
		else:
			plugin = self.listePluginActif[nomPlugin]
			if not plugin.pluginDatas[APIPrive.DATA_EMISSION].has_key(chaine):
				plugin.pluginDatas[APIPrive.DATA_EMISSION][chaine] = []
				plugin.listerEmissions(chaine)
			liste+=plugin.pluginDatas[APIPrive.DATA_EMISSION][chaine]
		return liste

	## Renvoie la liste des fichiers pour un plugin et une émission donné
	#
	# Si nomPlugin est égal à None, la liste des fichiers de tout les plugins est renvoyée, sinon c'est celle du plugin portant le nom passé en paramètre. Si emission est égal à None, la liste des fichiers de toute les émissions du plugin est renvoyée.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param emission le nom de l'émission
	# @return la liste des fichiers
	def getPluginListeFichiers(self, nomPlugin=None, emission=None):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return []
		
		liste= []
		if nomPlugin == None:
			for nom in self.listePluginActif.keys():
				plugin = self.listePluginActif[nom]
				for emission in self.getPluginListeEmissions(nom):
					if not plugin.pluginDatas[APIPrive.DATA_FICHIER].has_key(emission):
						plugin.pluginDatas[APIPrive.DATA_FICHIER][emission] = []
						plugin.listerFichiers(emission)
					liste+=plugin.pluginDatas[APIPrive.DATA_FICHIER][emission]
		elif emission == None:
			plugin = self.listePluginActif[nomPlugin]
			for emission in self.getPluginListeEmissions(nomPlugin):
				if not plugin.pluginDatas[APIPrive.DATA_FICHIER].has_key(emission):
					plugin.pluginDatas[APIPrive.DATA_FICHIER][emission] = []
					plugin.listerFichiers(emission)
				liste+=plugin.pluginDatas[APIPrive.DATA_FICHIER][emission]
		else:
			plugin = self.listePluginActif[nomPlugin]
			if not plugin.pluginDatas[APIPrive.DATA_FICHIER].has_key(emission):
				plugin.pluginDatas[APIPrive.DATA_FICHIER][emission] = []
				plugin.listerFichiers(emission)
			liste+=plugin.pluginDatas[APIPrive.DATA_FICHIER][emission]
		return liste
			

	## Renvoie la liste des options pour un plugin donné
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return la liste des options
	def getPluginListeOptions(self, nomPlugin):
		if not self.listePluginActif.has_key(nomPlugin):
			return []
		
		return self.listePluginActif[nomPlugin].pluginOptions

	## Renvoie l'option d'un plugin
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param nomOption le nom de l'option
	# @return la valeur de l'option, None en cas d'échec
	def getPluginOption(self, nomPlugin, nomOption):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return None
		plugin = self.listePluginActif[nomPlugin]
		
		for option in plugin.pluginOptions:
			if option.getNom() == nomOption:
				return option
		return None

	#/**************
	# *	SETTERS *
	# **************/
		
	## Change la valeur d'une option d'un plugin.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param valeur la valeur de l'option
	# @return Rien
	def setPluginOption(self, nomPlugin, nomOption, valeur):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return None
		plugin = self.listePluginActif[nomPlugin]
		
		plugin.pluginDatas = {"chaines":[],
			"emissions":{},
			"fichiers":{}}
		for option in plugin.pluginOptions:
			if option.getNom() == nomOption:
				option.setValeur(valeur)

	
	#/************
	# *	DIVERS *
	# ************/
	## Rafraichie un plugin (appel à Plugin.rafraichir)
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return Rien
	def pluginRafraichir(self, nomPlugin):
		try:
			if self.listePluginActif.has_key(nomPlugin):
				self.listePluginActif[nomPlugin].vider()
				self.listePluginActif[nomPlugin].rafraichir()
		except Exception, ex:
			logger.error("Erreur lors du rafraichissement du plugin",self.listePlugin[nomPlugin].nom+":"+str(ex))
			print_exc()
	
	## Rafraichie tous les plugins qui ont besoin de l'être.
	#
	# Doit être appelé obligatoirement après l'ajout des plugins.
	# @param self l'objet courant
	# @return Rien
	def pluginRafraichirAuto(self):
		t = time.time()
		for instance in self.listePlugin.values():
			if instance.frequence >= 0:
				if os.path.isfile(instance.fichierCache):
					delta = t-os.path.getmtime(instance.fichierCache)
					if delta > instance.frequence*86400:
						self.pluginRafraichir(instance.nom)
				else:
					self.pluginRafraichir(instance.nom)
			#~ instance.chargerPreference()
			#~ if len(instance.pluginOptions) == 0:
				#~ instance.listerOptions()
			instance.listerOptions()
			if os.path.exists(instance.fichierConfiguration):
				try:
					file = open(instance.fichierConfiguration, "r")
					tmp = pickle.load(file)
					file.close()
					for k in tmp.keys():
						self.setPluginOption(instance.nom, k, tmp[k])
				except:
					logger.error( u"impossible de charger les préférences de %s" %( instance.nom ) )
	
	## Effectue les tâches de sauvegarde avant la fermeture.
	#
	# Doit être absolument appelé avant la fermeture.
	# @param self l'objet courant
	def fermeture(self):
		for instance in self.listePluginActif.values():
			if len(instance.pluginOptions) > 0:
				try:
					pref = {}
					for o in instance.pluginOptions:
						pref[o.getNom()] = o.getValeur()
					file = open(instance.fichierConfiguration, "w")
					pickle.dump(pref, file)
					file.close()
				except:
					logger.error("Erreur de sauvegarde des préférences de"+instance.nom)
	
	#/*************
	# *	AUTRES *
	# *************/
	USER_AGENT = [ 'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
		'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
		'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; fr; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2',
		'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2) Gecko/20100115 Firefox/3.6',
		'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
		'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) midori',
		'Opera/8.50 (Windows NT 5.1; U; en)',
		'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.2.15 Version/10.00',
		'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312' ]
	PATTERN_CHARSET = re.compile("charset=(.*?)$", re.IGNORECASE)
	PATTERN_SPECCAR= re.compile("&(.+?);")
	PATTERN_URL = re.compile("http://(.+?)(/.*)|(.+?)(/.*)")
	TAILLE_BLOCK = 1000#essayé avec 8k mais plante :/
	HTTP_TIMEOUT = 5
	def reponseHttpToUTF8(self, reponse):
		"""Renvoie le corp d'une réponse HTTP en UTF8, décompressé et débarassé des caractères spéciaux html.
		Renvoie la chaîne vide en cas d'échec."""
		data = ""
		if reponse.getheader('Content-Encoding', '').find('gzip') >= 0:
			try:
				decomp = zlib.decompressobj(16+zlib.MAX_WBITS)#chiffre "magic" apparemment
				while True:
					buff = reponse.read(APIPrive.TAILLE_BLOCK)
					if not(buff):
						break
					data = data+decomp.decompress(buff)
			except:
				logger.warn("APIPrive.reponseHttpToUTF8(): erreur de décompression")
				return ""
		else:
			data = reponse.read()
		
		#Vérification de l'encodage et conversion si néscessaire
		encoding = reponse.getheader("Content-Type", "")
		if encoding != "":
			try:
				match = re.search(APIPrive.PATTERN_CHARSET, encoding)
				if match != None and encoding != "utf-8":
					data = unicode(data, match.group(1), "replace").encode("utf-8", "replace")
				else:
					logger.info("APIPrive.reponseHttpToUTF8(): encodage inconnu.")
			except:
				logger.error("APIPrive.reponseHttpToUTF8(): erreur de décodage.")
		iters = []
		for match in re.finditer(APIPrive.PATTERN_SPECCAR, data):
			iters.insert(0, match)
		for match in iters:
			if match.group(1)[0] == "#":
				try:
					car = chr(int(match.group(1)[1:]))
					data = data[:match.start()] + car + data[match.end():]
				except:
					#Rien
					rien = None
			elif SPECCAR_CODE.has_key(match.group(1)):
				data = data[:match.start()] + SPECCAR_CODE[match.group(1)] + data[match.end():]
		return data
	
