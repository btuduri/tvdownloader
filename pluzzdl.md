#Petit tour d'horizon de pluzzdl (version 0.8).

# Introduction #

Le système de streaming de Pluzz ayant changé et TVDownloader étant toujours en refonte, un petit standalone a été fait pour permettre de récupérer les vidéos de Pluzz.
Il sera, plus tard, intégré à TVDownloader.

# Installation #

Pour faciliter le déploiement des mises à jour, pluzzdl a été ajouté au PPA de TVDownloader.

Il faut donc :
  * ajouter le PPA
```
sudo add-apt-repository ppa:chaoswizard/tvdownloader
```
  * mettre à jour la liste des paquets
```
sudo apt-get update
```
  * installer pluzzdl
```
sudo apt-get install pluzzdl
```

Le paquet sera alors mis à jour automatiquement avec votre système.

Il est également possible de récupérer les paquets deb via [FTP](http://ppa.launchpad.net/chaoswizard/tvdownloader/ubuntu/pool/main/p/pluzzdl/).
Le tar.gz contenant les sources est disponible dans la section Downloads.

# Utilisation #

Voir le man
```
man pluzzdl
```
ou le fichier manuel.pdf inclus dans l'archive.