#M6 Replay (mise à jour) 31/03/12 et W9 Replay (mise à jour) 01/05/12

# Introduction #

Les dernières modifications des sites de replay entrainent des modifications en profondeur de TVDownloader (modifications qui ne peuvent être faites via notre menu de mise à jour).
Comme une nouvelle version n'est pas encore prévu, il est possible, pour les impatients, de mettre à jour le logiciel "à la main".
Bien entendu, pendant toutes les étapes, prenez bien la peine **de lire tous les retours de votre terminal** pour être sur de ne pas faire une bêtise...

Avant de commencer, il va falloir :
  * mettre à jour TVDownloader en version 0.7.2 (si ce n'est pas déjà le cas)
  * mettre à jour les plugins existants
  * mettre à jour rtmpdump et de sa librairie librtmp0 en version 2.4

# Mise à jour des plugins #

Pour commencer, cela ne fait pas de mal, il faut mettre à jour les plugins via l'interface du logiciel : Edition -> Mise à jour des plugins.
Il suffit de renseigner l'URL suivante
```
http://tvdownloader.googlecode.com/hg/plugins
```
puis de cliquer sur le bouton pour rechercher des mises à jour puis sur celui pour les installer.

# Mise à jour de rtmpdump #

Il faut ensuite utiliser une version récente de rtmpdump (2.4).
Il est par exemple possible (pour Ubuntu) de récupérer une version de rtmpdump et de sa librairie librtmp0 à l'adresse suivante :
```
http://ppa.launchpad.net/team-xbmc/ppa/ubuntu/pool/main/r/rtmpdump/
```
ou en utilisant directement le PPA suivant :
```
ppa:team-xbmc/ppa
```

# Mise à jour de TVDownloader (manuelle) #

Il va falloir :
  * se placer dans le répertoire d'installation du logiciel :
```
   cd /usr/share/tvdownloader/
```
  * passer en root s'il faut les droits pour écrire dans le répertoire en question :
```
   sudo -s
```
  * télécharger les fichiers modifiés :
```
   wget -O Downloader.py http://tvdownloader.googlecode.com/hg/other/Stable/src/Downloader.py 
   wget -O plugins/M6Replay.py http://tvdownloader.googlecode.com/hg/other/Stable/src/plugins/M6Replay.py
   wget -O plugins/W9Replay.py http://tvdownloader.googlecode.com/hg/other/Stable/src/plugins/W9Replay.py
```
  * mettre à jour les fichiers pyc :
```
   python -c "import compileall ; compileall.compile_dir( '.' )"
```

Et c'est fini ! :)