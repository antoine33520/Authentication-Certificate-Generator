#!/usr/bin/env python3
import os, sys, hashlib
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta

# message à crypter
message = 'hello world'

def generate_key():
    # Générer paire de clés RSA
    key = RSA.generate(2048) # taille de la clé en bits
    # Enregistrer la clé dans un fichier
    file = open('mykey.pem', 'wb')
    file.write(key.export_key('PEM'))
    file.close()

def recup_pubkey():
    pubkey = key.publickey().exportKey('PEM')
    print(pubkey)

def hachage_func():
    # Fonction de hachage
    hash_message = hashlib.sha1(message)
    hex_dig = hash_message.hexdigest()

def duree():
    #### dates de début et de fin de validité
    ###### date de création du certificat et début de validité
    date_debut = datetime.now()
    date_debut = str(date_debut.day) + '-' + str(date_debut.month) + '-' + str(date_debut.year)
    ###### date de fin de validité du certificat
    date_fin = datetime.now() + timedelta(days=10)
    date_fin = str(date_fin.day) + '-' + str(date_fin.month) + '-' + str(date_fin.year)

# Générer une CSR (demande de signature)
# Supprimer la phrase secrète de la clé
# Générer un certificat auto-signé

## Structure d'un certificat :
#### version de X.509 à laquelle le certificat correspond
#### numéro de série du certificat
#### algorythme de chiffrement utilisé pour signer le certificat
#### objet de l'utilisation de la clé publique
#### clé publique du propriétaire du certificat
#### signature de l'émetteur du certificat

# mettre en binaire et identifier la cle de hash et publique
# uint16 (4 caracteres)
# signature avant chiffrement = + sécurisé !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
