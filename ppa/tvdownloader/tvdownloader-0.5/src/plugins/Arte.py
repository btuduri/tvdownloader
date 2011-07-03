#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier LICENSE #
#########################################

#~ Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
#~ Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
#~ Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########

import os

from Plugin import Plugin
from Fichier import Fichier
from urllib import quote,unquote
import re,unicodedata
import time,rfc822 # for RFC822 datetime format (rss feed)
from htmlentitydefs import name2codepoint

##########
# Classe #
##########

class Arte( Plugin ):
    """Classe abstraite Plugin dont doit heriter chacun des plugins"""

    ##
    ## Arte Live Web
    ##
    
    #
    # A/ Recherche des émissions
    #
    # 1. On liste les catégories à partir de la page d'accueil.
    #    Chaque catégorie est une "émission" de la chaine Arte Live Web
    #
    # B/ Recherche des fichiers d'une émission
    #
    # 1. On recherche la page du flux RSS à partir de la page de la catégorie choisie.
    # 2. On extrait la liste des fichiers (les pages de chaque enregistrement proposé)
    # 3. On recherche le numéro eventID à partir de la page de l'enregistrement
    # 4. On recherche les détails de l'enregistrement dans la page xml associée à l'eventID
    #

    ##
    ## Arte+7
    ##
    ## Utilisation de la méthode de Pascal92
    ## http://www.encodage.org/phpBB/viewtopic.php?f=26&t=90
    ##
    
    #
    # A/ Recherche des émissions
    #
    # 1. On liste les chaines à partir de la page d'accueil.
    #    Chaque chaine est une "émission" de la chaine Arte+7
    #
    # B/ Recherche des fichiers d'une émission
    #
    # 1. On charge la page spéciale "videoArtePlusSeptChaineBaseUrl" contenant les fichiers de la chaine choisie
    # 2. On extrait la liste des fichiers (les pages ainsi que nom et date de chaque enregistrement proposé)
    # 3. On recherche le numéro de référence de la vidéo à partir de la page de l'enregistrement
    # 4. On recherche les détails de l'enregistrement dans la page xml associée à la référence
    #
    
    ##
    ## Arte Live Web
    ##
    nomArteLiveWeb = "Arte Live Web"
    # Page permettant de lister les catégories
    listeArteLiveWebCategoriesUrl = "http://liveweb.arte.tv/"
    # Expression régulière pour extraire les catégories
    listeArteLiveWebCategoriesPattern = re.compile("<a href=\"http://liveweb.arte.tv/fr/cat/(.*?)\">(.*?)</a>", re.DOTALL)
    # Rang dans le résultat de l'expression régulière précédente
    categorieArteLiveWeb_LIEN = 0
    categorieArteLiveWeb_NOM = 1
    # Base de la page catégorie, permettant de retrouver le lien du flux RSS
    videoArteLiveWebCategorieBaseUrl = "http://liveweb.arte.tv/fr/cat/"
    # Expression régulière pour extraire le lien du flux RSS
    videoArteLiveWebRSSPattern = re.compile("<a href=\"(http://download.liveweb.arte.tv/o21/liveweb/rss/home.*?\.rss)\"", re.DOTALL)

    # Expression régulière pour extraire le lien vers la page de la video, ainsi que sa date
    videoArteLiveWebVideosPattern = re.compile("<link>(http://liveweb.arte.tv/fr/video/.*?)</link>.*?<pubDate>(.*?)</pubDate>", re.DOTALL)
    #~ videoArteLiveWebEventIDPattern = re.compile("eventID=(.*?)&")
    #~ videoArteLiveWebEventIDPattern = re.compile("new LwEvent('(.*?)', '');")
    videoArteLiveWebEventIDPattern = re.compile("/media/event/(.*?)/", re.DOTALL)
    videoArteLiveWebInfosBaseUrl = "http://arte.vo.llnwd.net/o21/liveweb/events/event-" # ".xml"
    
    videoArteLiveWebTitrePattern = re.compile("<nameFr>(.*?)</nameFr>", re.DOTALL)
    videoArteLiveWebLienPatternHD = re.compile("<urlHd>(.*?)</urlHd>", re.DOTALL)
    videoArteLiveWebLienPatternSD = re.compile("<urlSd>(.*?)</urlSd>", re.DOTALL)
    #~ videoArteLiveWebDatePattern = re.compile("<dateEvent>(.*?)</dateEvent>", re.DOTALL)
    
    ##
    ## Arte+7
    ##
    nomArtePlusSept = "Arte+7"
    # Page permettant de lister les chaines
    listeArtePlusSeptChainesUrl = "http://videos.arte.tv/fr/videos/arte7"
    # Expression régulière pour extraire les chaines
    listeArtePlusSeptChainesPattern = re.compile("<a href=\"/fr/videos/chaines/(.*?)\".*?>(.*?)</a>", re.DOTALL)
    # Rang dans le résultat de l'expression régulière précédente
    categorieArtePlusSept_LIEN = 0
    categorieArtePlusSept_NOM = 1
    # Expression régulière pour extraire le channelID du lien de la chaine
    chaineArtePlusSeptChannelIDPattern = re.compile(".*?/index-(.*?)\.html", re.DOTALL)
    # Base de la page chaine, permettant de retrouver les fichiers (lien donné par "listViewUrl" dans la page principale)
    videoArtePlusSeptChaineBaseUrl = "http://videos.arte.tv/fr/do_delegate/videos/arte7/index-3211552,view,asList.html?hash=fr/list/date//1/250/channel-%channel%-program-"

    # Expression régulière pour extraire le lien vers la page de la video, son titre ainsi que sa date
    videoArtePlusSeptVideosPattern = re.compile("<a href=\"(/fr/videos/.*?\.html)\"><span class=\"teaserTitle\">(.*?)</span></a>.*?<td class=\"col2\"><em>(.*?)</em></td>", re.DOTALL)
    # Base de la page permettant de rechercher la référence de la video
    videoArtePlusSeptVideoBaseUrl = "http://videos.arte.tv"
    # Expression régulière pour extraire la référence de la vidéo à lire
    videoArtePlusSeptVideoRefPattern = re.compile("addToPlaylistOpen {ajaxUrl:'/fr/do_addToPlaylist/videos/.*?-(.*?)\.html'}", re.DOTALL)
    videoArtePlusSeptPlayerPattern = re.compile("<param name=\"movie\" value=\"(.*?\.swf)", re.DOTALL)
    # Base de la page XML décrivant la vidéo, ses liens
    videoArtePlusSeptXMLBaseURL = "http://videos.arte.tv/fr/do_delegate/videos/360_geo-%video%,view,asPlayerXml.xml"
    videoArtePlusSeptLienPatternHD = re.compile("<url quality=\"hd\">(.*?)</url>", re.DOTALL)
    videoArtePlusSeptLienPatternSD = re.compile("<url quality=\"sd\">(.*?)</url>", re.DOTALL)

    # Ordre des éléments dans le tuple "chaine"
    chaine_NOM = 1
    chaine_LIEN = 0
    
    nom = "Arte"
    url = "http://www.arte.tv/"
    
    def __init__( self ):
        Plugin.__init__(self, self.nom, self.url)
        #~ Plugin.__init__(self)
    
        self.listeChaines = {}
        self.listeFichiers = {}
        
        if os.path.exists( self.fichierCache ):
                self.listeChaines = self.chargerCache()

    def htmlentitydecode(self, s):
        # http://wiki.python.org/moin/EscapingHtml
        return re.sub('&(%s);' % '|'.join(name2codepoint), 
                lambda m: unichr(name2codepoint[m.group(1)]), s)

    def listerOptions(self):
        # Qualité à rechercher SD ou HD ?
        self.optionChoixUnique("qualite", "Qualité des vidéos", "HD", ["HD", "SD"])
        # Nombre maximum de fichiers à rechercher (0 = aucune limite)
        self.optionTexte("maxdepth", "Nombre d'enregistrementrs à rechercher (0=pas de limite)", 0)
        # Renommer les fichiers à partir du titre de l'émission
        self.optionBouleen("rename", "Renommer les fichiers à partir du titre de l'émission (attention, plusieurs enregistrements peuvent avoir le même nom)", False)

    def rafraichir( self ):
        self.afficher("Création de la liste des chaines...")

        ##
        ## Arte Live Web
        ##
        self.afficher("Récupération de la liste des catégories "+self.nomArteLiveWeb+"...")
        # On crée la chaine
        self.listeChaines[self.nomArteLiveWeb] = []
        # On recherche toutes les catégories
        for item in re.findall(self.listeArteLiveWebCategoriesPattern, self.API.getPage(self.listeArteLiveWebCategoriesUrl)):
            lien = item[self.categorieArteLiveWeb_LIEN]
            nom = item[self.categorieArteLiveWeb_NOM]
            #~ nom = unicode(nom, "iso-8859-1", "replace")
            itemLive = []
            itemLive.insert (self.chaine_LIEN, lien)
            itemLive.insert (self.chaine_NOM, nom)
            # On ajoute la catégorie trouvée si elle n'est pas déjà présente
            if (itemLive not in self.listeChaines[self.nomArteLiveWeb]):
                self.listeChaines[self.nomArteLiveWeb].append(itemLive)

        ##
        ## Arte+7
        ##
        self.afficher("Récupération de la liste des chaines "+self.nomArtePlusSept+"...")
        # On crée la chaine
        self.listeChaines[self.nomArtePlusSept] = []
        # On recherche toutes les catégories
        for item in re.findall(self.listeArtePlusSeptChainesPattern, self.API.getPage(self.listeArtePlusSeptChainesUrl)):
            lien = item[self.categorieArtePlusSept_LIEN]
            nom = item[self.categorieArtePlusSept_NOM]
            #~ nom = unicode(nom, "utf8", "replace")
            #~ nom = self.htmlentitydecode(nom)
            #~ nom = nom.encode("utf-8", "replace")
            itemPlusSept = []
            itemPlusSept.insert (self.chaine_LIEN, lien)
            itemPlusSept.insert (self.chaine_NOM, nom)
            # On ajoute la catégorie trouvée si elle n'est pas déjà présente
            if (itemPlusSept not in self.listeChaines[self.nomArtePlusSept]):
                self.listeChaines[self.nomArtePlusSept].append(itemPlusSept)

        self.sauvegarderCache(self.listeChaines)
    
    def getLienEmission(self, emission):
        #~ emission = unicode( emission, "utf8", "replace" )
        # Cherche dans quelle chaine se trouve l'émission
        #~ self.afficher("Recherche de : "+emission)
        #~ for chaine in self.listeChaines.keys():
        #~     #~ self.afficher("Chaine : "+chaine)
        chaine = self.derniereChaine
        for item in self.listeChaines[chaine]:
            s = item[self.chaine_NOM]
            #~ self.afficher("Item : "+s)
            if (cmp(s, emission)==0):
                s = item[self.chaine_LIEN]
                if (s==""):
                    return None
                else:
                    return quote(s.encode( 'ascii','ignore' ))
    
    def listerChaines( self ):
        t = self.listeChaines.keys()
        t.sort()
        for chaine in t:
            self.ajouterChaine(chaine)
    
    def listerEmissions( self, chaine ):
        t = []
        self.derniereChaine = chaine
        if self.listeChaines.has_key(chaine):
            for item in self.listeChaines[chaine]:
                s = item[self.chaine_NOM]
                #~ t.append(s.decode("iso-8859-1"))
                t.append(s)
            t.sort()
        for emission in t:
            self.ajouterEmission(chaine, emission)

    def listerFichiersArteLiveWeb( self, emission ):
        """Renvoi la liste des fichiers disponibles pour une emission donnnee"""
        # Renvoi la liste des fichiers (utilisation de la classe Fichier)
        #    [ Fichier ( nom, date, lien) , Fichier( ... ), ... ]
        if self.listeFichiers.has_key(emission):
            return self.listeFichiers[emission]
        
        lien = self.getLienEmission(emission)
        
        if lien == None:
            self.afficher ("Erreur de recherche du lien pour \""+emission+"\"")
        else:
            self.afficher("Récupération de la liste des fichiers pour \""+emission+"\"...")
            # Reconstitution du lien complet
            lien = self.videoArteLiveWebCategorieBaseUrl+lien
            # On recherche l'adresse de la page RSS
            self.afficher ("Recherche du flux RSS \""+emission+"\" à l'adresse "+lien)
            feedURL = re.search(self.videoArteLiveWebRSSPattern, self.API.getPage(lien)).group(1)

            # On recherche toutes les émissions contenues dans le flux RSS
            self.afficher ("Recherche des émissions dans le flux : "+feedURL)
            videos = re.findall(self.videoArteLiveWebVideosPattern, self.API.getPage(feedURL))

            liste = []
            if videos == None:
                return liste

            # Pour chacune des vidéos trouvées
            curDepth = 0
            for fichier in videos:
                #~ curDepth = curDepth+1
                curDepth += 1
                opt_maxDepth = int(self.getOption("maxdepth"))
                if (opt_maxDepth>0 and curDepth>opt_maxDepth):
                    break
                
                self.afficher ("Émission trouvée "+fichier[0])
                # Recherche de l'eventID dans la page de l'emission
                fichierInfosEventID_match = re.search (self.videoArteLiveWebEventIDPattern, self.API.getPage(fichier[0]))
                if fichierInfosEventID_match == None:
                    continue
                self.afficher ("... eventID : "+fichierInfosEventID_match.group(1))
                
                # Chargement de la page XML de l'eventID trouvé
                fichierInfos = self.API.getPage(self.videoArteLiveWebInfosBaseUrl+fichierInfosEventID_match.group(1)+".xml")

                titre = re.search(self.videoArteLiveWebTitrePattern, fichierInfos)
                if titre != None:
                    titre = titre.group(1)
                else:
                    curDepth -= 1 # On n'est pas tombé sur une vidéo valide (pas de titre trouvé ?!)
                    continue

                opt_qual = self.getOption("qualite")
                if opt_qual == "HD":
                    lien = re.search(self.videoArteLiveWebLienPatternHD, fichierInfos)
                else:
                    lien = re.search(self.videoArteLiveWebLienPatternSD, fichierInfos)

                if lien != None:
                    lien = lien.group(1)
                    
                    opt_rename = self.getOption("rename")
                    if opt_rename:
                        nomFichierSortie = titre.replace(" ","_")+".mp4"
                        nomFichierSortie = nomFichierSortie.replace(":","_")
                        nomFichierSortie = nomFichierSortie.replace("/","_")
                        nomFichierSortie = nomFichierSortie.replace("\\","_")
                        nomFichierSortie = nomFichierSortie.replace("?","_")
                    else:
                        nomFichierSortie = lien.split('/')[-1]
                else:
                    curDepth -= 1 # On n'est pas tombé sur une vidéo valide (pas de lien, vidéo Live à venir ??)
                    continue
                #~ date =  re.search(self.videoDatePattern, fichierInfos)
                date =  fichier[1]
                if date != None:
                    rfc_date = rfc822.parsedate(date)
                    # Format année/mois/jour, mieux pour effectuer un tri
                    date = str(rfc_date[0])+"/"+str(rfc_date[1]).zfill(2)+"/"+str(rfc_date[2]).zfill(2)
                else:
                    continue
                
                if not(lien):
                    continue
                
                self.afficher ("... Titre : "+titre)
                self.afficher ("... Date : "+date)
                self.afficher ("... Lien : "+lien)
                self.afficher ("... nomFichierSortie : "+nomFichierSortie)

                self.ajouterFichier(emission, Fichier( titre, date, lien, nomFichierSortie ) )
                liste.append(Fichier(titre, date, lien))
            self.afficher(str(len(liste))+" fichiers trouvés.")
            self.listeFichiers[emission] = liste
            #~ return liste

    def listerFichiersArtePlusSept( self, emission ):
        """Renvoi la liste des fichiers disponibles pour une emission donnnee"""
        # Renvoi la liste des fichiers (utilisation de la classe Fichier)
        #    [ Fichier ( nom, date, lien) , Fichier( ... ), ... ]
        if self.listeFichiers.has_key(emission):
            return self.listeFichiers[emission]
        
        # Code de la "chaine" Arte+7
        channel = re.search (self.chaineArtePlusSeptChannelIDPattern, self.getLienEmission(emission)).group(1)
        # Construction du lien contenant toutes les émissions de cette chaine
        lien = self.videoArtePlusSeptChaineBaseUrl.replace ("%channel%", channel)
        
        if lien == None:
            self.afficher ("Erreur de recherche du lien pour \""+emission+"\"")
        else:
            self.afficher("Récupération de la liste des fichiers pour \""+emission+"\"...")

            # On recherche toutes les émissions de la chaine
            self.afficher ("Recherche des émissions de la chaine \""+emission+"\" à l'adresse "+lien)
            videos = re.findall(self.videoArtePlusSeptVideosPattern, self.API.getPage(lien))

            liste = []
            if videos == None:
                return liste

            # Pour chacune des vidéos trouvées
            curDepth = 0
            for fichier in videos:
                #~ curDepth = curDepth+1
                curDepth += 1
                opt_maxDepth = self.getOption("maxdepth")
                if (opt_maxDepth>0 and curDepth>opt_maxDepth):
                    break
                
                self.afficher ("Émission trouvée "+fichier[0])
                
                fichierInfos = self.API.getPage(self.videoArtePlusSeptVideoBaseUrl+fichier[0])
                
                # Recherche de la référence de la vidéo dans la page de l'emission
                fichierInfosVideoRef_match = re.search (self.videoArtePlusSeptVideoRefPattern, fichierInfos)
                if fichierInfosVideoRef_match == None:
                    continue
                self.afficher ("... videoRef : "+fichierInfosVideoRef_match.group(1))

                # Recherche l'adresse du player video, pour la suite
                fichierInfosPlayer_match = re.search (self.videoArtePlusSeptPlayerPattern, fichierInfos)
                if fichierInfosPlayer_match == None:
                    continue
                self.afficher ("... Player : "+fichierInfosPlayer_match.group(1))
                
                #~ # Chargement de la page XML de la référence trouvée
                fichierInfos = self.API.getPage(self.videoArtePlusSeptXMLBaseURL.replace("%video%",fichierInfosVideoRef_match.group(1)))

                #~ file = open(self.fichierCache+"_web", "w")
                #~ file.write (fichierInfos)
                #~ file.close()

                titre = fichier[1]
                opt_qual = self.getOption("qualite")
                if opt_qual == "HD":
                    lien = re.search(self.videoArtePlusSeptLienPatternHD, fichierInfos)
                else:
                    lien = re.search(self.videoArtePlusSeptLienPatternSD, fichierInfos)
                
                if lien != None:
                    lien = lien.group(1)
                    
                    opt_rename = self.getOption("rename")
                    if opt_rename:
                        nomFichierSortie = titre.replace(" ","_")+".mp4"
                        nomFichierSortie = nomFichierSortie.replace(":","_")
                        nomFichierSortie = nomFichierSortie.replace("/","_")
                        nomFichierSortie = nomFichierSortie.replace("\\","_")
                        nomFichierSortie = nomFichierSortie.replace("?","_")
                    else:
                        nomFichierSortie = lien.split('/')[-1]
                        if nomFichierSortie.index('?')>0:
                            nomFichierSortie = nomFichierSortie.split('?')[0]
                        nomFichierSortie = nomFichierSortie+".mp4"
                    
                    #~ nomFichierSortie = titre.replace(" ","_").replace(":","_").replace("/","_")+".mp4"

                    #~ lien = lien.group(1)
                    # Workaround : on ajoute le nom du player directement ici
                    lien = lien+" -W "+fichierInfosPlayer_match.group(1)
                else:
                    continue
                date =  fichier[2]
                
                if not(lien):
                    continue
                
                self.afficher ("... Titre : "+titre)
                self.afficher ("... Date : "+date)
                self.afficher ("... Lien : "+lien)
                self.afficher ("... nomFichierSortie : "+nomFichierSortie)
                
                self.ajouterFichier(emission, Fichier( titre, date, lien, nomFichierSortie ) )
                liste.append(Fichier(titre, date, lien))
            self.afficher(str(len(liste))+" fichiers trouvés.")
            self.listeFichiers[emission] = liste
            #~ return liste

    
    def listerFichiers( self, emission ):
        if (self.derniereChaine == self.nomArteLiveWeb):
            #~ return self.listerFichiersArteLiveWeb (emission)
            self.listerFichiersArteLiveWeb (emission)
        elif (self.derniereChaine == self.nomArtePlusSept):
            #~ return self.listerFichiersArtePlusSept (emission)
            self.listerFichiersArtePlusSept (emission)
        else:
            self.afficher("Chaine non prise en compte actuellement")