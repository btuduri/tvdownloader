#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import cPickle as pickle
import sqlite3 as sqlite

import Constantes
import Fichier

import logging
logger = logging.getLogger( __name__ )

##########
# Classe #
##########

class PluginCache( object ):
	
	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( PluginCache, self ).__new__( self )
		return self.instance
	
	def __init__( self ):
		self.connexion              = sqlite.connect( Constantes.FICHIER_CACHE )
		self.connexion.text_factory = str
		self.curseur                = self.connexion.cursor()
		# Nettoyage
		self.clear()
	
	def __del__( self ):
		self.curseur.close()
		self.connexion.close()
	
	def creerTables( self ):
		self.curseur.execute( "CREATE TABLE IF NOT EXISTS plugins   ( id INTEGER PRIMARY KEY, nom TEXT );" )
		self.curseur.execute( "CREATE TABLE IF NOT EXISTS chaines   ( id INTEGER PRIMARY KEY, nom TEXT, idPlugin INTEGER, FOREIGN KEY( idPlugin ) REFERENCES plugins( id ) );" )
		self.curseur.execute( "CREATE TABLE IF NOT EXISTS emissions ( id INTEGER PRIMARY KEY, nom TEXT, idChaine INTEGER, FOREIGN KEY( idChaine ) REFERENCES chaines( id ) );" )
		self.curseur.execute( "CREATE TABLE IF NOT EXISTS fichiers  ( id INTEGER PRIMARY KEY, donnees BLOB, idEmission INTEGER, FOREIGN KEY( idEmission ) REFERENCES emissions( id ) );" )
		self.connexion.commit()
	
	def clear( self ):
		self.curseur.execute( "DROP TABLE IF EXISTS fichiers;" )
		self.curseur.execute( "DROP TABLE IF EXISTS emissions;" )
		self.curseur.execute( "DROP TABLE IF EXISTS chaines;" )
		self.curseur.execute( "DROP TABLE IF EXISTS plugins;" )
		self.creerTables()
		self.connexion.commit()
	
	# Met en forme dans une liste les retours de requete SQL
	# d'ou il n'est extrait qu'un element
	def miseEnFormeUnElement( self ):
		ret = []
		for res in self.curseur.fetchall():
			ret.append( res[ 0 ] )
		return ret			
		
	def listerPlugins( self ):
		self.curseur.execute( "SELECT nom FROM plugins;" )
		return self.miseEnFormeUnElement()

	def listerChaines( self, nomPlugin ):
		self.curseur.execute( "SELECT chaines.nom FROM chaines, plugins WHERE chaines.idPlugin = plugins.id AND plugins.nom = ?;", ( nomPlugin, ) )
		return self.miseEnFormeUnElement()

	def listerEmissions( self, nomChaine, nomPlugin ):
		self.curseur.execute( "SELECT emissions.nom FROM emissions, chaines, plugins WHERE emissions.idChaine = chaines.id AND chaines.nom = ? AND chaines.idPlugin = plugins.id AND plugins.nom = ?;", ( nomChaine, nomPlugin ) )
		return self.miseEnFormeUnElement()
	
	def listerFichiers( self, nomEmission, nomChaine, nomPlugin ):
		self.curseur.execute( "SELECT fichiers.donnees FROM fichiers, emissions, chaines, plugins WHERE fichiers.idEmission = emissions.id AND emissions.nom = ? AND emissions.idChaine = chaines.id AND chaines.nom = ? AND chaines.idPlugin = plugins.id AND plugins.nom = ?;", ( nomEmission, nomChaine, nomPlugin ) )
		ret = []
		for res in self.curseur.fetchall():
			ret.append( pickle.loads( res[ 0 ] ) )
		return ret
		
	def ajouterPlugin( self, nom ):
		self.curseur.execute( "INSERT INTO plugins ( nom ) VALUES ( ? );", ( nom, ) )
		self.connexion.commit()
		
	def ajouterChaine( self, nom, nomPlugin ):
		self.curseur.execute( "INSERT INTO chaines ( nom, idPlugin ) VALUES ( ?, ( SELECT id FROM plugins WHERE nom = ? ) );", ( nom, nomPlugin ) )
		self.connexion.commit()
		
	def ajouterEmission( self, nom, nomChaine, nomPlugin ):
		self.curseur.execute( "INSERT INTO emissions ( nom, idChaine ) VALUES ( ?, ( SELECT chaines.id FROM chaines, plugins WHERE chaines.idPlugin = plugins.id AND chaines.nom = ? AND plugins.nom = ? ) );", ( nom, nomChaine, nomPlugin ) )
		self.connexion.commit()

	def ajouterFichier( self, donnees, nomEmission, nomChaine, nomPlugin ):
		self.curseur.execute( "INSERT INTO fichiers ( donnees, idEmission ) VALUES ( ?, ( SELECT emissions.id FROM emissions, chaines, plugins WHERE emissions.idChaine = chaines.id AND emissions.nom = ? AND chaines.idPlugin = plugins.id AND chaines.nom = ? AND plugins.nom = ? ) );", ( pickle.dumps( donnees ), nomEmission, nomChaine, nomPlugin ) )
		self.connexion.commit()
