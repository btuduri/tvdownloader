#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import sys
import threading
import runpy
import os.path
from multiprocessing.managers import BaseManager
import tvdcore
from lockfile import FileLock
import logging

UI_ARG = "--ui"
UI_RUN__NAME__ = "__tvdui__"
LAUNCHER_ADDRESS = ('', 5096)
LAUNCHER_AUTHKEY = "tvdkey"
LOCK_FILE_PATH = tvdcore.REPERTOIRE_CONFIGURATION+"/LOCK"
UNLOCK_ARG = "--unlock"


# Mise en place du logger de TVDownloader
logger  = logging.getLogger( "TVDownloader" )
console = logging.StreamHandler( sys.stdout )

flock = FileLock(tvdcore.REPERTOIRE_CONFIGURATION)

if UNLOCK_ARG in sys.argv:
	flock.break_lock()
	sys.exit(0)

def isLaunched():
	return flock.is_locked()

def lockLaunch():
	try:
		flock.acquire(20)
	except Exception as e:
		return False
	return True

def unlockLaunch():
	try:
		flock.release()
	except Exception as e:
		return

class UICallback():
	def __init__(self):
		pass
	
	def onEnd(self, uiname):
		pass

class UIRunner(threading.Thread):
	def __init__(self, callback, name, path):
		threading.Thread.__init__(self)
		self.callback = callback
		self.name = name
		self.path = path
	
	def run(self):
		if os.path.isfile(path):
			runpy.run_path(self.path, init_globals=None, run_name=UI_RUN__NAME__)
			logger.info("UI "+self.name+" fermée")
		else:
			logger.error("L'ui "+self.path+" est introuvable")
		self.callback.onEnd(self.name)

class UILauncher(threading.Thread, UICallback):
	def __init__(self):
		threading.Thread.__init__(self)
		UICallback.__init__(self)
		
		self.threads = {}
	
	def lauchUI(self, name, path):
		if name in self.threads:
			logger.warning("L'ui "+name+" est déjà lancée")
		else:
			self.threads[name] = UIRunner(self, name, path)
			self.threads[name].start()
	
	def hasActiveUI(self):
		return len(self.threads) > 0
	
	def onEnd(self, uiname):
		self.threads.pop(uiname)
	

if __name__ == "__main__" :
	uiname = "qt"
	for arg in sys.argv:
		if arg.find(UI_ARG) == 0:
			uiname = arg[len(UI_ARG)+1:]
			break
	path = "./uis/"+uiname+"/main.py"
	if not(os.path.isfile(path)):
		logger.error("L'ui "+uiname+" est introuvable")
		sys.exit(1)

	# if( options.verbose ):#TODO
	if( True ):
		logger.setLevel( logging.DEBUG )
		console.setLevel( logging.DEBUG )
	else:
		logger.setLevel( logging.INFO )
		console.setLevel( logging.INFO )
	console.setFormatter( tvdcore.ColorFormatter( True ) )
	logger.addHandler( console )
	
	if isLaunched():
		#TODO Appel au laucher d'ui dans le processus lancé
		BaseManager.register('getUILauncher')
		manager = BaseManager(LAUNCHER_ADDRESS, LAUNCHER_AUTHKEY)
		manager.connect()

		launcher = manager.getUILauncher()
		launcher.lauchUI(uiname, path)
	else:
		#lockLaunch()
		context = tvdcore.TVDContext()
		if not(context.isInitialized()) and not(context.initialize()):
			logger.error("Impossible d'initialiser le context")
			sys.exit(1)
		
		#Mise à disposition du laucher
		launcher = UILauncher()
		launcher.lauchUI(uiname, path)
		
		BaseManager.register('getUILauncher', callable=lambda:launcher)
		manager = BaseManager(LAUNCHER_ADDRESS, LAUNCHER_AUTHKEY)
		
		manager.start()
		
		pluginMan = context.pluginManager
		pluginMan.pluginRafraichirAuto()
		
		import time
		while launcher.hasActiveUI():
			time.sleep(0.1)
		manager.shutdown()
		pluginMan.fermeture()
		context.historique.sauverHistorique()
		context.release()
		#unlockLaunch()

