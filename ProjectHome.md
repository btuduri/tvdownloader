This project uses Python and Qt to create a small software to download podcasts and videos from French websites.
It uses plugins to enlarge software possibilities.

TVDownloader est un projet qui a pour but de permettre le téléchargement de podcasts et d'émissions librement disponibles sur Internet.
On retrouvera, en autre, les podcasts de grands groupes radio comme Radio France ou télévisuel comme France Télévision.

Un système de plugin a été mis en place pour permettre à tous d'ajouter les sites qui l'intéresse (n'hésiter pas à nous envoyer vos plugins).

Ce logiciel est libre. Il est codé en Python et utilise PyQt.

<img src='http://uploads.imagup.com/14/1286109684.png' alt='http://uploads.imagup.com/14/1286109684.png' />


---


La dernière version sortie est la 0.7.

Il faut supprimer l'ancien fichier de configuration/cache si vous utilisez une version précédente de TVD :

```
rm -r .tvdownloader
```


---


## Pour Ubuntu ##

Pour installer le logiciel, vous pouvez ajouter le dépôt PPA (ppa:chaoswizard/tvdownloader) à votre source.list :
```
deb http://ppa.launchpad.net/chaoswizard/tvdownloader/ubuntu lucid main
OU
deb http://ppa.launchpad.net/chaoswizard/tvdownloader/ubuntu maverick main
```
ou utiliser la commande :
```
sudo add-apt-repository ppa:chaoswizard/tvdownloader
```
puis un petit
```
aptitude update
aptitude install tvdownloader
```
N.B. :
  * Le PPA contient TVDownloader et MSDL (dépendance de TVDownloader)
  * Il vous faudra également rtmpdump que vous pourrez trouver [ICI](http://security.ubuntu.com/ubuntu/pool/universe/r/rtmpdump/) (NB : rtmpdump est désormais dans les dépôts de Ubuntu 10.10 Marverick).

## Pour les autres distributions ##

  * Une archive tar.gz contenant le logiciel et ses sources est disponible [ICI](http://tvdownloader.googlecode.com/files/tvdownloader-0.7.tar.gz)
  * La liste des dépendances pour le logiciel est disponible [ICI](http://code.google.com/p/tvdownloader/wiki/Dependances)