#!/bin/python


from cmd import Cmd
import sys

from core import *

class Cli(Cmd):
	EXEC_MAP = {"quit": [sys.exit, (0,)],
		"help": [sys.stdout.write, (help,)]}
	
	def __init__(self):
		Cmd.__init__(self)
		self.execs = [MainExec()]

	def onecmd(self, cmdText):
		if len(self.execs) == 0:
			sys.exit(0)
		else:
			args = cmdText.split(" ")
			res = self.execs[len(self.execs)-1].execCmd(args[0], args[1:])
			if isinstance(res, CmdExec):
				self.execs.append(res)
			elif not(res):
				self.execs.pop()

#		cmdKey = cmdText
#		res = Cli.EXEC_MAP[cmdText][0](*Cli.EXEC_MAP[cmdText][1])
#		if res:
#			if type(res) == list:
#				for e in res:
#					print "  ",e
#			else:
#				print res

class CmdExec(object):
	
	def __init__(self):
		object.__init__(self)
	
	def execCmd(self, cmd, args):
		if cmd == "retour":
			return False;
		if not(self.EXEC_MAP.has_key(cmd)):
			print "Commande inconnue"
			return True
		res = self.EXEC_MAP[cmd][0](*self.EXEC_MAP[cmd][1])
		if res:
			if type(res) == list:
				for e in res:
					print "  ",e
			else:
				print res
		return True

MAIN_HELP = """Liste des commandes:
 plugin (list|activer|desactiver)
 chaine (nomPlugin)
 emission (nomPlugin) (chaine)
 fichier (nomPlugin) (emission)
 downloads
 retour
"""
PLUGIN_MANAGER = PluginManager()
class MainExec(CmdExec):

	def __init__(self):
		CmdExec.__init__(self)
		self.EXEC_MAP = MainExec.EXEC_MAP;
	
	EXEC_MAP = {"quit": [sys.exit, (0,)],
		"help": [sys.stdout.write, (MAIN_HELP,)],
		"plugin": [PLUGIN_MANAGER.getPluginListe, ()]}
	
	def execCmd(self, cmd, args):
		if cmd == "downloads":
			return DownloadExec()
		else:
			return CmdExec.execCmd(self, cmd, args)
#		if cmd == "retour":
#			return False;
#		if not(MainExec.EXEC_MAP.has_key(cmd)):
#			print "Commande inconnue"
#			return True
#		res = MainExec.EXEC_MAP[cmd][0](*MainExec.EXEC_MAP[cmd][1])
#		if res:
#			if type(res) == list:
#				for e in res:
#					print "  ",e
#			else:
#				print res
#		return True


class DownloadExec(CmdExec):

	def __init__(self):
		CmdExec.__init__(self)


cli = Cli()
cli.cmdloop()



