#!/usr/bin/env python3
import os, sys, hashlib
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta
from getmac import get_mac_address as gma

def generate_keys():
    global keys, pubkey, privkey
# Dévérouiller l'accès aux fichiers

# Générer une paire de clés RSA
    keys = RSA.generate(2048) # Taille de la clé en bits
# Exporter les clés
    pubkey = keys.publickey().exportKey('PEM')
    privkey = keys.exportKey('PEM')
# Enregistrer les clés dans 2 fichiers
    # pour la clé publique
    with open('public.pem', 'w') as file_pubkey:
        file_pubkey.write(pubkey.decode())
        file_pubkey.close()
    # pour la clé privée
    with open('private.pem', 'w') as file_privkey:
        file_privkey.write(privkey.decode())
        file_privkey.close()
# Vérouiller l'accès aux fichiers

    return pubkey
"""
Cette fonction hash les données du certificat et les retourne.
Elle utilise la fonction de hachage SHA256.
"""
def hash_func(data):
    global hash_message
# Encodage avant hachage
    data = data.encode('ascii')
# Fonction de hachage
    hash_message = hashlib.sha256(data)
# Passage en hexadecimal
    hash_message = hash_message.hexdigest()
    return hash_message
"""
Cette fonction récupère la clé publique et encrypte les données du certificat.
Elle retourne les données encryptées.
"""
def encrypt(data):
    global encrypt_data, privkey
# Récupérer la clé privée
    with open('./private/private.pem', 'r') as file_privkey:
        priv_key = file_privkey.read()
        file_privkey.close()
    privkey = RSA.import_key(priv_key)
# Encoder les données en ascii
    data = data.encode('ascii')
# Encrypter les données
    encrypt_data = privkey.encrypt(data)
    return encrypt_data



































"""
def gen_binary(text):
    tab = []
    count = 0
    for char in text:
        binary = '0' + bin(ord(char))[2:]
        while count <= len(text):
            tab.append(binary)
            count += 1
        return tab

print(gen_binary(gen_certificate()))
"""