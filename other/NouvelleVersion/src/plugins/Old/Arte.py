#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier COPYING #
#########################################

# Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
# Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
# Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import os

from urllib import quote,unquote
import re,unicodedata
import time,rfc822 # for RFC822 datetime format (rss feed)
from datetime import datetime
from htmlentitydefs import name2codepoint

from core import Plugin
from core import Fichier

##########
# Classe #
##########

class Arte(Plugin):

    ##
    ## Arte Live Web
    ##
    configArteLiveWeb = {
        'nom' : "Arte Live Web",
        'qualite' : ['SD', 'HD', 'Live'],
        'regexEmissions' : {
            'url' : "http://liveweb.arte.tv/",
            # Attention à bien nommer les zones de recherche "lien" et "nom"
            'pattern' : re.compile("<li><a href=\"http://liveweb.arte.tv/fr/cat/(?P<lien>.*?)\" class=\"accueil\">(?P<nom>.*?)</a></li>", re.DOTALL)
        },
        'regexListeFichiers' : {
            0 : {
                # %emission% représente l'émission à lister
                'url' : "http://liveweb.arte.tv/fr/cat/%emission%",
                'pattern' : re.compile("<a href=\"(http://download.liveweb.arte.tv/o21/liveweb/rss/home.*?\.rss)\"", re.DOTALL)
            },
            1 : {
                # %pattern% représente le résultat de l'expression régulière précédente
                'url' : "%pattern%",
                # Expression régulière pour extraire les blocs descriptifs de chaque fichier
                'pattern' : re.compile("(<item>.*?</item>)", re.DOTALL)
            },
        },
        'regexInfosFichiers' : {
            0 : {
                # Premère regex, ne se base pas sur une URL mais sur les données extraites par regexListeFichiers
                # Liste des informations à récupérer
                'patterns' : {
                    'titre' : re.compile("<title>(.*?)</title>", re.DOTALL),
                    'lien' : re.compile("<link>(http://liveweb.arte.tv/fr/video/.*?)</link>", re.DOTALL),
                    'date' : re.compile("<pubDate>(.*?)</pubDate>", re.DOTALL),
                    'description' : re.compile("<description>(.*?)</description>", re.DOTALL),
                    #'eventid' : re.compile("<enclosure.*?/event/(.*?)/.*?/>", re.DOTALL),
                    'eventid' : re.compile("<enclosure.*?/event/.*?/(.*?)-.*?/>", re.DOTALL)
                }
            },
            1 : {
                # Les variables %xxx% sont remplacées par les éléments déjà trouvés via les expressions précédentes
                'url' : "%lien%",
                # optional = 1, cette étape n'est pas exécutée en mode TURBO
                'optional' : 1,
                # Liste des informations à récupérer
                'patterns' : {
                    'eventid_html': re.compile("new LwEvent\('(.*?)', ''\);", re.DOTALL)
                },
            },
            2 : {
                # Les variables %xxx% sont remplacées par les éléments déjà trouvés via les expressions précédentes
                'url' : "http://arte.vo.llnwd.net/o21/liveweb/events/event-%eventid%.xml",
                # Liste des informations à récupérer
                'patterns' : {
                    'titre' : re.compile("<nameFr>(.*?)</nameFr>", re.DOTALL),
                    'lien.HD': re.compile("<urlHd>(.*?)</urlHd>", re.DOTALL),
                    'lien.SD': re.compile("<urlSd>(.*?)</urlSd>", re.DOTALL),
                    'lien.Live': re.compile("<liveUrl>(.*?)</liveUrl>", re.DOTALL)
                },
            },
        },
        'infosFichier' : {
            'nom' : "[%qualite%] %titre%",
            'date' : "%date%",
            'lien' : "%lien%",
            #'nomFichierSortieStd' : "%lien%",
            #'nomFichierSortieRen' : "%titre%",
            #~ 'urlImage' : "http://download.liveweb.arte.tv/o21/liveweb/media/event/%eventid%/%eventid%-visual-cropcropcrop-small.jpg",
            'urlImage' : "http://download.liveweb.arte.tv/o21/liveweb/media/event/%eventid%/%eventid%-visual.jpg",
            'descriptif' : "%description%"
        }
    }
        
    ##
    ## Arte+7
    ##
    # En cas de souci, on pourrait utiliser la page RSS de chaque chaine
    # Pour récupérer la liste des chaines (càd la liste des flux RSS)
    #    http://videos.arte.tv/fr/videos/meta/index-3188674-3223978.html
    # Pour récupérer la liste des émissions d'une chaine
    #    http://videos.arte.tv/fr/do_delegate/videos/programmes/360_geo/index-3188704,view,rss.xml
    configArtePlusSept = {
        'nom' : "Arte+7",
        'qualite' : ['SD', 'HD'],
        'regexEmissions' : {
            'url' : "http://videos.arte.tv/fr/videos",
            # Attention à bien nommer les zones de recherche "lien" et "nom"
            'pattern' : re.compile("<input type=\"checkbox\" value=\"(?P<lien>.*?)\"/>.*?<a href=\"#\">(?P<nom>.*?)</a>", re.DOTALL)
        },
        'regexListeFichiers' : {
            0 : {
                # %emission% représente l'émission à lister
                'url' : "http://videos.arte.tv/fr/do_delegate/videos/index-%emission%-3188698,view,asList.html?hash=fr/list/date//1/250/",
                # Expression régulière pour extraire les blocs descriptifs de chaque vidéo
                'pattern' : re.compile("(<tr.*?>.*?</tr>)", re.DOTALL)
            },
        },
        'regexInfosFichiers' : {
            0 : {
                # Premère regex, ne se base pas sur une URL mais sur les données extraites par regexListeFichiers
                # Liste des informations à récupérer
                # Les expressions de type texte %xxx% sont remplacées par les options du plugin (choix arbitraire pour l'instant)
                'patterns' : {
                    'titre' : re.compile("title=\"(.*?)\|\|", re.DOTALL),
                    'lien' : re.compile("<a href=\"/(fr/videos/.*?\.html)\">", re.DOTALL),
                    'date' : re.compile("<em>(.*?)</em>", re.DOTALL),
                    'description' : re.compile("\|\|(.*?)\">", re.DOTALL),
                    'guid' : re.compile("{ajaxUrl:'.*-(.*?).html", re.DOTALL),
                    'player_swf' : "%default_playerSWF%",
                }
            },
            1 : {
                # Les variables %xxx% sont remplacées par les éléments déjà trouvés via les expressions précédentes
                'url' : "http://videos.arte.tv/%lien%",
                # optional = 1, cette étape n'est pas exécutée en mode TURBO
                'optional' : 1,
                # Liste des informations à récupérer
                'patterns' : {
                    'player_swf' : re.compile("<param name=\"movie\" value=\"(.*?\.swf)", re.DOTALL),
                    'titre' : re.compile("<div class=\"recentTracksMast\">.*?<h3>(.*?)</h3>.*?</div>", re.DOTALL),
                    'image' : re.compile("<link rel=\"image_src\" href=\"(.*?)\"/>", re.DOTALL),
                    'description' : re.compile("<div class=\"recentTracksCont\">.*?<div>(.*?)</div>", re.DOTALL),
                    'guid': re.compile("addToPlaylistOpen {ajaxUrl:'/fr/do_addToPlaylist/videos/.*?-(.*?)\.html'}", re.DOTALL)
                },
            },
            2 : {
                # Les variables %xxx% sont remplacées par les éléments déjà trouvés via les expressions précédentes
                'url' : "http://videos.arte.tv/fr/do_delegate/videos/-%guid%,view,asPlayerXml.xml",
                # Liste des informations à récupérer
                'patterns' : {
                    'titre' : re.compile("<name>(.*?)</name>", re.DOTALL),
                    'date' : re.compile("<dateVideo>(.*?)</dateVideo>", re.DOTALL),
                    'image' : re.compile("<firstThumbnailUrl>(.*?)</firstThumbnailUrl>", re.DOTALL),
                    'lien.HD': re.compile("<url quality=\"hd\">(.*?)</url>", re.DOTALL),
                    'lien.SD': re.compile("<url quality=\"sd\">(.*?)</url>", re.DOTALL),
                },
            },
        },
        'infosFichier' : {
            'nom' : "[%qualite%] %titre%",
            'date' : "%date%",
            'lien' : "%lien% -W %player_swf%",
            #'nomFichierSortieStd' : "%lien%.mp4",
            #'nomFichierSortieRen' : "%titre%",
            'urlImage' : "%image%",
            'descriptif' : "%description%"
        }
    }

    ##
    ## Options du plugin
    ##
    listeOptions = {
        0: {
            # Qualité à rechercher SD ou HD ?
            'type' : "ChoixUnique",
            'nom' : "qualite",
            'description' : "Qualité des vidéos",
            'defaut' : "HD",
            'valeurs' : ["HD", "SD","HD & SD"],
        },
        1: {
            # Nombre maximum de fichiers à rechercher (0 = aucune limite)
            'type' : "Texte",
            'nom' : "max_files",
            'description' : "Nombre d'enregistrements à analyser\n(0=pas de limite)",
            'defaut' : "20",
        },
        2: {
            # Renommer les fichiers à partir du titre de l'émission
            'type' : "Bouleen",
            'nom' : "rename_files",
            'description' : "Renommer les fichiers à partir du titre de l'émission\nATTENTION : plusieurs enregistrements peuvent avoir le même nom",
            'defaut' : False,
        },
        3: {
            # Mode turbo : charge moins de pages, donc plus rapide, mais moins de détails
            'type' : "Bouleen",
            'nom' : "turbo_mode",
            'description' : "Mode TURBO\nChargement plus rapide mais informations moins détaillées",
            'defaut' : False,
        },
        4: {
            # PlayerSWF par default pour Arte+7
            'type' : "Texte",
            'nom' : "default_playerSWF",
            'description' : "Player Arte+7 à utiliser par défaut (en mode TURBO)\nATTENTION : Réservé aux utilisateurs avancés",
            'defaut' : "http://videos.arte.tv/blob/web/i18n/view/player_11-3188338-data-4785094.swf",
        }
    }
    
    nom = "Arte"
    url = "http://www.arte.tv/"
    listeChaines = {} # Clef = Nom Chaine, Valeur = { Nom emission : Lien }
    
    # Supprime les caractères spéciaux HTML du tyle &#nn;
    # http://www.w3.org/QA/2008/04/unescape-html-entities-python.html
    # http://bytes.com/topic/python/answers/21074-unescaping-xml-escape-codes
    def htmlent2chr(self, s):
        def ent2chr(m):
            code = m.group(1)
            if code.isdigit(): code = int(code)
            else: code = int(code[1:], 16)
            if code<256: return chr(code)
            else: return '?' #XXX unichr(code).encode('utf-16le') ??
        return re.sub(r'\&\#(x?[0-9a-fA-F]+);', ent2chr, s)

    # Supprime les caractères spéciaux HTML
    # http://wiki.python.org/moin/EscapingHtml
    def htmlentitydecode(self, s):
        return re.sub('&(%s);' % '|'.join(name2codepoint), 
                lambda m: unichr(name2codepoint[m.group(1)]), s)

    # Supprime les caractères spéciaux pour obtenir un nom de fichier correct
    def cleanup_filename (self, s):
        nouvNom = s
        nouvNom = nouvNom.replace(" ","_")
        nouvNom = nouvNom.replace(":","_")
        nouvNom = nouvNom.replace("/","_")
        nouvNom = nouvNom.replace("\\","_")
        nouvNom = nouvNom.replace("?","_")
        return nouvNom

    # Fonction parse_date recopiée de l'application arte+7recorder
    # Permet de convertir une date issue d'Arte+7 (hier, aujourd'hui...) en vrai date
    def parse_date(self, date_str):
        time_re = re.compile("^\d\d[h:]\d\d$")
        fr_monthesL = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        fr_monthesC = ["janv.", "fevr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
        de_monthes = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

        date_array = date_str.split(",")
        if time_re.search(date_array[-1].strip()) is None:
            return ""
        time_ = date_array[-1].strip()
        if date_array[0].strip() in ("Aujourd'hui", "Heute"):
            date_ = time.strftime("%Y/%m/%d")
        elif date_array[0].strip() in ("Hier", "Gestern"):
            date_ = time.strftime("%Y/%m/%d", time.localtime(time.time() - (24*60*60)))
        else:
            array = date_array[1].split()
            day = array[0].strip(".")
            month = array[1]
            for arr in (fr_monthesL, fr_monthesC, de_monthes):
                if array[1] in arr:
                    month = "%02d" % (arr.index(array[1])+1)
            year = array[2]
            date_ = "%s/%s/%s" % (year, month, day)
        return date_ + ", " + time_

    def __init__(self):
        Plugin.__init__(self, self.nom, self.url, 7) #7 = fréquence de rafraichissement

        if os.path.exists(self.fichierCache):
                self.listeChaines = self.chargerCache()

    def debug_savefile (self, buffer):
        path = os.path.expanduser( "~" )
        fichierDebug = path+"/.tvdownloader/"+self.nom.replace( " ", "_" )+".log"
        file = open(fichierDebug, "w")
        file.write (buffer)
        file.close()

    def debug_print (self, variable):
        #~ print str(variable).replace("},", "},\n\n").replace("',", "',\n").replace("\",", "\",\n")
        print str(variable).replace("{", "\n\n{").replace(", ", ",\n")

    def listerOptions(self):
        for option in self.listeOptions.values():
            if option['type']=="ChoixUnique":
                self.optionChoixUnique(option['nom'], option['description'], option['defaut'], option['valeurs'])
            elif option['type']=="ChoixMultiple":
                self.optionChoixMultiple(option['nom'], option['description'], option['defaut'], option['valeurs'])
            elif option['type']=="Texte":
                self.optionTexte(option['nom'], option['description'], option['defaut'])
            elif option['type']=="Bouleen":
                self.optionBouleen(option['nom'], option['description'], option['defaut'])


    def rafraichir(self):
        self.afficher("Global : Création de la liste des chaines...")

        # On remet a 0 la liste des chaines
        self.listeChaines.clear()

        # On boucle sur chaque "chaine" à analyser
        for chaineActuelle in [self.configArteLiveWeb, self.configArtePlusSept]:
            self.afficher (chaineActuelle['nom']+" Récupération de la liste des catégories "+chaineActuelle['nom']+"...")
            listeEmissions = {}
            # On recherche toutes les catégories
            for item in re.finditer(chaineActuelle['regexEmissions']['pattern'], self.getPage(chaineActuelle['regexEmissions']['url'])):
                self.afficher (chaineActuelle['nom']+" ... Catégorie "+item.group('nom')+" : "+item.group('lien')+".")
                listeEmissions[item.group('nom')]=item.group('lien')
            self.listeChaines[chaineActuelle['nom']] = listeEmissions

        # On sauvegarde les chaines trouvées
        self.listerOptions()
        self.sauvegarderCache(self.listeChaines)
        self.afficher("Global : Emissions conservées.")

    def listerChaines(self):
        liste = self.listeChaines.keys()
        liste.sort()
        for chaine in liste:
            self.ajouterChaine(chaine)

    def listerEmissions(self, chaine):
        if(self.listeChaines.has_key(chaine)):
            self.derniereChaine = chaine
            liste = self.listeChaines[chaine].keys()
            liste.sort()
        for emission in liste:
            self.ajouterEmission(chaine, emission)

    def getLienEmission(self, emission):
        # Cherche dans quelle chaine se trouve l'émission
        if(self.listeChaines.has_key(self.derniereChaine)):
            listeEmissions = self.listeChaines[ self.derniereChaine ]
            if(listeEmissions.has_key(emission)):
                return listeEmissions[ emission ]

    def chargeListeEnregistrements(self, emission, chaineActuelle):
        emissionID = self.getLienEmission(emission)
        if emissionID == None:
            self.afficher (chaineActuelle['nom']+" Erreur de recherche du lien pour \""+emission+"\"")
            return None
        else:
            self.afficher (chaineActuelle['nom']+" Liste des enregistrements pour \""+emission+"\"...")
            pattern = ""
            for unItem in chaineActuelle['regexListeFichiers'].values():
                #~ print str(chaineActuelle['regexListeFichiers'])
                # Construction du lien contenant toutes les émissions de cette catégorie
                lienPage = unItem['url'].replace("%emission%", emissionID).replace("%pattern%", pattern)
                self.afficher (chaineActuelle['nom']+" ... lecture de la page "+lienPage)
                laPage = self.getPage(lienPage)
                if len(laPage)>0:
                    foundItems = re.findall(unItem['pattern'], laPage)
                    pattern = foundItems[0]
                    self.afficher (chaineActuelle['nom']+" On a listé " + str(len(foundItems)) + " enregistrements.")
                else:
                    self.afficher (chaineActuelle['nom']+" Impossible de charger la page. Aucun enregistrement trouvé !")
                    foundItems = None
            return foundItems

    def ajouteFichiers (self, emission, listeEnregistrement, chaineActuelle):
        self.afficher (chaineActuelle['nom']+" On ajoute les enregitrements trouvés.")
        opt_renameFiles = self.getOption("rename_files")
        opt_qual = self.getOption("qualite")
        nbLiens = 0

        for keyEnregistrement in listeEnregistrement.keys():
            # on supprime l'enregistrement avec son index actuel
            unEnregistrement = listeEnregistrement.copy()[keyEnregistrement]
            for infosQualite in chaineActuelle['qualite']:
                infosFichier = {}
                if opt_qual.find(infosQualite)>=0:
                    # Lien dans la qualité voulue
                    unEnregistrement['lien'] = unEnregistrement.get('lien.'+infosQualite, None)
                    if unEnregistrement['lien'] == None:
                        self.afficher (chaineActuelle['nom']+" ... Pas de lien "+infosQualite+" trouvé.")
                        continue

                    # Date, mise en forme
                    rfc_date = rfc822.parsedate(unEnregistrement['date'])
                    # Format année/mois/jour hh:mm, mieux pour effectuer un tri
                    unEnregistrement['date'] = time.strftime("%Y/%m/%d %H:%M", rfc_date)

                    lesInfos = {}
                    for keyInfo in chaineActuelle['infosFichier'].keys():
                        uneInfo = chaineActuelle['infosFichier'][keyInfo]
                        # On effectue les remplacements selon les informations collectées
                        for unTag in unEnregistrement.keys():
                            if unEnregistrement[unTag] != None:
                                uneInfo = uneInfo.replace("%"+unTag+"%", unEnregistrement[unTag])
                            else:
                                uneInfo = uneInfo.replace("%"+unTag+"%", "")
                            # Qualité de la video
                            uneInfo = uneInfo.replace("%qualite%", infosQualite)
                        lesInfos[keyInfo] = uneInfo


                    # Nom fichier
                    if opt_renameFiles:
                        nomFichierSortie = self.cleanup_filename(unEnregistrement['titre'])
                    else:
                        nomFichierSortie = unEnregistrement['lien'].split('/')[-1]
                        if nomFichierSortie.find('?')>0:
                            nomFichierSortie = nomFichierSortie.split('?')[0]
                    if not re.match(".*\.mp4", nomFichierSortie):
                        nomFichierSortie = nomFichierSortie+".mp4"

                    # Ajout du fichier
                    nbLiens += 1

                    self.afficher (chaineActuelle['nom']+" Ajoute dans la liste...")
                    self.afficher (chaineActuelle['nom']+" ... Date : "+ lesInfos['date'])
                    self.afficher (chaineActuelle['nom']+" ... Nom : "+ lesInfos['nom'])
                    self.afficher (chaineActuelle['nom']+" ... Lien : " + lesInfos['lien'])
                    self.afficher (chaineActuelle['nom']+" ... Image : " + lesInfos['urlImage'])
                    self.afficher (chaineActuelle['nom']+" ... Nom fichier : " + nomFichierSortie)

                    leFichier = Fichier(
                        lesInfos['nom'],
                        lesInfos['date'],
                        lesInfos['lien'],
                        nomFichierSortie,
                        lesInfos['urlImage'],
                        lesInfos['descriptif']
                    )
                    self.ajouterFichier(emission, leFichier)
        return nbLiens
    
    def listerEnregistrements(self, emission, chaineActuelle):
        opt_maxFiles = int(self.getOption("max_files"))
        opt_turbo = self.getOption("turbo_mode")

        nbLiens = 0

        # Charge la page contenant la liste des émissions
        videosList = self.chargeListeEnregistrements(emission, chaineActuelle)

        # A-t-on une liste d'enregistrements ?
        if videosList != None:
            listeEnregistrement = {}
            # Boucle sur chaque traitement de recherche
            for unItem in chaineActuelle['regexInfosFichiers'].values():
                optional = unItem.get('optional',0)
                if not (opt_turbo and optional):
                    if unItem.get('url', None) == None:
                        # On n'a pas d'url, on travaille sur videoList
                        # C'est la première passe
                        nbFichiers = 0
                        lesPages = {}
                        for infosVideo in videosList:
                            lesPages[nbFichiers] = infosVideo
                            # On crée, et on indexe listeEnregistrement en phase avec videosList
                            listeEnregistrement[nbFichiers] = {}
                            nbFichiers += 1
                            if (opt_maxFiles>0 and nbFichiers>=opt_maxFiles):
                                break
                    else:
                        # Chargement des pages HTML sur lesquelles on va devoir travailler
                        self.afficher (chaineActuelle['nom']+" Chargement des pages nécessaires...")
                        listeURL = []
                        # On boucle sur chaque enregistrement à travailler
                        for keyEnregistrement in listeEnregistrement.keys():
                            # on supprime l'enregistrement avec son index actuel
                            unEnregistrement = listeEnregistrement.pop (keyEnregistrement)
                            lienHTML = unItem['url']
                            # On effectue les remplacements des paramètres dans l'url
                            for unTag in unEnregistrement.keys():
                                if unEnregistrement[unTag] != None:
                                    lienHTML = lienHTML.replace("%"+unTag+"%", unEnregistrement[unTag])
                                else:
                                    lienHTML = lienHTML.replace("%"+unTag+"%", "")
                            listeURL.append(lienHTML)
                            # on recrée l'enregistrement avec son nouvel index
                            listeEnregistrement[lienHTML] = unEnregistrement
                        # On charge les pages désirées
                        lesPages = self.getPages(listeURL)

                    # On boucle et exécute les expressions régulières
                    for pageNum in lesPages.keys():
                        unePage = lesPages[pageNum]
                        if len(unePage)==0:
                            self.afficher (chaineActuelle['nom']+" ERREUR : La page "+pageNum+" n'a pas été chargée !")
                        #~ print "Page : "+repr(unePage)
                        unEnregistrement = listeEnregistrement[pageNum]
                        for unTag in unItem['patterns'].keys():
                            if type(unItem['patterns'][unTag]).__name__==type(re.compile("foo")).__name__:
                                reFound = re.search(unItem['patterns'][unTag], unePage)
                                if reFound != None:
                                    unEnregistrement[unTag] = reFound.group(1)
                                else:
                                    unEnregistrement[unTag] = None
                            else:
                                texte = unItem['patterns'][unTag]
                                for option in self.listeOptions.values():
                                    texte = texte.replace("%"+option['nom']+"%", str(self.getOption(option['nom'])))
                                unEnregistrement[unTag] = texte

            # On ajoute enfin la liste des fichiers à télécharger
            nbLiens = self.ajouteFichiers(emission, listeEnregistrement, chaineActuelle)

    def listerFichiers(self, emission):
        for chaineActuelle in [self.configArteLiveWeb, self.configArtePlusSept]:
            if (self.derniereChaine == chaineActuelle['nom']):
                self.listerEnregistrements (emission, chaineActuelle)
