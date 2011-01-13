from PyQt4 import QtGui, QtCore

from TvDownloaderPluzzWidgetView import Ui_TvDownloaderPluzzWidget

class TvDownloaderPluzzWidgetController(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        
        self.mainWindow = parent
        
        self.ui = Ui_TvDownloaderPluzzWidget()
        self.ui.setupUi(self)
        
        # Connect the events
        self.connect(self.ui.pushButton_France2, QtCore.SIGNAL('clicked()'), self.france2Clicked)
        self.connect(self.ui.pushButton_France3, QtCore.SIGNAL('clicked()'), self.france3Clicked)
        self.connect(self.ui.pushButton_France4, QtCore.SIGNAL('clicked()'), self.france4Clicked)
        self.connect(self.ui.pushButton_France5, QtCore.SIGNAL('clicked()'), self.france5Clicked)
        self.connect(self.ui.pushButton_FranceO, QtCore.SIGNAL('clicked()'), self.franceOClicked)
        self.connect(self.ui.pushButton_Back, QtCore.SIGNAL('clicked()'), self.backClicked)
        
    def france2Clicked(self):
        print 'TvDownloaderPluzzWidgetController>> france2 clicked'
    
    def france3Clicked(self):
        print 'TvDownloaderPluzzWidgetController>> france3 clicked'
    
    def france4Clicked(self):
        print 'TvDownloaderPluzzWidgetController>> france4 clicked'
        
    def france5Clicked(self):
        print 'TvDownloaderPluzzWidgetController>> france5 clicked'
        
    def franceOClicked(self):
        print 'TvDownloaderPluzzWidgetController>> franceO clicked'
        
    def backClicked(self):
        print 'TvDownloaderPluzzWidgetController>> franceO clicked'
        self.mainWindow.updateCentralWidget('back')