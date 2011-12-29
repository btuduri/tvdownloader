#-*- encoding: UTF-8 -*-
import core


from core import *
from plugins import CanalPlus

class CBackTest(PluginCallback):
	
	def __init__(self):
		PluginCallback.__init__(self)
	
	def pluginStatus(self, pluginName, status):
		print pluginName+":", status.getStatus()

m = PluginManager()

m.addCallback(CBackTest())

print m.getPluginListe()
print m.getPluginActifListe()
print m.getPluginInactifListe()
print m.getPluginListeChaines("M6Replay")

m.activerPlugin("M6Replay")

print m.getPluginListeChaines("M6Replay")

m.desactiverPlugin("M6Replay")

