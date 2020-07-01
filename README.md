# Certificat et authentification
## I. Présentation du projet

## II. Technologies utilisées, Architecture & Fonctionnalités
Le travail effectué m'était demandé dans le langage `Python` (version 3.6). J'ai donc utilisé les librairies `getmac`, `pycrypto`, `datetime` et `hashlib`.  
Les fichiers se trouvant dans le dossier `private` sont protégés par un mot de passe.
```
projet/
|-- certificat/
    |-- certificat.py
    |-- private/
        |-- certif_serial_nb.txt
        |-- mykey.pem
|-- README.md
```
À la génération du certificat, il est demandé à l'utilisateur de choisir un délais de validité en nombre de jours.  
Chaque ligne du certificat correspond à un élément différent :
* le numéro de série du certificat  
* le numéro de série du générateur associé au certificat
* l'algorithme de chiffrement utilisé
* la durée du certificat
* la clé publique
* l'uuid de la carte mère de l'ordinateur
* l'adresse mac de la carte réseau de l'ordinateur
* le numéro de série de l'ordinateur  

Chaque numéro de série de certificat est enregistré dans le fichier `certif_serial_nb.txt` afin qu'il n'y ai pas 2 fois le même.
La clé privée est stockée dans le fichier `mykey.pem`.

## IV. Pré-requis & Utilisation
### Pré-requis :
Afin d'utiliser le programme, il faut installer ou mettre à jour ... :
* python 3.6
* pip
* getmac
* pycrypto
* datetime
* hashlib
#### 1. Installation de `python 3` et `pip` :
* Pour Windows :  
Pour installer `python3`, veuillez télécharger le programme d'installation exécutable sur le [site officiel](https://www.python.org/downloads/) puis exécuter le programme, cocher les deux cases et installer.  
![install](python-setup.png)
>`pip` est normalement installée en même temps

* Pour Linux :  
```bash
# ubuntu & debian:
[user]~ sudo apt-get install python3.6
[user]~ sudo apt-get install python3-pip
# centos:
[user]~ sudo yum install -y python3
[user]~ sudo yum install -y python-pip
# arch:
[user]~ sudo pacman -S python
[user]~ sudo pacman -S python-pip
```
* Pour macOS/X :
```bash
[user]~ brew install python
```
>`pip` est normalement installée en même temps
#### 2. Vérification de la version et de l'installation de python et de pip :
```bash
[user]~ python
Python 3.8.3 (default, May 17 2020, 18:15:42) 
[GCC 10.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> ctrl+D
[user]~ pip -V
pip 20.0.2 from /usr/lib/python3.8/site-packages/pip (python 3.8)
```
### Utilisation
Pour générer un certificat, vous devez ouvrir un terminal et taper la commande suivante:
```bash
[user]~ python certificat.py
```
## V. Problèmes rencontrés
* Trouver 3 identifiants d'ordinateur uniques et qui sont le moins susceptibles d'être changés
* Fonction de hashage : problème d'encodage des données résolu en encodant les donnée en `utf-8`
* Fonction d'encryptage : problème de longueur de données à crypter (trop grande)

## VI. Améliorations suggérées