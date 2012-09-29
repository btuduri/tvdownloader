#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import argparse
import lockfile
import logging
logger = None
from multiprocessing.managers import BaseManager
import os
import runpy
import sys
import threading

import tvdcore
import tvdcore.Constantes as Constantes

#
# Gestion des UIs
#

LAUNCHER_ADDRESS = ('', 5096)
LAUNCHER_AUTHKEY = "tvdkey"
UI_RUN__NAME__ = "__tvdui__"

flock = lockfile.FileLock( Constantes.REPERTOIRE_CONFIGURATION )

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
		if os.path.isfile(self.path):
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

#
# Main
#

if( __name__ == "__main__" ):
	
	# Arguments de la ligne de commande
	usage   = "tvdownloader [options]"
	parser  = argparse.ArgumentParser( usage = usage )
	parser.add_argument( "--ui", dest = "uiname", metavar = "UI_NAME", default = "qt", help = "nom de l'UI a utiliser (qt par defaut)" )
	parser.add_argument( "--unlock", action = "store_true", default = False, help = "je ne sais pas quoi mettre" )
	parser.add_argument( "-v", "--verbose", action = "store_true", default = False, help = "affiche les informations de debugage" )
	parser.add_argument( "--nocolor", action = 'store_true', default = False, help = "désactive la couleur dans le terminal" )
	parser.add_argument( "--version", action = 'version', version = "tvdownloader %s" %( Constantes.TVD_VERSION ) )
	args = parser.parse_args()
	
	# Mise en place du logger de TVDownloader
	logger  = logging.getLogger( "TVDownloader" )
	console = logging.StreamHandler( sys.stdout )
	if( args.verbose ):
		logger.setLevel( logging.DEBUG )
		console.setLevel( logging.DEBUG )
	else:
		logger.setLevel( logging.INFO )
		console.setLevel( logging.INFO )
	console.setFormatter( tvdcore.ColorFormatter( not args.nocolor ) )
	logger.addHandler( console )
	
	# Mise en place du logger des fichiers de base
	loggerBase  = logging.getLogger( "base" )
	consoleBase = logging.StreamHandler( sys.stdout )
	if( args.verbose ):
		loggerBase.setLevel( logging.DEBUG )
		consoleBase.setLevel( logging.DEBUG )
	else:
		loggerBase.setLevel( logging.INFO )
		consoleBase.setLevel( logging.INFO )
	consoleBase.setFormatter( tvdcore.ColorFormatter( not args.nocolor ) )
	loggerBase.addHandler( consoleBase )
	
	#
	if( args.unlock ):
		flock.break_lock()
		sys.exit( 0 )
	
	# Verification de la presence de l'UI
	pathUi = "./uis/%s/main.py" %( args.uiname )
	if( not os.path.isfile( pathUi ) ):
		logger.critical( "L'UI %s est introuvable" %( args.uiname ) )
		sys.exit( 1 )
	
	# 
	if isLaunched():
		#TODO Appel au laucher d'ui dans le processus lancé
		BaseManager.register('getUILauncher')
		manager = BaseManager(LAUNCHER_ADDRESS, LAUNCHER_AUTHKEY)
		manager.connect()

		launcher = manager.getUILauncher()
		launcher.lauchUI(args.uiname, pathUi)
	else:
		#lockLaunch()
		context = tvdcore.TVDContext()
		if not(context.isInitialized()) and not(context.initialize()):
			logger.error("Impossible d'initialiser le context")
			sys.exit(1)
		
		#Mise à disposition du laucher
		launcher = UILauncher()
		launcher.lauchUI(args.uiname, pathUi)
		
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
