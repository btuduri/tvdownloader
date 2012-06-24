#!/usr/bin/env python
# -*- coding:Utf-8 -*-

##############
# Décorateur #
##############

import logging,threading
logger = logging.getLogger( "TVDownloader" )

## Décorateur qui permet d'assurer la synchronisation des méthodes, une
# thread à la fois travaille sur l'instance avec les méthodes marquées.
# L'instance doit posséder un attribut RLOCK affecté à une instance de
# threading.RLock. Ne peut décorer les méthodes __new__ ou __init__.
def SynchronizedMethod(meth):
	def local(self, *arg):
		if hasattr(self, "RLOCK"):
			self.RLOCK.acquire()
			res = meth(self, *arg)
			self.RLOCK.release()
		else:
			logger.error("Pas d'attribut RLOCK sur "+str(self))
			res = meth(self, *arg)
		return res
	return local

def Synchronized(meth):
	LOCAL_RLOCK = threading.RLock()
	def local(self, *arg):
		if not(hasattr(self, "RLOCK")):
			LOCAL_RLOCK.acquire()
			setattr(self, "RLOCK", threading.RLock())
			LOCAL_RLOCK.release()
		self.RLOCK.acquire()
		res = meth(self, *arg)
		self.RLOCK.release()
		return res
	return local

def SynchronizedWith(instance):
	def decorator(func):
		LOCAL_RLOCK = threading.RLock()
		def local(*arg):
			if not(hasattr(instance, "RLOCK")):
				LOCAL_RLOCK.acquire()
				setattr(instance, "RLOCK", threading.RLock())
				LOCAL_RLOCK.release()
			instance.RLOCK.acquire()
			res = func(*arg)
			instance.RLOCK.release()
			return res
		return local
	return decorator


## Classe permettant la gestion d'un groupe de callback en gérant ajout,
# suppression et appel aux membres de ce groupe.
class CallbackGroup(object):
	
	## Constructeur
	# @param methode le nom de la méthode à appeler sur
	# les callbacks
	def __init__(self, methode):
		self.callbacks = []
		self.methode = methode
		self.RLOCK = threading.RLock()
	
	## Ajoute un callback à ce groupe.
	# @param callback le callback
	def add(self, callback):
		self.callbacks.append(callback)
	
	## Enlève un callback à ce groupe.
	# @param callback le callback
	def remove(self, callback):
		self.callbacks.remove(callback)
	
	## Appel les callbacks.
	# @param args arguments à passer au callback
	# @param kwargs arguments (keyword args) à passer au callback
	def __call__(self, *args, **kwargs):
		for cback in self.callbacks:
			getattr(cback, self.methode)(*args, **kwargs)
