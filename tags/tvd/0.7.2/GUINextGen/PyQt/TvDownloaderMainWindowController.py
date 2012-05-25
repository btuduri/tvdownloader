from PyQt4 import QtGui, QtCore
from GUI.AProposDialog import AProposDialog
from GUI.PreferencesDialog import PreferencesDialog
from GUI.UpdateManagerDialog import UpdateManagerDialog
from TvDownloaderMainWindowView import Ui_TvDownloaderMainWindow
from TvDownloaderSitesWidgetController import TvDownloaderSitesWidgetController
from TvDownloaderPluzzWidgetController import TvDownloaderPluzzWidgetController


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
        
        # Define the other dialogs
        self.updatePluginsDlg = None
        self.preferencesDlg = None
        self.aboutDlg = None
        
        # Init the main widget
        self.previousWidgetID = 'main_menu'
        self.updateCentralWidget(self.previousWidgetID)
    
    def updateCentralWidget(self, strWidgetID):
        
        if strWidgetID == 'main_menu':
            self.setCentralWidget(TvDownloaderSitesWidgetController(self))
        elif strWidgetID == "site_arte":
            print 'TvDownloaderMainWindowController>> display site Arte'
        elif strWidgetID == "site_canal":
            print 'TvDownloaderMainWindowController>> display site Canal+'
        elif strWidgetID == "site_m6replay":
            print 'TvDownloaderMainWindowController>> display site M6Replay'
        elif strWidgetID == "site_pluzz":
            print 'TvDownloaderMainWindowController>> display site Pluzz'
            self.setCentralWidget(TvDownloaderPluzzWidgetController(self))
        elif strWidgetID == "site_w9replay":
            print 'TvDownloaderMainWindowController>> display site W9'
        elif strWidgetID == 'back':
            print 'TvDownloaderMainWindowController>> back'
            self.updateCentralWidget(self.previousWidgetID)
    
    def openUpdatePluginsWindow(self):
        if self.updatePluginsDlg == None:
            self.updatePluginsDlg = UpdateManagerDialog(self)
        self.updatePluginsDlg.afficher()
            
    def openPreferencesWindow(self):
        if self.preferencesDlg == None:
            self.preferencesDlg = PreferencesDialog(self)
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