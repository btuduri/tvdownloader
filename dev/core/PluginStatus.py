# -*- coding:Utf-8 -*-

class PluginStatus :
	ENABLED = 0
	DISABLED = 1
	REFRESHING = 2
	REFRESHED = 3
	
	def __init__(self, status):
		self.status = status
	
	def getStatus(self):
		return self.status

