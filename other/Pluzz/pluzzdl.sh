#!/bin/bash

cd "__DATADIR__/pluzzdl/"

if [ ! -z "`python --version 2>&1 | grep 'Python 2'`" ]
then
	python main.py "$*"
else
	if [ -x "/usr/bin/python2" ]
	then
		python2 main.py "$*"
	else
		if [ -x "/usr/bin/python2.7" ]
		then
			python2.7 main.py "$*"
		else
			if [ -x "/usr/bin/python2.6" ]
			then
				python2.6 main.py "$*"
			else
				echo "Erreur : impossible de trouver une version de Python 2"
			fi
		fi
	fi
fi
