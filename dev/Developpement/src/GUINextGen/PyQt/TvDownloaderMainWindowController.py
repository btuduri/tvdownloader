# -*- coding: utf-8 -*-

# Last change: 2011/01/11
#
# Author: psyphi <psyphi@gmail.com>

from GUI.AProposDialog import AProposDialog
from GUI.PreferencesDialog import PreferencesDialog
from TvDownloaderMainWindowView import Ui_TvDownloaderMainWindow
from TvDownloaderSitesWidgetController import TvDownloaderSitesWidgetController
from PyQt4 import QtGui, QtCore

class TvDownloaderMainWindowController(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Load the View
        self.ui = Ui_TvDownloaderMainWindow()
        self.ui.setupUi(self)
        
        # Connect the HMI Events
        self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionUpdatePlugins, QtCore.SIGNAL('triggered()'), self.openUpdatePluginsWindow)
        self.connect(self.ui.actionPreferences, QtCore.SIGNAL('triggered()'), self.openPreferencesWindow)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.openAboutDialog)
        
        # Define the other widgets
        self.updatePluginsDlg = None
        self.preferencesDlg = None
        self.aboutDlg = None
        
        #
        self.sitesWidget = TvDownloaderSitesWidgetController()
        
        # Init the main widget
        self.setCentralWidget(self.sitesWidget)
    
    def openUpdatePluginsWindow(self):
        print 'openUpdatePluginsWindow'
#        if self.updatePluginsDlg == None:
#            self.updatePluginsDlg = None
            
    def openPreferencesWindow(self):
        if self.preferencesDlg == None:
            self.preferencesDlg = PreferencesDialog()
        self.preferencesDlg.afficher()
        
    def openAboutDialog(self):
        if self.aboutDlg == None:
            self.aboutDlg = AProposDialog()
        self.aboutDlg.show()
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win = TvDownloaderMainWindowController()
    win.show()
    sys.exit(app.exec_())    