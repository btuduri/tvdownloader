
from PyQt4 import QtGui, QtCore

from TvDownloaderSitesWidgetView import Ui_TvDownloaderSitesWidget

class TvDownloaderSitesWidgetController(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.ui = Ui_TvDownloaderSitesWidget()
        self.ui.setupUi(self)