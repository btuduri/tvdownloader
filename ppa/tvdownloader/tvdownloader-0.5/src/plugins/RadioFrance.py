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

import re
import os

from Fichier import Fichier
from Plugin import Plugin

##########
# Classe #
##########

class RadioFrance( Plugin ):
	
	listeEmissionsFranceInter = { u"Allo la planète" : "http://radiofrance-podcast.net/podcast09/rss_10121.xml",
								u"Au detour du monde" : "http://radiofrance-podcast.net/podcast09/rss_10039.xml",
								u"Bons baisers de Manault" : "http://radiofrance-podcast.net/podcast09/rss_11160.xml",
								u"Carnet de campagne" : "http://radiofrance-podcast.net/podcast09/rss_10205.xml",
								u"carrefour de l'Eco" : "http://radiofrance-podcast.net/podcast09/rss_11292.xml",
								u"C'est demain la veille" : "http://radiofrance-podcast.net/podcast09/rss_11264.xml",
								u"CO2 mon Amour" : "http://radiofrance-podcast.net/podcast09/rss_10006.xml",
								u"Comme on nous parle" : "http://radiofrance-podcast.net/podcast09/rss_11242.xml",
								u"Daniel Morin" : "http://radiofrance-podcast.net/podcast09/rss_10906.xml",
								u"Didier Porte" : "http://radiofrance-podcast.net/podcast09/rss_10907.xml",
								u"ECLECTIK (dimanche)" : "http://radiofrance-podcast.net/podcast09/rss_10946.xml",
								u"Eclectik (samedi)" : "http://radiofrance-podcast.net/podcast09/rss_17621.xml",
								u"Esprit critique" : "http://radiofrance-podcast.net/podcast09/rss_10240.xml",
								u"Et pourtant elle tourne" : "http://radiofrance-podcast.net/podcast09/rss_10269.xml",
								u"Histoire de..." : "http://radiofrance-podcast.net/podcast09/rss_10919.xml",
								u"LA BAS, SI J'Y SUIS" : "http://radiofrance-podcast.net/podcast09/rss_14288.xml",
								u"La cellule de dégrisement" : "http://radiofrance-podcast.net/podcast09/rss_11259.xml",
								u"la chronique anglaise de David LOWE" : "http://radiofrance-podcast.net/podcast09/rss_11345.xml",
								u"La chronique de régis Mailhot" : "http://radiofrance-podcast.net/podcast09/rss_11335.xml",
								u"La chronique de Vincent Roca" : "http://radiofrance-podcast.net/podcast09/rss_11336.xml",
								u"La librairie francophone" : "http://radiofrance-podcast.net/podcast09/rss_18647.xml",
								u"La nuit comme si" : "http://radiofrance-podcast.net/podcast09/rss_11254.xml",
								u"La presse étrangère" : "http://radiofrance-podcast.net/podcast09/rss_11331.xml",
								u"Le Cinq Six Trente" : "http://radiofrance-podcast.net/podcast09/rss_10915.xml",
								u"L'économie autrement" : "http://radiofrance-podcast.net/podcast09/rss_11081.xml",
								u"Le débat économique" : "http://radiofrance-podcast.net/podcast09/rss_18783.xml",
								u"Le jeu des mille euros" : "http://radiofrance-podcast.net/podcast09/rss_10206.xml",
								u"Le journal de l'économie" : "http://radiofrance-podcast.net/podcast09/rss_10980.xml",
								u"le sept neuf du dimanche" : "http://radiofrance-podcast.net/podcast09/rss_10982.xml",
								u"le sept neuf du samedi" : "http://radiofrance-podcast.net/podcast09/rss_10981.xml",
								u"Les grandes nuits et les petits ..." : "http://radiofrance-podcast.net/podcast09/rss_11257.xml",
								u"Les savanturiers" : "http://radiofrance-podcast.net/podcast09/rss_10908.xml",
								u"Le Zapping de France Inter" : "http://radiofrance-podcast.net/podcast09/rss_10309.xml",
								u"L'humeur de Didier Porte" : "http://radiofrance-podcast.net/podcast09/rss_11078.xml",
								u"L'humeur de François Morel" : "http://radiofrance-podcast.net/podcast09/rss_11079.xml",
								u"L'humeur de Stéphane Guillon" : "http://radiofrance-podcast.net/podcast09/rss_10692.xml",
								u"L'humeur vagabonde" : "http://radiofrance-podcast.net/podcast09/rss_10054.xml",
								u"Noctiluque" : "http://radiofrance-podcast.net/podcast09/rss_10208.xml",
								u"Nocturne" : "http://radiofrance-podcast.net/podcast09/rss_10268.xml",
								u"Nonobstant" : "http://radiofrance-podcast.net/podcast09/rss_10615.xml",
								u"Nous autres" : "http://radiofrance-podcast.net/podcast09/rss_18633.xml",
								u"Panique au Mangin palace" : "http://radiofrance-podcast.net/podcast09/rss_10128.xml",
								u"panique au ministère psychique" : "http://radiofrance-podcast.net/podcast09/rss_10905.xml",
								u"Parking de nuit" : "http://radiofrance-podcast.net/podcast09/rss_10136.xml",
								u"Périphéries" : "http://radiofrance-podcast.net/podcast09/rss_10040.xml",
								u"Service public" : "http://radiofrance-podcast.net/podcast09/rss_10207.xml",
								u"Sous les étoiles exactement" : "http://radiofrance-podcast.net/podcast09/rss_10218.xml",
								u"Studio théatre" : "http://radiofrance-podcast.net/podcast09/rss_10629.xml",
								u"Système disque" : "http://radiofrance-podcast.net/podcast09/rss_10093.xml",
								u"Un jour sur la toile" : "http://radiofrance-podcast.net/podcast09/rss_10274.xml",
								u"Un livre sous le bras" : "http://radiofrance-podcast.net/podcast09/rss_10664.xml" }
	
	listeEmissionsFranceInfo = { u"Il était une mauvaise foi" : "http://radiofrance-podcast.net/podcast09/rss_10951.xml",
								u"La vie et vous, Le chemin de l'école" : "http://radiofrance-podcast.net/podcast09/rss_11077.xml",
								u"Le bruit du net" : "http://radiofrance-podcast.net/podcast09/rss_11064.xml",
								u"Le droit d'info" : "http://radiofrance-podcast.net/podcast09/rss_10986.xml",
								u"Le sens de l'info" : "http://radiofrance-podcast.net/podcast09/rss_10586.xml",
								u"Question d'argent" : "http://radiofrance-podcast.net/podcast09/rss_10556.xml",
								u"Tout comprendre" : "http://radiofrance-podcast.net/podcast09/rss_11313.xml",
								u"Tout et son contraire" : "http://radiofrance-podcast.net/podcast09/rss_11171.xml" }
	
	listeEmissionsFranceBleu = { u"1999" : "http://radiofrance-podcast.net/podcast09/rss_11325.xml",
								u"C'est bon à savoir" : "http://radiofrance-podcast.net/podcast09/rss_10337.xml",
								u"Chanson d'Aqui" : "http://radiofrance-podcast.net/podcast09/rss_11298.xml",
								u"Club Foot Marseille" : "http://radiofrance-podcast.net/podcast09/rss_11201.xml",
								u"Côté Mer" : "http://radiofrance-podcast.net/podcast09/rss_10890.xml",
								u"France Bleu Midi " : "http://radiofrance-podcast.net/podcast09/rss_11204.xml",
								u"Histoire en Bretagne" : "http://radiofrance-podcast.net/podcast09/rss_10638.xml",
								u"La science en question" : "http://radiofrance-podcast.net/podcast09/rss_10336.xml",
								u"Les défis du Professeur Gersal" : "http://radiofrance-podcast.net/podcast09/rss_11263.xml",
								u"Les Français parlent aux Français" : "http://radiofrance-podcast.net/podcast09/rss_11351.xml",
								u"Les nouvelles archives de l étrange" : "http://radiofrance-podcast.net/podcast09/rss_11265.xml",
								u"L'horoscope" : "http://radiofrance-podcast.net/podcast09/rss_10020.xml",
								u"L'humeur de Fred Ballard" : "http://radiofrance-podcast.net/podcast09/rss_11317.xml",
								u"Ligne d'expert" : "http://radiofrance-podcast.net/podcast09/rss_11023.xml",
								u"On repeint la musique" : "http://radiofrance-podcast.net/podcast09/rss_11268.xml",
								u"Planète Bleu" : "http://radiofrance-podcast.net/podcast09/rss_11031.xml",
								u"Sul gouel ha bembez..." : "http://radiofrance-podcast.net/podcast09/rss_10312.xml",
								u"Tour de France 2010" : "http://radiofrance-podcast.net/podcast09/rss_11355.xml" }
	
	listeEmissionsFranceCulture = { u"Affinités électives" : "http://radiofrance-podcast.net/podcast09/rss_10346.xml",
									u"A plus d'un titre" : "http://radiofrance-podcast.net/podcast09/rss_10466.xml",
									u"avec ou sans rdv" : "http://radiofrance-podcast.net/podcast09/rss_10180.xml",
									u"A voix nue" : "http://radiofrance-podcast.net/podcast09/rss_10351.xml",
									u"Ca rime à quoi" : "http://radiofrance-podcast.net/podcast09/rss_10897.xml",
									u"Carnet Nomade" : "http://radiofrance-podcast.net/podcast09/rss_10237.xml",
									u"Caroline FOUREST" : "http://radiofrance-podcast.net/podcast09/rss_10725.xml",
									u"Chanson boum" : "http://radiofrance-podcast.net/podcast09/rss_10975.xml",
									u"Chronique de Caroline Eliacheff" : "http://radiofrance-podcast.net/podcast09/rss_10477.xml",
									u"Chronique de Cécile Ladjali" : "http://radiofrance-podcast.net/podcast09/rss_11270.xml",
									u"Chronique de Clémentine Autain" : "http://radiofrance-podcast.net/podcast09/rss_10714.xml",
									u"CONCORDANCE DES TEMPS" : "http://radiofrance-podcast.net/podcast09/rss_16278.xml",
									u"Conférences de Michel Onfray" : "http://radiofrance-podcast.net/podcast09/rss_11141.xml",
									u"Continent sciences" : "http://radiofrance-podcast.net/podcast09/rss_16256.xml",
									u"Controverses du progrès (les)" : "http://radiofrance-podcast.net/podcast09/rss_11055.xml",
									u"Cultures D'Islam" : "http://radiofrance-podcast.net/podcast09/rss_10073.xml",
									u"Des histoires à ma façon" : "http://radiofrance-podcast.net/podcast09/rss_11181.xml",
									u"Des papous dans la tête" : "http://radiofrance-podcast.net/podcast09/rss_13364.xml",
									u"Divers aspects de la pensée (...)" : "http://radiofrance-podcast.net/podcast09/rss_10344.xml",
									u"Du grain à moudre" : "http://radiofrance-podcast.net/podcast09/rss_10175.xml",
									u"Du jour au Lendemain" : "http://radiofrance-podcast.net/podcast09/rss_10080.xml",
									u"En toute franchise" : "http://radiofrance-podcast.net/podcast09/rss_10898.xml",
									u"'EPOPEE DE LA FRANCE LIBRE" : "http://radiofrance-podcast.net/podcast09/rss_11365.xml",
									u"Foi et tradition" : "http://radiofrance-podcast.net/podcast09/rss_10492.xml",
									u"For interieur" : "http://radiofrance-podcast.net/podcast09/rss_10266.xml",
									u"HORS" : "http://radiofrance-podcast.net/podcast09/rss_11189.xml",
									u"Jeux d'épreuves" : "http://radiofrance-podcast.net/podcast09/rss_10083.xml",
									u"La chronique d'Alexandre Adler" : "http://radiofrance-podcast.net/podcast09/rss_18810.xml",
									u"La chronique de d'Alain" : "http://radiofrance-podcast.net/podcast09/rss_18809.xml",
									u"La chronique d'Olivier Duhamel" : "http://radiofrance-podcast.net/podcast09/rss_18811.xml",
									u"LA FABRIQUE DE L'HUMAIN" : "http://radiofrance-podcast.net/podcast09/rss_11188.xml",
									u"LA MARCHE DES SCIENCES" : "http://radiofrance-podcast.net/podcast09/rss_11193.xml",
									u"La messe" : "http://radiofrance-podcast.net/podcast09/rss_10272.xml",
									u"La nelle fabrique de l'histoire" : "http://radiofrance-podcast.net/podcast09/rss_10076.xml",
									u"La rumeur du monde" : "http://radiofrance-podcast.net/podcast09/rss_10234.xml",
									u"LA SUITE DANS LES IDEES" : "http://radiofrance-podcast.net/podcast09/rss_16260.xml",
									u"L'ATELIER LITTERAIRE" : "http://radiofrance-podcast.net/podcast09/rss_11185.xml",
									u"LA VIGNETTE" : "http://radiofrance-podcast.net/podcast09/rss_11199.xml",
									u"Le bien commun" : "http://radiofrance-podcast.net/podcast09/rss_16279.xml",
									u"L'économie en question o" : "http://radiofrance-podcast.net/podcast09/rss_10081.xml",
									u"Le journal de 12h30" : "http://radiofrance-podcast.net/podcast09/rss_10059.xml",
									u"Le journal de 18h" : "http://radiofrance-podcast.net/podcast09/rss_10060.xml",
									u"Le journal de 22h" : "http://radiofrance-podcast.net/podcast09/rss_10061.xml",
									u"Le journal de 7h" : "http://radiofrance-podcast.net/podcast09/rss_10055.xml",
									u"Le journal de 8h" : "http://radiofrance-podcast.net/podcast09/rss_10057.xml",
									u"Le magazine de la rédaction" : "http://radiofrance-podcast.net/podcast09/rss_10084.xml",
									u"LE MARDI DES AUTEURS" : "http://radiofrance-podcast.net/podcast09/rss_11194.xml",
									u"Le portrait du jour par Marc Krav" : "http://radiofrance-podcast.net/podcast09/rss_18812.xml",
									u"Le regard d'Albert Jacquard" : "http://radiofrance-podcast.net/podcast09/rss_16496.xml",
									u"Le rendez" : "http://radiofrance-podcast.net/podcast09/rss_10082.xml",
									u"Le salon noir" : "http://radiofrance-podcast.net/podcast09/rss_10267.xml",
									u"Les ateliers de création radio." : "http://radiofrance-podcast.net/podcast09/rss_10185.xml",
									u"Les enjeux internationaux" : "http://radiofrance-podcast.net/podcast09/rss_13305.xml",
									u"LES JEUDIS DE L'EXPO" : "http://radiofrance-podcast.net/podcast09/rss_11196.xml",
									u"Les lundis de l'histoire" : "http://radiofrance-podcast.net/podcast09/rss_10193.xml",
									u"Les matins de France Culture" : "http://radiofrance-podcast.net/podcast09/rss_10075.xml",
									u"LES MERCREDIS DU THEATRE" : "http://radiofrance-podcast.net/podcast09/rss_11195.xml",
									u"Les nv chemins de la connaissance" : "http://radiofrance-podcast.net/podcast09/rss_10467.xml",
									u"LES PASSAGERS DE LA NUIT" : "http://radiofrance-podcast.net/podcast09/rss_11190.xml",
									u"Les Pieds sur Terre" : "http://radiofrance-podcast.net/podcast09/rss_10078.xml",
									u"L'esprit public" : "http://radiofrance-podcast.net/podcast09/rss_16119.xml",
									u"LES RACINES DU CIEL" : "http://radiofrance-podcast.net/podcast09/rss_11200.xml",
									u"LES RETOURS DU DIMANCHE" : "http://radiofrance-podcast.net/podcast09/rss_11186.xml",
									u"LES VENDREDIS DE LA MUSIQUE" : "http://radiofrance-podcast.net/podcast09/rss_11197.xml",
									u"L'oeil du larynx" : "http://radiofrance-podcast.net/podcast09/rss_10311.xml",
									u"MACADAM PHILO" : "http://radiofrance-podcast.net/podcast09/rss_11198.xml",
									u"Maison d'études" : "http://radiofrance-podcast.net/podcast09/rss_10182.xml",
									u"Masse critique" : "http://radiofrance-podcast.net/podcast09/rss_10183.xml",
									u"Mauvais Genres" : "http://radiofrance-podcast.net/podcast09/rss_10070.xml",
									u"MEGAHERTZ" : "http://radiofrance-podcast.net/podcast09/rss_11182.xml",
									u"METROPOLITAINS" : "http://radiofrance-podcast.net/podcast09/rss_16255.xml",
									u"Orthodoxie" : "http://radiofrance-podcast.net/podcast09/rss_10491.xml",
									u"Place de la toile" : "http://radiofrance-podcast.net/podcast09/rss_10465.xml",
									u"PLACE DES PEUPLES" : "http://radiofrance-podcast.net/podcast09/rss_11207.xml",
									u"Planète terre" : "http://radiofrance-podcast.net/podcast09/rss_10233.xml",
									u"POST FRONTIERE" : "http://radiofrance-podcast.net/podcast09/rss_11191.xml",
									u"Projection privée" : "http://radiofrance-podcast.net/podcast09/rss_10198.xml",
									u"Question d'éthique" : "http://radiofrance-podcast.net/podcast09/rss_10201.xml",
									u"RADIO LIBRE" : "http://radiofrance-podcast.net/podcast09/rss_11183.xml",
									u"Répliques" : "http://radiofrance-podcast.net/podcast09/rss_13397.xml",
									u"Revue de presse internationale" : "http://radiofrance-podcast.net/podcast09/rss_10901.xml",
									u"RUE DES ECOLES" : "http://radiofrance-podcast.net/podcast09/rss_11192.xml",
									u"Science publique" : "http://radiofrance-podcast.net/podcast09/rss_10192.xml",
									u"Service protestant" : "http://radiofrance-podcast.net/podcast09/rss_10297.xml",
									u"Sur les docks" : "http://radiofrance-podcast.net/podcast09/rss_10177.xml",
									u"Terre à terre" : "http://radiofrance-podcast.net/podcast09/rss_10867.xml",
									u"TIRE TA LANGUE" : "http://radiofrance-podcast.net/podcast09/rss_11184.xml",
									u"Tout arrive" : "http://radiofrance-podcast.net/podcast09/rss_10077.xml",
									u"Tout un monde" : "http://radiofrance-podcast.net/podcast09/rss_10191.xml",
									u"Vivre sa ville" : "http://radiofrance-podcast.net/podcast09/rss_10878.xml" }
	
	listeEmissionsFranceMusique = { u"Histoire de..." : "http://radiofrance-podcast.net/podcast09/rss_10977.xml",
									u"Le mot musical du jour" : "http://radiofrance-podcast.net/podcast09/rss_10976.xml",
									u"Miniatures" : "http://radiofrance-podcast.net/podcast09/rss_10978.xml",
									u"Sonnez les matines" : "http://radiofrance-podcast.net/podcast09/rss_10979.xml" }
	
	listeEmissionsLeMouv = { u"Buzz de la semaine" : "http://radiofrance-podcast.net/podcast09/rss_10924.xml",
							u"Cette année là" : "http://radiofrance-podcast.net/podcast09/rss_11280.xml",
							u"Chez Francis" : "http://radiofrance-podcast.net/podcast09/rss_11285.xml",
							u"Compression de Cartier" : "http://radiofrance-podcast.net/podcast09/rss_11279.xml",
							u"Fausse Pub" : "http://radiofrance-podcast.net/podcast09/rss_11309.xml",
							u"La BD de Philippe Audoin" : "http://radiofrance-podcast.net/podcast09/rss_11278.xml",
							u"La minute culturelle de Cug et Westrou" : "http://radiofrance-podcast.net/podcast09/rss_10914.xml",
							u"La minute numérique" : "http://radiofrance-podcast.net/podcast09/rss_11277.xml",
							u"La mode de Samyjoe" : "http://radiofrance-podcast.net/podcast09/rss_11048.xml",
							u"La Revue de Presse" : "http://radiofrance-podcast.net/podcast09/rss_11281.xml",
							u"Le cinema de Jean Z" : "http://radiofrance-podcast.net/podcast09/rss_11045.xml",
							u"Le Comedy Club Live" : "http://radiofrance-podcast.net/podcast09/rss_11314.xml",
							u"Le meilleur du Mouv'" : "http://radiofrance-podcast.net/podcast09/rss_11274.xml",
							u"L'Environnement" : "http://radiofrance-podcast.net/podcast09/rss_11041.xml",
							u"Le pire de la semaine" : "http://radiofrance-podcast.net/podcast09/rss_11276.xml",
							u"Le Reportage de la Redaction" : "http://radiofrance-podcast.net/podcast09/rss_11311.xml",
							u"Les bons plans" : "http://radiofrance-podcast.net/podcast09/rss_11273.xml",
							u"Les lectures de Clementine" : "http://radiofrance-podcast.net/podcast09/rss_11051.xml",
							u"Les séries TV de Pierre Langlais" : "http://radiofrance-podcast.net/podcast09/rss_11288.xml",
							u"Le Top 3 d'Emilie" : "http://radiofrance-podcast.net/podcast09/rss_11287.xml",
							u"Le tour du Web" : "http://radiofrance-podcast.net/podcast09/rss_10926.xml",
							u"L'invité du Mouv'" : "http://radiofrance-podcast.net/podcast09/rss_11330.xml",
							u"L'invité matinal" : "http://radiofrance-podcast.net/podcast09/rss_11286.xml",
							u"Revue de Web" : "http://radiofrance-podcast.net/podcast09/rss_11310.xml",
							u"Un grand verre d'Orangeade" : "http://radiofrance-podcast.net/podcast09/rss_11282.xml",
							u"Un tir dans la lucarne" : "http://radiofrance-podcast.net/podcast09/rss_11289.xml",
							u"Zebra" : "http://radiofrance-podcast.net/podcast09/rss_11308.xml" }
	
	listeEmissions = { "France Inter"   : listeEmissionsFranceInter,
					   "France Info"    : listeEmissionsFranceInfo,
					   "France Bleu"    : listeEmissionsFranceBleu,
					   "France Culture" : listeEmissionsFranceCulture,
					   "France Musique" : listeEmissionsFranceMusique,
					   "Le Mouv'"       : listeEmissionsLeMouv }
	
	def __init__( self):
		Plugin.__init__( self, "Radio France", "http://www.radiofrance.fr/")
		
	def rafraichir( self ):
		pass # Rien a rafraichir ici...	   
	
	def listerChaines( self ):
		liste = self.listeEmissions.keys()
		liste.sort()
		for chaine in liste:
			self.ajouterChaine(chaine)

	def listerEmissions( self, chaine ):
		self.derniereChaine = chaine
		liste = []
		if( chaine != "" ):
			liste = self.listeEmissions[ chaine ].keys()
			liste.sort()
		for emission in liste:
			self.ajouterEmission(chaine, emission)
	
	def listerFichiers( self, emission ):
		if( emission != "" ):
			if( emission in self.listeEmissions[ self.derniereChaine ] ):
				# On recupere le lien de la page de l'emission
				lienPage = self.listeEmissions[ self.derniereChaine ][ emission ]
				# On recupere la page de l'emission
				page = self.API.getPage( lienPage )
				# On extrait les emissions
				resultats = re.findall( "podcast09/([^\"]*\.mp3)\"", page )
				for res in resultats:
					lien = "http://media.radiofrance-podcast.net/podcast09/" + res
					listeDates = re.findall( "\d{2}\.\d{2}\.\d{2}", res )
					if( listeDates == [] ): # Si on n'a pas pu extraire une date
						date = "Inconnue"
					else: # Si on a extrait une date
						date = listeDates[ 0 ]
					self.ajouterFichier(emission, Fichier( emission + " (" + date + ")", date, lien ) )
