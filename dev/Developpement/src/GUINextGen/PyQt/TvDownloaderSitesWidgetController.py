from PyQt4 import QtGui, QtCore

from TvDownloaderSitesWidgetView import Ui_TvDownloaderSitesWidget

class TvDownloaderSitesWidgetController(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        
        self.mainWindow = parent
        
        self.ui = Ui_TvDownloaderSitesWidget()
        self.ui.setupUi(self)
        
        # Connect the events
        self.connect(self.ui.pushButton_Arte, QtCore.SIGNAL('clicked()'), self.arteClicked)
        self.connect(self.ui.pushButton_Canal, QtCore.SIGNAL('clicked()'), self.canalClicked)
        self.connect(self.ui.pushButton_M6Replay, QtCore.SIGNAL('clicked()'), self.m6Clicked)
        self.connect(self.ui.pushButton_Pluzz, QtCore.SIGNAL('clicked()'), self.pluzzClicked)
        self.connect(self.ui.pushButton_W9Replay, QtCore.SIGNAL('clicked()'), self.w9Clicked)
        
    def arteClicked(self):
        print 'TvDownloaderSitesWidgetController>> arteClicked'
        
    def canalClicked(self):
        print 'TvDownloaderSitesWidgetController>> canalClicked'
    
    def m6Clicked(self):
        print 'TvDownloaderSitesWidgetController>> m6Clicked'
    
    def pluzzClicked(self):
        print 'TvDownloaderSitesWidgetController>> pluzzClicked'
        self.mainWindow.updateCentralWidget('site_pluzz')
        
    def w9Clicked(self):
        print 'TvDownloaderSitesWidgetController>> w9Clicked'