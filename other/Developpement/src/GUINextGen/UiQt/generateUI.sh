#!/bin/sh

pyuic4 -o ../PyQt/TvDownloaderMainWindowView.py  -x TvDownloaderMainWindow.ui
pyuic4 -o ../PyQt/TvDownloaderPluzzWidgetView.py -x TvDownloaderPluzzWidget.ui
pyuic4 -o ../PyQt/TvDownloaderSitesWidgetView.py -x TvDownloaderSitesWidget.ui
cp ./ico/* ../../ico/
cp ./img/* ../../img/
