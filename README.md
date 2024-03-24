# Gestionnaire de Fichiers en Double

Ce script Python aide à identifier et à gérer les fichiers en double dans un dossier spécifié par l'utilisateur. Il utilise un algorithme de hachage pour détecter efficacement les duplicatas et offre une interface graphique pour permettre à l'utilisateur de prévisualiser et de choisir les fichiers à supprimer.

## Fonctionnalités

- Parcours récursif des dossiers à la recherche de fichiers en double.
- Calcul du hash MD5 pour chaque fichier afin d'identifier les duplicatas.
- Interface graphique pour la sélection des dossiers et la confirmation de suppression des fichiers en double.
- Prise en charge de la prévisualisation des fichiers images et l'ouverture des PDF.
- Suppression sécurisée des fichiers en utilisant la corbeille du système d'exploitation.

## Prérequis

Pour exécuter ce script, vous aurez besoin de Python 3.6 ou supérieur ainsi que des dépendances listées dans le fichier `requirements.txt`.

## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances nécessaires avec la commande suivante :

pip install -r requirements.txt


## Utilisation

Lancez le script depuis un terminal ou un invite de commande :

python duplicate_file_manager.py


Suivez les instructions à l'écran pour sélectionner le dossier à analyser. Utilisez l'interface graphique pour gérer les fichiers en double détectés.

## Licence

Ce projet est distribué sous la Licence MIT. Voir le fichier `LICENSE` pour plus d'informations.


