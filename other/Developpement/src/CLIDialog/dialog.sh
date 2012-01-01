#!/bin/sh
# Script de présentation de dialog
# demo_dialog.sh copyleft spi.marc 2004

# Pour découvrir dialog par la pratique :
# faites tourner ce script, examinez son code.

# Différentes boîtes de dialog sont ici présentées dans
# un contexte minimal. A chacune de ces boîtes correspond
# une fonction ; elles apparaissent dans l'ordre suivant.
# [message d'introduction à dialog (fonction intr)]
# Définition
# - d'une boîte d'information (fonction info)
# - d'une boîte de message (fonction mess)
# - d'une boîte de sélection de fichier (fonction fsel)
# - d'une boîte de fichier texte (fonction text)
# - d'une boîte de barre d'avancement (fonction gaug)
# - d'une boîte oui non (fonction yesn)
# - d'une boîte d'entrée de valeur (fonction inpu)
# - d'une boîte de mot de passe (fonction pass)
# - d'une boîte d'heure (fonction time)
# - d'une boîte de menu (fonction menu)
# [message sur les boîtes de cases à cocher (fonction mche)]
# - d'une boîte de cases à cocher (fonction chec)

# # # Début du script proprement dit # # #

# Définition d'un fichier temporaire
# Il sert à conserver les sorties de dialog qui sont normalement
# redirigées vers la sortie d'erreur (2). trap sert à être propre.
touch /tmp/dialogtmp && FICHTMP=/tmp/dialogtmp
trap "rm -f $FICHTMP" 0 1 2 3 5 15

# Définitions des différentes fonctions
# Message d'introduction à dialog
# (boîtes de message voyez plutôt la fonction mess)
function intr ()
{
dialog --backtitle "Présentation de dialog" --title "Introduction" \
--ok-label "Suite" --msgbox "
Dialog vous permet d'améliorer la présentation de vos
scripts bash en mode texte. Il comporte de nombreuses
boîtes et options, vous en découvrirez quelques unes
en utilisant ce script (console 80x25 recommandée).

En mode graphique vous pouvez utiliser xdialog dont la
syntaxe est proche de celle de dialog." 12 60

dialog --backtitle "Présentation de dialog" --title "Introduction (suite)" \
--msgbox "
Une instruction dialog possède la syntaxe suivante:
dialog --options communes --options de boîte

Par exemple --title est une option commune que l'on
peut utiliser avec toutes les boîtes. Alors que
--info est une option spécifique (de boîte info)." 12 60
}

# Définition d'une boîte d'information
function info ()
{
dialog --backtitle "Présentation de dialog" --title "Boîte d'information" \
--sleep 12 --infobox "
Ceci est une boîte d'information.
Sa syntaxe est --infobox text height width
Elle ne comporte pas de bouton par défaut.
Ici l'option --sleep 12 fixe son temps de vie à 12 s.

Pour la tester vous pouvez entrer dans une console:
dialog --sleep 4 --infobox Information 8 40" 12 60
}

# Définition d'une boîte de message
function mess ()
{
dialog --backtitle "Présentation de dialog" --title "Boîte de message" \
--msgbox "
Ceci est une boîte de message.
Sa syntaxe est --msgbox text height width
Elle ne comporte qu'un seul bouton par défaut.

Pour la tester vous pouvez entrer dans une console:
dialog --msgbox Message 8 40" 12 60
}

# Définition d'une boîte de sélection de fichier
function fsel ()
{
# message sur les boîtes de sélection de fichier (boîte de message)
dialog --backtitle "Présentation de dialog" --title "Les boîtes de sélection de fichier" \
--ok-label "Suite" --msgbox "
Une boîte de sélection de fichier permet ...
de sélectionner un fichier.
Sa syntaxe est --fselect filepath height width
Pour l'afficher vous pouvez entrer dans une console:
dialog --fselect $HOME/ 12 60

Voyez aussi la boîte suivante de ce script." 12 60
# boîte de sélection de fichier proprement dite
dialog --backtitle "Présentation de dialog" --title "Boîte de sélection de fichier" \
--ok-label "Valider" --fselect $HOME/ 8 60 2> $FICHTMP
# retour d'information (boîte d'info)
# 0 est le code retour du bouton Valider
# seul celui-ci permet ici de sélectionner un fichier.
if [ $? = 0 ]
then INFO="Le fichier sélectionné est `cat $FICHTMP`"
else INFO="Vous n'avez pas sélectionné de fichier!"
fi
dialog --backtitle "Présentation de dialog" --title "Votre sélection" \
--sleep 2 --infobox "
$INFO" 8 40
}

# Définition d'une boîte de fichier texte
function text ()
{
# message sur les boîtes de fichier texte (boîte de message)
dialog --backtitle "Présentation de dialog" --title "Les boîtes texte" \
--ok-label "Suite" --msgbox "
Une boîte texte permet d'afficher le contenu d'un
fichier texte passé en paramètre.
Sa syntaxe est --textbox file height width
Pour l'essayer vous pouvez entrer dans une console:
dialog --textbox /etc/inittab 18 60

La boîte texte suivante va afficher ce script.
Utilisez les 4 flèches pour vous déplacer." 14 60
# boîte de fichier texte proprement dite
# $0 est la variable correspondant au script
dialog --backtitle "Présentation de dialog" --title "Boîte de fichier texte" \
--textbox $0 18 60
}

# Définition d'une boîte de barre d'avancement
# La jauge avance par la redirection |
# de la sortie du sous shell ( ) qui la précède.
function gaug ()
{
(for i in `seq 0 10 100` ; do echo $i ; sleep 1 ; done) | \
dialog --backtitle "Présentation de dialog" --title "Boîte de barre d'avancement" \
--gauge "
Ceci est une boîte de barre d'avancement.
Sa syntaxe est --gauge text height width [percent]
Sa progression vient du sous shell () qui la précède.

Vous avez 10 secondes pour lire ce message.
" 12 60 0
}

# Définition d'une boîte oui non
function yesn ()
{
# boîte oui non proprement dite
dialog --backtitle "Présentation de dialog" --title "Boîte oui non" \
--yesno "
Ceci est une boîte oui non.
Elle sert bien sûr à poser une question fermée.
Sa syntaxe est --yesno text height width
Pour l'essayer vous pouvez entrer dans une console:
dialog --yesno Question 8 40

Souhaitez-vous quitter ce script ? " 12 60
# traitement de la réponse
# O est le code retour du bouton Oui
# ici Oui arrête le script
# toute autre action (Non, Esc, Ctrl-C) le poursuit
if [ $? = 0 ]
then exit 0
else
# boîte d'info
dialog --backtitle "Présentation de dialog" --title "Remerciements" \
--sleep 4 --infobox "
L'auteur de ce script vous trouve
de ce fait bien sympathique." 8 40
fi
}

# Définition d'une boîte d'entrée de valeur
function inpu ()
{
# boîte d'entrée de valeur proprement dite
dialog --backtitle "Présentation de dialog" --title "Boîte d'entrée" \
--inputbox "
Ceci est une boîte d'entrée.
Sa syntaxe est --inputbox text height width [init]
Ici l'option init est utilisée et contient user
Pour l'afficher vous pouvez entrer dans une console:
dialog --inputbox Entrée 8 40

Entrez votre nom de login:" 14 60 user 2> $FICHTMP
# retour d'information (boîte d'info)
# 0 est le code retour du bouton Accepter
# ici seul celui-ci attribue un nom de login.
if [ $? = 0 ]
then INFO="Votre nom de login est `cat $FICHTMP`"
else INFO="Vous n'avez pas de nom de login!"
fi
dialog --backtitle "Présentation de dialog" --title "Votre login" \
--sleep 2 --infobox "
$INFO" 8 40
}

# Définition d'une boîte de mot de passe
function pass ()
{
# boîte de mot de passe proprement dite
dialog --backtitle "Présentation de dialog" --title "Boîte de mot de passe" \
--insecure --passwordbox "
Ceci est une boîte de mot de passe.
Sa syntaxe est --passwordbox text height width [init]
Ici l'option --insecure est utilisée pour avoir des *
Pour la tester vous pouvez entrer dans une console:
dialog --passwordbox Password 8 40

Entrez un mot de passe fictif (il sera affiché):" 14 60 2> $FICHTMP
# retour d'information (boîte d'info)
# pour la démo, à éviter en temps normal !
# 0 est le code retour du bouton Accepter
# ici seul celui-ci attribue un mot de passe.
if [ $? = 0 ]
then INFO="Le mot de passe choisi est `cat $FICHTMP`"
else INFO="Vous n'avez pas de mot de passe!"
fi
dialog --backtitle "Présentation de dialog" --title "Votre mot de passe" \
--sleep 2 --infobox "
$INFO" 8 40
}

# Définition d'une boîte d'heure
function time ()
{
# boîte d'heure proprement dite
dialog --backtitle "Présentation de dialog" --title "Boîte d'heure" \
--timebox "
Ceci est une boîte d'heure. Sa syntaxe est
--timebox text height width [hour minute second]
Pour l'afficher vous pouvez entrer dans une console:
dialog --timebox Heure 4 40

Quelle est votre heure locale ?" 10 60 2> $FICHTMP
# retour d'information (boîte d'info)
# 0 est le code retour du bouton Accepter
# seul celui-ci permet de définir une heure différente.
if [ $? = 0 ]
then INFO="Votre heure locale est `cat $FICHTMP`"
else INFO="Vous n'avez pas défini d'heure.
L'heure par défaut est `date +%X`"
fi
dialog --backtitle "Présentation de dialog" --title "Heure locale" \
--sleep 2 --infobox "
$INFO" 8 40
}

# Définition d'une boîte de menu
function menu ()
{
# boîte de menu proprement dite
dialog --backtitle "Présentation de dialog" --title "Boîte de menu" \
--menu "
Ceci est une boîte de menu. Sa syntaxe est
--menu text height width menu-height [tag item] ...
Elle permet de faire un choix parmi une liste.

Choisissez une des entrées proposées:" 18 60 6 \
"Continuer" "Continuer selon les choix déjà faits" \
"Introduction" "Relire l'intro à dialog puis continuer" \
"Arrêter" "Et au revoir..." 2> $FICHTMP
# traitement de la réponse
if [ $? = 0 ]
then
for i in `cat $FICHTMP`
do
case $i in
# Continuer est par défaut
Introduction) intr ;;
Arrêter) exit 0 ;;
esac
done
fi
}

# Message sur les boîtes de cases à cocher
# (boîtes de message voyez plutôt la fonction mess)
function mche ()
{
dialog --backtitle "Présentation de dialog" --title "Les boîtes de cases à cocher" \
--ok-label "Suite" --msgbox "
Une boîte de cases à cocher permet de proposer un menu
à choix multiples. Sa syntaxe est --checklist
text height width list-height [tag item status] ...

Le menu principal de ce script est une boîte de ce
type. Vous la retrouverez en quittant cet écran." 12 60
}

# Définition d'une boîte de cases à cocher
# Menu principal de choix des boîtes du script
function chec ()
{
# boîte de cases à cocher proprement dite
dialog --backtitle "Présentation de dialog" --title "Liste des boîtes" \
--ok-label "Valider" --cancel-label "Quitter" \
--checklist "
Cochez les boîtes dont vous souhaitez une présentation." 18 60 10 \
"intr" "Introduction à dialog" off \
"info" "Boîte d'information" off \
"mess" "Boîte de message" off \
"fsel" "Boîte de sélection de fichier" off \
"text" "Boîte de fichier texte" off \
"gaug" "Boîte de barre d'avancement" off \
"yesn" "Boîte oui non" off \
"inpu" "Boîte d'entrée de valeur" off \
"pass" "Boîte de mot de passe" off \
"time" "Boîte d'heure" off \
"menu" "Boîte de menu" off \
"mche" "Boîte de cases à cocher (message sur)" off 2> $FICHTMP
# traitement de la réponse
# 0 est le code retour du bouton Valider
# ici seul le bouton Valider permet de continuer
# tout autre action (Quitter, Esc, Ctrl-C) arrête le script.
if [ $? = 0 ]
then
for i in `cat $FICHTMP`
do
case $i in
\"intr\") intr ;;
\"info\") info ;;
\"mess\") mess ;;
\"fsel\") fsel ;;
\"text\") text ;;
\"gaug\") gaug ;;
\"yesn\") yesn ;;
\"inpu\") inpu ;;
\"pass\") pass ;;
\"time\") time ;;
\"menu\") menu ;;
\"mche\") mche ;;
esac
done
else exit 0
fi
}

# Fin des définitions des fonctions
# Boucle d'appel du menu principal à l'infini
while :
do chec
done

# dialog offre de nombreuses autres possibilités.
# A vous maintenant de les découvrir au travers
# par exemple de sa page man :o)

# # # Fin du script # # #