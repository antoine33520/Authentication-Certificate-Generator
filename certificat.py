#!/usr/bin/env python3
import os, sys, hashlib
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta
from getmac import get_mac_address as gma


def get_motherboard_uuid():
    global result1
    os_type = sys.platform.lower()
    if "win" in os_type:
        commande = "wmic csproduct get name,identifyingnumber,uuid"
    elif "linux" in os_type:
        commande = "dmidecode | grep -i uuid"
    elif "darwin" in os_type:
        commande = "dmidecode --string system-uuid"
    result1 = os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")
    return result1

def get_mac():
    global mac_address
    mac_address = str("MAC:" + gma())
    return mac_address

def get_serial_nb():
    global result2
    os_type = sys.platform.lower()
    if "win" in os_type:
        commande = "wmic bios get serialnumber"
    elif "linux" in os_type:
        commande = "dmidecode -t system | grep Serial"
    elif "darwin" in os_type:
        commande = "ioreg -l | grep IOPlatformeSerialNumber"
    result2 = os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")
    return result2


def generate_key():
    global key, pubkey
    # Générer paire de clés RSA
    key = RSA.generate(2048) # Taille de la clé en bits
    # Enregistrer la clé dans un fichier
    file = open('mykey.pem', 'wb')
    file.write(key.export_key('PEM'))
    file.close()
    pubkey = key.publickey().exportKey('PEM')
    return pubkey


# Message à crypter
message = 'certificat'
def hash_func():
    global hex_dig
    # Fonction de hachage
    hash_message = hashlib.sha256(message)
    hex_dig = hash_message.hexdigest()
    print(hex_dig)

# dates de début et de fin de validité
def duration():
    # date de création du certificat et début de validité
    date_debut = datetime.now()
    date_debut = str(date_debut.day) + '-' + str(date_debut.month) + '-' + str(date_debut.year)
    # date de fin de validité du certificat
    date_fin = datetime.now() + timedelta(days=10)
    date_fin = str(date_fin.day) + '-' + str(date_fin.month) + '-' + str(date_fin.year)
    duree = 'Du ' + date_debut + ' au ' + date_fin
    return(duree)

certif_serial_nb = 0
# Structure d'un certificat :
def generate_certificate():
    global certif_serial_nb
    # numéro de série du certificat
    for generate_certificate() == True:
        certif_serial_nb += 1
        print(certif_serial_nb)
    # numéro de série du générateur en uint16 [0,65535] de 4 caractères
    gen_serial_nb = 'GeneratorSerialNumber:0001'
    print(gen_serial_nb)
    # algorithme de chiffrement utilisé pour signer le certificat
    print('Hash:SHA256')
    # durée
    print(duration())
    # clé publique du propriétaire du certificat
    pubkey = 'PublicKey:' + str(generate_key())
    print(pubkey)
    # identifiants pc
    print(get_motherboard_uuid())
    print(get_mac())
    print(get_serial_nb())



generate_certificate()

# mettre en binaire et identifier la cle de hash et publique
# uint16 (4 caracteres)
# signature avant chiffrement = + sécurisé !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
