#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from PyQt4 import QtGui, QtCore, Qt
import sys

class MainWindow(QtGui.QMainWindow):
	
	DEFAULT_WIDTH = 700
	DEFAULT_HEIGHT = 400
	
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
		scroll.setFixedWidth(100)
		scroll.setSizePolicy(expandingHeightPolicy)
		layout.addWidget(scroll)
		self.pluginArea = QtGui.QWidget()
		self.pluginArea.setLayout(QtGui.QVBoxLayout())
		scroll.setViewport(self.pluginArea)
		
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
		self.pluginArea.layout().addWidget(QtGui.QLabel( "file:///usr/share/icons/Faenza/apps/22/access.png"))
		self.pluginArea.layout().addWidget(PluginWidget(None, "file:///usr/share/icons/Faenza/apps/22/access.png"))
		self.pluginArea.layout().addWidget(QtGui.QLabel( "file:///usr/share/icons/Faenza/apps/22/access.png"))


from urlparse import urlparse

class PluginWidget(QtGui.QWidget):
	
	SIZE_POLICY = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
	
	def __init__(self, parent, iconUri):
		QtGui.QWidget.__init__(self, parent)
		self.setLayout(QtGui.QVBoxLayout())
		self.setSizePolicy(PluginWidget.SIZE_POLICY)
		
		component = urlparse(iconUri)
		
		if component.scheme == 'file':
			pixmap = QtGui.QPixmap(component.path)
			self.qImage = QtGui.QLabel(self)
			self.qImage.setPixmap(pixmap)
			print component.path
		#else: TODO
		
		self.qImage.setSizePolicy(PluginWidget.SIZE_POLICY)


app = QtGui.QApplication( sys.argv )
window = MainWindow()
window.show()
sys.exit(app.exec_())


