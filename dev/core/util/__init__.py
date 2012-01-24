#!/usr/bin/env python
# -*- coding:Utf-8 -*-

##############
# Décorateur #
##############

import logging
logger = logging.getLogger( "TVDownloader" )

## Décorateur qui permet d'assurer la synchronisation des méthodes, une
# thread à la fois travaille sur l'instance avec les méthodes marquées.
# L'instance doit posséder un attribut RLOCK affecté à une instance de
# threading.RLock. Ne peut décorer les méthodes __new__ ou __init__.
def SynchronizedMethod(meth):
	def local(self, *arg):
		if hasattr(self, "LOCK"):
			self.RLOCK.acquire()
			res = meth(self, *arg)
			self.RLOCK.release()
		else:
			logger.error("Pas d'attribut RLOCK sur "+str(self))
			res = meth(self, *arg)
		return res
	return local
