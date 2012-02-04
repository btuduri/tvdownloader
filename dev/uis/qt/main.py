#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from PyQt4 import QtGui, QtCore, Qt
import sys

from tvdcore import *
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
		
		#self.fichierArea = QtGui.QListWidget()
		#rightAreaLayout.addWidget(self.fichierArea, 1, 0, 1, 2)
		self.fichierArea = QFileTableWidget()
		rightAreaLayout.addWidget(self.fichierArea, 1, 0, 1, 2)
		
		QtCore.QObject.connect(self.chaineArea,
			QtCore.SIGNAL( "currentItemChanged(QListWidgetItem*,QListWidgetItem*)" ),
			self.selectChannel
		)
		QtCore.QObject.connect(self.emissionArea,
			QtCore.SIGNAL( "currentItemChanged(QListWidgetItem*,QListWidgetItem*)" ),
			self.selectShow
		)
		
		###
		self.pluginManager = PluginManager()
		for name in self.pluginManager.getPluginListe():
			plugin = self.pluginManager.getInstance(name)
			self.pluginArea.layout().addWidget(AutoLoadImage(plugin.logo, None, 100))
		self.currentPlugin = None
		self.currentChannel = None
		self.currentShow = None
	
	def selectPlugin(self, name):
		plugin = self.pluginManager.getInstance(name)
		if plugin == None:
			print "Le plugin "+name+"n'existe pas"
			return
		if isinstance(name, QtGui.QListWidgetItem):
			self.currentPlugin = str(name.text())
		else:
			self.currentPlugin = name
		#On efface les anciens
		self.currentChannel = None
		while self.chaineArea.count() > 0:
			self.chaineArea.takeItem(0)
		self.currentShow = None
		while self.emissionArea.count() > 0:
			self.emissionArea.takeItem(0)
		while self.fichierArea.rowCount() > 0:
			self.fichierArea.removeRow(0)
		#Ajout des chaînes
		for chaine in self.pluginManager.getPluginListeChaines(name):
			self.chaineArea.addItem(chaine)
	
	def selectChannel(self, name):
		if isinstance(name, QtGui.QListWidgetItem):
			self.currentChannel = str(name.text())
		else:
			self.currentChannel = name
		#On efface les anciens
		self.currentShow = None
		while self.emissionArea.count() > 0:
			self.emissionArea.takeItem(0)
		while self.fichierArea.rowCount() > 0:
			self.fichierArea.removeRow(0)
		#Ajout des emissions
		for emission in self.pluginManager.getPluginListeEmissions(self.currentPlugin, self.currentChannel):
			self.emissionArea.addItem(emission)
	
	def selectShow(self, name):
		if isinstance(name, QtGui.QListWidgetItem):
			self.currentShow = str(name.text())
		else:
			self.currentShow = name
		#On efface les anciens
		while self.fichierArea.rowCount() > 0:
			self.fichierArea.removeRow(0)
		#Ajout des fichiers
		for fichier in self.pluginManager.getPluginListeFichiers(self.currentPlugin, self.currentShow):
			self.fichierArea.addFichier(fichier)

class QFileTableWidget( QtGui.QTableWidget ):
	def __init__(self, parent=None):
		QtGui.QTableWidget.__init__(self, parent)
		self.setColumnCount(2)
		self.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Date"))
		self.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Nom"))
		
		# On masque le numero des lignes
		self.verticalHeader().setVisible( False )
		# On masque le quadrillage
		self.setShowGrid( False )
		# Lorsque qu'on clique sur une ligne, on selectionne toute la ligne
		self.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
		# On ne peut selectionner qu'une ligne a la fois
		self.setSelectionMode( QtGui.QAbstractItemView.SingleSelection )
		# La derniere colonne visible prend toute la place restante
		self.horizontalHeader().setStretchLastSection( True )
		# On alterne les couleurs des lignes
		self.setAlternatingRowColors( True )
	
	def addFichier(self, fichier):
		newRow = self.rowCount()
		self.insertRow(newRow)
		print fichier
		print fichier.nom
		self.setItem(newRow, 0, QtGui.QTableWidgetItem(fichier.date.strftime("%Y-%m-%d")))
		self.setItem(newRow, 1, QtGui.QTableWidgetItem(fichier.nom))

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

logger = logging.getLogger( "TVDownloader" )

ctx = TVDContext()
if not(ctx.isInitialized()) and not(ctx.initialize()):
	logger.error("Impossible d'initialiser le context")
else:
	app = QtGui.QApplication( sys.argv )
	window = MainWindow()
	window.show()
	# window.selectPlugin("Canal+")
	# window.selectPlugin("W9Replay")
	# window.selectPlugin("M6Replay")
	window.selectPlugin("TF1")
	#sys.exit(app.exec_())
	print app.exec_()

