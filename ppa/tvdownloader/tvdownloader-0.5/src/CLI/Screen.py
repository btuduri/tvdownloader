#/usr/bin/python
# -*- coding: utf-8 -*-
import os

#classe qui affiche la barre en haut de l'ecran
# @param self l'objet courant
# @param plugin le nom du plugin choisi
# @param chaine le nom de la chaine choisie
# @param program le nom du programme choisi
# @param program le nom du programme choisi ou de l'ecran d'option affiche
# @return Rien
def header(plugin,chaine,program):
	print ""
	#on efface l'affichage en cours
	os.system(['clear','cls'][os.name == 'nt'])
	#formatte le nom du plugin (entre 0 et 14 caracteres)
	if len(plugin)<7:plugin+="\t"
	#formatte le nom de la chaine (entre 0 et 14 caracteres)
	if len(chaine)<7:chaine+="\t"
	#formatte le nom du programme selon le nombre de caracteres
	#if len(program)==0:program+="\t\t\t\t    "
	if len(program)<7:program+="\t\t\t\t    "
	elif len(program)<14:program+="\t\t\t    "
	elif len(program)<21:program+="\t\t    "
	elif len(program)<28:program+="\t    "
	elif len(program)>32:
		program=program[:29]
		program+="..."
	#affiche la barre avec les parametres recus
	print " ##############################################################################"
	print " ##                           TVDownloader 0.4                               ##"
	print " ##                         Command-Line Interface                           ##"
	print " ##                                                                          ##"
	print " ##                                                                          ##"
	print " ##\t",plugin,"\t",chaine,"\t",program,"##"
	print " ##                                                                          ##"
	print " ##############################################################################"
	print ""

#classe qui affiche la barre de menu en bas de l'ecran, avant l'invite de saisie
# @param self l'objet courant
# @param Rien
# @return Rien
def footer():
        print "  q:quitter   p:preferences t:telechargements r:retour a:actualiser",

#classe qui affiche les plugins, avec defilement +/- si plus de 15 plugins
# @param self l'objet courant
# @param plugins la liste des plugins
# @param current le numero de defilement dans la liste (0 pour la premiere page, 1 pour la page suivantee, etc)
# @return Rien
def plugin(plugins,current):
	for i in range(10) :
		if i+10*current<len(plugins): print " ",i,":",plugins[i+10*current]
		else: print ""
	print "\n\n"
	if len(plugins)>10:print "  +:plugins suivants  -:plugins precedents (page",current+1,"/",len(plugins)/10+1,",",len(plugins),"plugins)"
	else:print""

#classe qui affiche les chaines, avec defilement +/- si plus de 15 chaines
# @param self l'objet courant
# @param chaines la liste des chaines
# @param current le numero de defilement dans la liste (0 pour la premiere page, 1 pour la page suivantee, etc)
# @return Rien
def chaine(chaines,current):
	for i in range(10) :
		if i+10*current<len(chaines): print " ",i,":",chaines[i+10*current]
		else: print ""
	print "\n\n"
	if len(chaines)>10:print "  +:chaines suivantes  -:chaines precedentes (page",current+1,"/",len(chaines)/10+1,",",len(chaines),"chaines)"
	else:print""

#classe qui affiche les programmes, avec defilement +/- si plus de 15 programmes
# @param self l'objet courant
# @param programs la liste des programmes
# @param current le numero de defilement dans la liste (0 pour la premiere page, 1 pour la page suivantee, etc)
# @return Rien
def program(programs,current):
	for i in range(10) :
		if i+10*current<len(programs): print " ",i,":",programs[i+10*current]
		else: print ""
	print "\n\n"
	if len(programs)>10:print "  +:programmes suivants  -:programmes precedents (page",current+1,"/",len(programs)/10+1,",",len(programs),"programmes)"
	else:print""

#classe qui affiche les fichiers, avec defilement +/- si plus de 15 fichiers
# @param self l'objet courant
# @param fichiers la liste des fichiers
# @param current le numero de defilement dans la liste (0 pour la premiere page, 1 pour la page suivantee, etc)
# @return Rien
def fichier(fichiers,current):
	for i in range(10) :			
		if i+10*current<len(fichiers):
			if len(fichiers[i+10*current].nom)>74:print " ",i,":",fichiers[i+10*current].nom[:71]+"..."
			elif len(fichiers[i+10*current].nom)<=74: print " ",i,":",fichiers[i+10*current].nom
		else: print ""
	print "\n\n"
	if len(fichiers)>10:print "  +:fichiers suivants  -:fichiers precedents (page",current+1,"/",len(fichiers)/10+1,",",len(fichiers),"fichiers)"
	else:print""
	print "  *:tous ",
