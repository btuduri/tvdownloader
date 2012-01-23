#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from API import API
from Navigateur import Navigateur

from time import time, sleep

urlsDifferentHost = ["http://www.google.fr/",
"http://fr.yahoo.com/",
"http://www.bing.com/",
"http://www.ubuntu-fr.org/",
"http://www.canalplus.fr/",
"http://www.m6.fr/",
"http://www.w9.fr/",
"http://www.tf1.fr/",
"http://www.france2.fr/",
"http://www.france3.fr/",
"http://www.france4.fr/",
"http://www.france5.fr/",
"http://www.franceo.fr/"]

urlsSameHost = ["http://www.canalplus.fr/c-divertissement/pid1784-les-guignols-de-l-info.html?",
"http://www.canalplus.fr/c-divertissement/pid1778-pepites-sur-le-net.html?",
"http://www.canalplus.fr/c-divertissement/pid3279-reperages-l-emission.html?",
"http://www.canalplus.fr/c-divertissement/pid2053-stephane-guillon.html?",
"http://www.canalplus.fr/c-divertissement/pid3591-une-minute-avant.html?",
"http://www.canalplus.fr/c-divertissement/pid3403-c-air-guitar-2010.html",
"http://www.canalplus.fr/c-divertissement/pid3299-album-de-la-semaine.html?",
"http://www.canalplus.fr/c-divertissement/pid3301-concert-prive.html?",
"http://www.canalplus.fr/c-divertissement/pid3535-c-la-musicale.html",
"http://www.canalplus.fr/c-divertissement/pid3308-la-radio-de-moustic.html?",
"http://www.canalplus.fr/c-divertissement/pid3298-coming-next.html?",
"http://www.canalplus.fr/c-divertissement/pid3522-u2-en-concert.html?",
"http://www.canalplus.fr/c-divertissement/pid3303-le-live-du-grand-journal.html?"]

navigateur = Navigateur()
api = API.getInstance()

def testeMechanize(urls):
	reponses = {}
	for url in urls:
		reponses[ url ] = navigateur.getPage( url )

def testeGetPage(urls):
	reponses = {}
	for url in urls:
		reponses[ url ] = api.getPage( url )

def testeGetPages(urls):
	reponses = api.getPages(urls)

#~ t = time()

print "Url sur différent serveur:"
sleep(1)
t = time()
testeMechanize(urlsDifferentHost)
print "Mechanize:",time()-t,"secondes"
#~ 
sleep(1)
t = time()
testeGetPage(urlsDifferentHost)
print "getPage:",time()-t,"secondes"
#~ 
sleep(1)
t = time()
testeGetPages(urlsDifferentHost)
print "getPages:",time()-t,"secondes"


#~ print "\nUrl sur un même serveur:"
#~ sleep(1)
#~ t = time()
#~ testeMechanize(urlsSameHost)
#~ print "Mechanize:",time()-t,"secondes"
#~ 
#~ sleep(1)
#~ t = time()
#~ testeGetPage(urlsSameHost)
#~ print "getPage:",time()-t,"secondes"
#~ 
#~ sleep(1)
#~ t = time()
#~ testeGetPages(urlsSameHost)
#~ print "getPages:",time()-t,"secondes"

