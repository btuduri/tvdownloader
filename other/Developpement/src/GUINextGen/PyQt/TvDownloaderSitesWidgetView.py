# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TvDownloaderSitesWidget.ui'
#
# Created: Thu Jan 13 22:07:19 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TvDownloaderSitesWidget(object):
    def setupUi(self, TvDownloaderSitesWidget):
        TvDownloaderSitesWidget.setObjectName("TvDownloaderSitesWidget")
        TvDownloaderSitesWidget.resize(760, 540)
        self.gridLayoutWidget = QtGui.QWidget(TvDownloaderSitesWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 741, 521))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_TV = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_TV.setObjectName("gridLayout_TV")
        self.pushButton_Arte = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_Arte.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_Arte.setMouseTracking(False)
        self.pushButton_Arte.setFocusPolicy(QtCore.Qt.TabFocus)
        self.pushButton_Arte.setAutoFillBackground(False)
        self.pushButton_Arte.setText("Arte")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/07_ARTE_256x256.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Arte.setIcon(icon)
        self.pushButton_Arte.setIconSize(QtCore.QSize(128, 128))
        self.pushButton_Arte.setObjectName("pushButton_Arte")
        self.gridLayout_TV.addWidget(self.pushButton_Arte, 0, 0, 1, 1)
        self.pushButton_Canal = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_Canal.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_Canal.setMouseTracking(False)
        self.pushButton_Canal.setFocusPolicy(QtCore.Qt.TabFocus)
        self.pushButton_Canal.setAutoFillBackground(False)
        self.pushButton_Canal.setText("Canal+")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/04_Canal+_256x256.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Canal.setIcon(icon1)
        self.pushButton_Canal.setIconSize(QtCore.QSize(128, 128))
        self.pushButton_Canal.setObjectName("pushButton_Canal")
        self.gridLayout_TV.addWidget(self.pushButton_Canal, 0, 1, 1, 1)
        self.pushButton_Pluzz = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_Pluzz.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_Pluzz.setMouseTracking(False)
        self.pushButton_Pluzz.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_Pluzz.setAutoFillBackground(False)
        self.pushButton_Pluzz.setText("Pluzz")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/Pluzz_470x318.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Pluzz.setIcon(icon2)
        self.pushButton_Pluzz.setIconSize(QtCore.QSize(128, 128))
        self.pushButton_Pluzz.setObjectName("pushButton_Pluzz")
        self.gridLayout_TV.addWidget(self.pushButton_Pluzz, 1, 0, 1, 1)
        self.pushButton_W9Replay = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_W9Replay.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_W9Replay.setMouseTracking(False)
        self.pushButton_W9Replay.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_W9Replay.setAutoFillBackground(False)
        self.pushButton_W9Replay.setText("W9 Replay")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/W9_Replay_220x122.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_W9Replay.setIcon(icon3)
        self.pushButton_W9Replay.setIconSize(QtCore.QSize(128, 128))
        self.pushButton_W9Replay.setObjectName("pushButton_W9Replay")
        self.gridLayout_TV.addWidget(self.pushButton_W9Replay, 1, 1, 1, 1)
        self.pushButton_M6Replay = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_M6Replay.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_M6Replay.setMouseTracking(False)
        self.pushButton_M6Replay.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_M6Replay.setAutoFillBackground(False)
        self.pushButton_M6Replay.setText("M6 Replay")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/M6_Replay_450x295.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_M6Replay.setIcon(icon4)
        self.pushButton_M6Replay.setIconSize(QtCore.QSize(128, 128))
        self.pushButton_M6Replay.setObjectName("pushButton_M6Replay")
        self.gridLayout_TV.addWidget(self.pushButton_M6Replay, 0, 2, 1, 1)

        self.retranslateUi(TvDownloaderSitesWidget)
        QtCore.QMetaObject.connectSlotsByName(TvDownloaderSitesWidget)

    def retranslateUi(self, TvDownloaderSitesWidget):
        TvDownloaderSitesWidget.setWindowTitle(QtGui.QApplication.translate("TvDownloaderSitesWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TvDownloaderSitesWidget = QtGui.QWidget()
    ui = Ui_TvDownloaderSitesWidget()
    ui.setupUi(TvDownloaderSitesWidget)
    TvDownloaderSitesWidget.show()
    sys.exit(app.exec_())

