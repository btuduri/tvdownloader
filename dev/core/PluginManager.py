#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import httplib,re,zlib, os.path, time, pickle, traceback
from random import choice
from traceback import print_exc
import os
import sys

from Plugin import Plugin

import Constantes

import logging
logger = logging.getLogger( "TVDownloader" )

from util import Synchronized
import threading
from TVDContext import TVDContext

##########
# Classe #
##########
#TODO Fusion imcomplette, utiliser les setters dans le constructeur, gérer la liste
# des plugins présents, actifs et inactifs.
#TODO Avoir des timeouts sur les appels des méthodes des plugins
## Classe qui gere les plugins
class PluginManager( object ):
	
	# Instance de la classe (singleton)
	__instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__(typ, *args, **kwargs):
		# On vérifie qu'on peut instancier
		context = TVDContext()
		if not(context.isInitialized()):
			logger.error("Le context n'est pas initialisé, impossible d'instancier")
			return None
		
		if PluginManager.__instance == None:
			return super(PluginManager, typ).__new__(typ, *args, **kwargs)
		else:
			return PluginManager.__instance
	
	## Constructeur
	def __init__( self ):
		if PluginManager.__instance != None:
			return
		PluginManager.__instance = self
		
		#Code venant de APIPrive
		self.listePluginActif = {}
		self.listePlugin = {}
		
		# Import de tous les plugins
		for rep in Constantes.REPERTOIRES_PLUGINS:
			# Ajout du repertoire au path si necessaire
			if not( rep in sys.path ):
				sys.path.insert( 0, rep )
			# Verifie que le repertoire des plugins existe bien
			if( not os.path.isdir( rep ) ):
				logger.warn( "le repertoire %s des plugins n'existe pas..." %( rep ) )
			else:
				# Importe les plugins
				self.importerPlugins( rep )
		# Instancie les plugins
		self.instancierPlugins()
		
		self.callbacks = []
		
	## Methode qui importe les plugins
	# @param rep Repertoire dans lequel se trouvent les plugins a importer
	@Synchronized
	def importerPlugins( self, rep ):
		for fichier in os.listdir( rep ): 
			# Tous les fichiers py autre que __init__.py sont des plugins a ajouter au programme
			if( fichier [ -3 : ] == ".py" and fichier.find( "__init__.py" ) == -1 ):
				# On suppose que c'est la derniere version du plugin
				derniereVersion = True
				# Pour les autres repertoires de plugins
				for autreRep in ( set( Constantes.REPERTOIRES_PLUGINS ).difference( set( [ rep ] ) ) ):
					# Si le fichier existe dans l'autre repertoire
					if( fichier in os.listdir( autreRep ) ):
						# Si la version du plugin de l'autre repertoire est plus recente
						if( os.stat( "%s/%s" %( autreRep, fichier ) ).st_mtime > os.stat( "%s/%s" %( rep, fichier ) ).st_mtime ):
							derniereVersion = False
							break # On arrete le parcourt des repertoires
				# Si ce n'est pas la derniere version
				if( not derniereVersion ):
					continue # Fichier suivant
				try :
					__import__( fichier.replace( ".py", "" ), None, None, [ '' ] )
				except ImportError as exc:
					logger.error( "impossible d'importer le fichier %s: %s" %( fichier, exc.message ) )
					traceback.print_exc()
					continue

	## Methode qui instancie les plugins
	# N.B. : doit etre lancee apres importerPlugins
	@Synchronized
	def instancierPlugins( self ):
		for plugin in Plugin.__subclasses__(): # Pour tous les plugins
			try:
				# Instance du plugin
				inst = plugin()
			except Exception as exc:
				logger.error( "impossible d'instancier le plugin %s: %s" %( plugin,  exc.message) )
				traceback.print_exc()
				continue
			# Nom du plugin
#			nom = inst.nom#FIXME Utiliser le nom de la classe
			# Ajout du plugin
#			self.listeInstances[ nom ] = inst
			self.ajouterPlugin(inst)
	
	## Methode qui retourne la liste des sites/plugins
	# N.B. : doit etre lancee apres listerPlugins
	# @return La liste des noms des plugins
#	def getListeSites( self ):
#		return self.listeInstances.keys()
	
	## Methode qui retourne l'instance d'un plugin
	# @param nom Nom du plugin dont il faut recuperer l'instance
	# @return    Instance du plugin ou None s'il n'existe pas
	@Synchronized
	def getInstance( self, nom ):
		return self.listePlugin.get( nom, None )

	@Synchronized
	def addCallback( self, callback ):
		self.callbacks.append(callback)
	
	@Synchronized
	def removeCallback( self, callback ):
		self.callbacks.remove(callback)
	
	###################################################
	############# Code venant de APIPrive #############
	###################################################
	
	## Active un plugin (il faut qu'il ait déjà été ajouté).
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return Rien
	@Synchronized
	def activerPlugin(self, nomPlugin):
		if self.listePlugin.has_key(nomPlugin):
			self.listePluginActif[nomPlugin] = self.listePlugin[nomPlugin]
			for cback in self.callbacks:
				cback.pluginStatus(nomPlugin, PluginStatus(PluginStatus.ENABLED))
	
	## Désactive un plugin (il faut qu'il ait déjà été ajouté).
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return Rien
	@Synchronized
	def desactiverPlugin(self, nomPlugin):
		if self.listePluginActif.has_key(nomPlugin):
			self.listePluginActif.pop(nomPlugin)
			for cback in self.callbacks:
				cback.pluginStatus(nomPlugin, PluginStatus(PluginStatus.DISABLED))
	
	## Ajoute un plugin.
	# @param self l'objet courant
	# @param instance l'instance du plugin
	# @return Rien
	@Synchronized
	def ajouterPlugin(self, instance):
		if not self.listePlugin.has_key(instance.nom):#FIXME Utiliser le nom de la classe
			self.listePluginActif[instance.nom] = instance
			self.listePlugin[instance.nom] = instance#FIXME Utiliser le nom de la classe
			instance.chargerCache()
	
	## Spécifie la liste des instances des plugins.
	# @param self l'objet courant
	# @param liste la liste des instances
	# @return Rien
	# @deprecated Utiliser #ajouterPlugin à la place.
	@Synchronized
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
	@Synchronized
	def getPluginListe(self):
		return self.listePlugin.keys()
	
	## Renvoie la liste des plugins (leur instance)
	# @return Liste des instances des plugins
	@Synchronized
	def getPluginListeInstances( self ):
		return self.listePlugin.values()
	
	## Renvoie la liste des plugins actifs (leur nom)
	# @param self l'objet courant
	# @return la liste des noms des plugins actifs
	@Synchronized
	def getPluginActifListe(self):
		return self.listePluginActif.keys()
	
	## Renvoie la liste des plugins inactifs (leur nom)
	# @param self l'objet courant
	# @return la liste des noms des plugins inactifs
	@Synchronized
	def getPluginInactifListe(self):
		res = []
		actifs = self.listePluginActif.keys()
		for plugin in self.listePlugin.keys():
			if not(plugin in actifs):
				res.append(plugin)
		return res
	
	## Renvoie la liste des chaînes.
	#
	# Si nomPlugin est égal à None, la liste des chaînes de tout les plugins est renvoyée, sinon c'est celle du plugin portant le nom passé en paramètre.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return la liste des chaînes du plugin
	@Synchronized
	def getPluginListeChaines(self, nomPlugin=None):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return []
			
		liste = []
		if nomPlugin == None:
			for nom in self.listePluginActif.keys():
				plugin = self.listePluginActif[nom]
				if len(plugin.pluginDatas[self.DATA_CHAINE]) == 0:
					plugin.listerChaines()
				liste+=plugin.pluginDatas[self.DATA_CHAINE]
		else:
			plugin = self.listePluginActif[nomPlugin]
			if len(plugin.pluginDatas[self.DATA_CHAINE]) == 0:
				plugin.listerChaines()
			liste+=plugin.pluginDatas[self.DATA_CHAINE]
		return liste

	## Renvoie la liste des émissions pour un plugin et une chaîne donné.
	#
	# Si nomPlugin est égal à None, la liste des émissions de tout les plugins est renvoyée, sinon c'est celle du plugin portant le nom passé en paramètre. Si chaine est égal à None, la liste des émissions de toute les chaines du plugin est renvoyée.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param chaine le nom de la chaîne
	# @return la liste des émissions
	@Synchronized
	def getPluginListeEmissions(self, nomPlugin=None, chaine=None):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return []
		
		liste= []
		if nomPlugin == None:
			for nom in self.listePluginActif.keys():
				plugin = self.listePluginActif[nom]
				for chaine in self.getPluginListeChaines(nom):
					if not plugin.pluginDatas[self.DATA_EMISSION].has_key(chaine):
						plugin.pluginDatas[self.DATA_EMISSION][chaine] = []
						plugin.listerEmissions(chaine)
					liste+=plugin.pluginDatas[self.DATA_EMISSION][chaine]
		elif chaine == None:
			plugin = self.listePluginActif[nomPlugin]
			for chaine in self.getPluginListeChaines(nomPlugin):
				if not plugin.pluginDatas[self.DATA_EMISSION].has_key(chaine):
					plugin.pluginDatas[self.DATA_EMISSION][chaine] = []
					plugin.listerEmissions(chaine)
				liste+=plugin.pluginDatas[self.DATA_EMISSION][chaine]
		else:
			plugin = self.listePluginActif[nomPlugin]
			if not plugin.pluginDatas[self.DATA_EMISSION].has_key(chaine):
				plugin.pluginDatas[self.DATA_EMISSION][chaine] = []
				plugin.listerEmissions(chaine)
			liste = plugin.pluginDatas[self.DATA_EMISSION][chaine]
		return liste

	## Renvoie la liste des fichiers pour un plugin et une émission donné
	#
	# Si nomPlugin est égal à None, la liste des fichiers de tout les plugins est renvoyée, sinon c'est celle du plugin portant le nom passé en paramètre. Si emission est égal à None, la liste des fichiers de toute les émissions du plugin est renvoyée.
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param emission le nom de l'émission
	# @return la liste des fichiers
	@Synchronized
	def getPluginListeFichiers(self, nomPlugin=None, emission=None):
		if nomPlugin != None and not self.listePluginActif.has_key(nomPlugin):
			return []
		
		liste= []
		if nomPlugin == None:
			for nom in self.listePluginActif.keys():
				plugin = self.listePluginActif[nom]
				for emission in self.getPluginListeEmissions(nom):
					if not plugin.pluginDatas[self.DATA_FICHIER].has_key(emission):
						plugin.pluginDatas[self.DATA_FICHIER][emission] = []
						plugin.listerFichiers(emission)
					liste+=plugin.pluginDatas[self.DATA_FICHIER][emission]
		elif emission == None:
			plugin = self.listePluginActif[nomPlugin]
			for emission in self.getPluginListeEmissions(nomPlugin):
				if not plugin.pluginDatas[self.DATA_FICHIER].has_key(emission):
					plugin.pluginDatas[self.DATA_FICHIER][emission] = []
					plugin.listerFichiers(emission)
				liste+=plugin.pluginDatas[self.DATA_FICHIER][emission]
		else:
			plugin = self.listePluginActif[nomPlugin]
			if not plugin.pluginDatas[self.DATA_FICHIER].has_key(emission):
				plugin.pluginDatas[self.DATA_FICHIER][emission] = []
				plugin.listerFichiers(emission)
			liste+=plugin.pluginDatas[self.DATA_FICHIER][emission]
		return liste
			

	## Renvoie la liste des options pour un plugin donné
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @return la liste des options
	@Synchronized
	def getPluginListeOptions(self, nomPlugin):
		if not self.listePluginActif.has_key(nomPlugin):
			return []
		
		return self.listePluginActif[nomPlugin].pluginOptions

	## Renvoie l'option d'un plugin
	# @param self l'objet courant
	# @param nomPlugin le nom du plugin
	# @param nomOption le nom de l'option
	# @return la valeur de l'option, None en cas d'échec
	@Synchronized
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
	@Synchronized
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
	@Synchronized
	def pluginRafraichir(self, nomPlugin):
		try:
			if self.listePluginActif.has_key(nomPlugin):
				for cback in self.callbacks:
					cback.pluginStatus(nomPlugin, PluginStatus(PluginStatus.REFRESHING))
				self.listePluginActif[nomPlugin].vider()
				self.listePluginActif[nomPlugin].rafraichir()
				for cback in self.callbacks:
					cback.pluginStatus(nomPlugin, PluginStatus(PluginStatus.REFRESHED))
		except Exception, ex:
			logger.error("Erreur lors du rafraichissement du plugin",self.listePlugin[nomPlugin].nom+":"+str(ex))
			print_exc()
		except Error, er:
			logger.error("Erreur lors du rafraichissement du plugin",self.listePlugin[nomPlugin].nom+":"+str(ex))
			print_exc()
	
	## Rafraichie tous les plugins qui ont besoin de l'être.
	#
	# Doit être appelé obligatoirement après l'ajout des plugins.
	# @param self l'objet courant
	# @return Rien
	@Synchronized
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
	@Synchronized
	def fermeture(self):
		for instance in self.listePlugin.values():
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

class PluginCallback :
	def __init__(self) :
		pass
		
	def pluginStatus(self, pluginName, status):
		pass

class PluginStatus :
	ENABLED = 0
	DISABLED = 1
	REFRESHING = 2
	REFRESHED = 3
	
	def __init__(self, status):
		self.status = status
	
	def getStatus(self):
		return self.status

