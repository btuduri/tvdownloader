#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from PyQt4 import QtGui, QtCore, Qt
import sys

from core import *
from urlparse import urlparse
import os.path

class MainWindow(QtGui.QMainWindow):
	
	DEFAULT_WIDTH = 700
	DEFAULT_HEIGHT = 400
	
	## @var pluginArea
	# Conteneur des boutons de sélection du plugin - QVBoxLayout
	
	## @var chaineArea
	# Liste des chaînes - QtGui.QListWidget
	
	## @var emissionArea
	# Liste des émissions - QtGui.QListWidget
	
	## @var fichierArea
	# Liste des fichiers - QtGui.QListWidget
	
	## @var pluginManager
	
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.resize(MainWindow.DEFAULT_WIDTH, MainWindow.DEFAULT_HEIGHT)
		
		expandingPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		expandingHeightPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		
		widget = QtGui.QWidget()
		widget.setSizePolicy(expandingPolicy)
		self.setCentralWidget(widget)
		layout = QtGui.QHBoxLayout(widget)
		
		scroll = QtGui.QScrollArea()
		scroll.setSizePolicy(QtGui.QSizePolicy(
			QtGui.QSizePolicy.MinimumExpanding,
			QtGui.QSizePolicy.Expanding
		))
		scroll.setWidgetResizable(True);
		layout.addWidget(scroll)
		
		self.pluginArea = QtGui.QWidget()
		self.pluginArea.setLayout(QtGui.QVBoxLayout())
		
		scroll.setWidget(self.pluginArea)
		
		#tmp = QtGui.QWidget()
		#tmp.setFixedWidth(100)
		#layout.addWidget(scroll)
		#self.pluginArea = QtGui.QVBoxLayout()
		#tmp.setLayout(self.pluginArea)
		#scroll.setWidget(tmp)
		
		rightArea = QtGui.QWidget()
		rightArea.setSizePolicy(expandingPolicy)
		rightAreaLayout = QtGui.QGridLayout(rightArea)
		layout.addWidget(rightArea)
		
		self.chaineArea = QtGui.QListWidget()
		self.chaineArea.setFixedHeight(80)
		rightAreaLayout.addWidget(self.chaineArea, 0, 0)
		
		self.emissionArea = QtGui.QListWidget()
		self.emissionArea.setFixedHeight(80)
		rightAreaLayout.addWidget(self.emissionArea, 0, 1)
		
		self.fichierArea = QtGui.QListWidget()
		rightAreaLayout.addWidget(self.fichierArea, 1, 0, 1, 2)
		
		###
		self.pluginManager = PluginManager()
		for name in self.pluginManager.getPluginListe():
			plugin = self.pluginManager.getInstance(name)
			self.pluginArea.layout().addWidget(AutoLoadImage(plugin.logo, None, 100))
	
	def selectPlugin(self, name):
		plugin = self.pluginManager.getInstance(name)
		if plugin != None:
			#On efface les anciens
			while self.chaineArea.count() > 0:
				self.chaineArea.removeItemWidget(self.chaineArea.item(0))
			while self.emissionArea.count() > 0:
				self.emissionArea.removeItemWidget(self.emissionArea.item(0))
			while self.fichierArea.count() > 0:
				self.fichierArea.removeItemWidget(self.fichierArea.item(0))
			
			#Ajout des chaînes
			for chaine in self.pluginManager.getPluginListeChaines(name):
				self.chaineArea.addItem(chaine)
		else:
			print "Le plugin "+name+"n'existe pas"
	
	def changeChaine(self):
		pass
		

class AutoLoadImage(QtGui.QLabel):
	
	def __init__(self, imageUri, parent=None, maxWidth=100, maxHeight=100):
		QtGui.QLabel.__init__(self, parent)
		
		component = urlparse(imageUri)
		
		if os.path.isfile(component.path):
			pixmap = QtGui.QPixmap(component.path)
			if pixmap.width()/pixmap.height() > maxWidth/maxHeight or True:
				pixmap = pixmap.scaledToWidth(maxWidth)
			else:
				pixmap = pixmap.scaledToHeight(maxHeight)
			self.resize(pixmap.width(), pixmap.height())
			self.setPixmap(pixmap)
		#else: TODO Lancer le chargement asynchrone


app = QtGui.QApplication( sys.argv )
window = MainWindow()
window.show()
window.selectPlugin("Canal+")
#sys.exit(app.exec_())
print app.exec_()

