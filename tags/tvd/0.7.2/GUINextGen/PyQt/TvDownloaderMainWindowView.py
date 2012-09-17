# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TvDownloaderMainWindow.ui'
#
# Created: Thu Jan 13 22:07:18 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TvDownloaderMainWindow(object):
    def setupUi(self, TvDownloaderMainWindow):
        TvDownloaderMainWindow.setObjectName("TvDownloaderMainWindow")
        TvDownloaderMainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ico/TVDownloader.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TvDownloaderMainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(TvDownloaderMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 5, 760, 540))
        self.widget.setObjectName("widget")
        TvDownloaderMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TvDownloaderMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtGui.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuEdition = QtGui.QMenu(self.menubar)
        self.menuEdition.setObjectName("menuEdition")
        self.menuAide = QtGui.QMenu(self.menubar)
        self.menuAide.setObjectName("menuAide")
        TvDownloaderMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TvDownloaderMainWindow)
        self.statusbar.setObjectName("statusbar")
        TvDownloaderMainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(TvDownloaderMainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ico/gtk-quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon1)
        self.actionQuit.setMenuRole(QtGui.QAction.QuitRole)
        self.actionQuit.setIconVisibleInMenu(True)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtGui.QAction(TvDownloaderMainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ico/gtk-about.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon2)
        self.actionAbout.setIconVisibleInMenu(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionUpdatePlugins = QtGui.QAction(TvDownloaderMainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ico/gtk-refresh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUpdatePlugins.setIcon(icon3)
        self.actionUpdatePlugins.setIconVisibleInMenu(True)
        self.actionUpdatePlugins.setObjectName("actionUpdatePlugins")
        self.actionPreferences = QtGui.QAction(TvDownloaderMainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ico/gtk-preferences.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon4)
        self.actionPreferences.setIconVisibleInMenu(True)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFichier.addAction(self.actionQuit)
        self.menuEdition.addAction(self.actionUpdatePlugins)
        self.menuEdition.addAction(self.actionPreferences)
        self.menuAide.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())

        self.retranslateUi(TvDownloaderMainWindow)
        QtCore.QMetaObject.connectSlotsByName(TvDownloaderMainWindow)

    def retranslateUi(self, TvDownloaderMainWindow):
        TvDownloaderMainWindow.setWindowTitle(QtGui.QApplication.translate("TvDownloaderMainWindow", "TvDownloader", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFichier.setTitle(QtGui.QApplication.translate("TvDownloaderMainWindow", "Fichier", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdition.setTitle(QtGui.QApplication.translate("TvDownloaderMainWindow", "Edition", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAide.setTitle(QtGui.QApplication.translate("TvDownloaderMainWindow", "Aide", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("TvDownloaderMainWindow", "Quitter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("TvDownloaderMainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("TvDownloaderMainWindow", "A propos", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdatePlugins.setText(QtGui.QApplication.translate("TvDownloaderMainWindow", "Mise à jour des plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdatePlugins.setShortcut(QtGui.QApplication.translate("TvDownloaderMainWindow", "Ctrl+U", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("TvDownloaderMainWindow", "Préférences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setShortcut(QtGui.QApplication.translate("TvDownloaderMainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TvDownloaderMainWindow = QtGui.QMainWindow()
    ui = Ui_TvDownloaderMainWindow()
    ui.setupUi(TvDownloaderMainWindow)
    TvDownloaderMainWindow.show()
    sys.exit(app.exec_())

