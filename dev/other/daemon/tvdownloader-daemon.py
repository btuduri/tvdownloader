#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import core,sys

if core.initialiser() != core.STATUS_INITIALIZED:
	print "Erreur d'initialisation du module core"
	sys.exit(1)
print "tvdd lancé"
#Lancé le démon (distribution des objets)
