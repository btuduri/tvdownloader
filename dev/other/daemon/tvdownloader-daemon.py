#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import core,sys

if core.initialiser() != core.STATUS_INITIALIZED:
	print "Erreur d'initialisation du module core"
	sys.exit(1)
else:
	print core.STATUS

import multiprocessing
from multiprocessing.managers import BaseManager

BaseManager.register('pluginManager', callable=lambda:core.PLUGIN_MANAGER)
BaseManager.register('downloadManager', callable=lambda:core.DOWNLOAD_MANAGER)
BaseManager.register('historique', callable=lambda:core.HISTORIQUE)

manager = BaseManager(core.SHARED_OBJECT_ADDRESS, core.SHARED_OBJECT_AUTHKEY)

server = manager.get_server()
print "Démon lancé..."
server.serve_forever()
