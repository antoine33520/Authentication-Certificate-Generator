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
    global keys, pubkey
    # Générer paire de clés RSA
    keys = RSA.generate(2048) # Taille de la clé en bits
    # Enregistrer la clé dans un fichier
    file = open('mykey.pem', 'wb')
    file.write(keys.export_key('PEM'))
    file.close()
    pubkey = keys.publickey().exportKey('PEM')
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
    duration = int(input('Quelle est la durée du certificat ? \nVeuillez entrer un nombre de jours :\n'))
    date_fin = datetime.now() + timedelta(days=duration)
    date_fin = str(date_fin.day) + '-' + str(date_fin.month) + '-' + str(date_fin.year)
    duree = 'Du ' + date_debut + ' au ' + date_fin
    return(duree)

def gen_certif_serial_nb():
    # Ouvrir le fichier en mode lecture et ajout
    serial_nb_file = open('certif_serial_nb.txt', 'r')
    # Récupérer la dernière ligne
    last_line = len(serial_nb_file.readlines()) - 1
    # Fermer le fichier
    serial_nb_file.close()
    # Créer nouveau numéro de série
    certif_serial_nb = int(last_line) + 1
    # Ouvrir le fichier en mode lecture et ajout
    serial_nb_file = open('certif_serial_nb.txt', 'a')
    # Ajouter nouveau numéro de série au fichier
    serial_nb_file.write('\n' + str(certif_serial_nb))
    # Fermer le fichier
    serial_nb_file.close()
    return certif_serial_nb

# Structure d'un certificat :
def gen_certificate():
    # numéro de série du certificat
    certif_serial_nb = 'CertificateSerialNumber:' + str(gen_certif_serial_nb())
    # numéro de série du générateur en uint16 [0,65535] de 4 caractères
    gen_serial_nb = 'GeneratorSerialNumber:0001'
    # algorithme de chiffrement utilisé pour signer le certificat
    hashage = 'Hash:SHA256'
    # durée
    duree = duration()
    # clé publique du propriétaire du certificat
    pubkey = 'PublicKey:' + str(generate_key())
    # identifiants pc
    uuid = get_motherboard_uuid()
    mac = get_mac()
    serial_nb = get_serial_nb()
    text = certif_serial_nb + '\n' + gen_serial_nb + '\n' + hashage + '\n' + duree + '\n' + pubkey + '\n' + uuid + '\n' + mac + '\n' + serial_nb
    return text


print(gen_certificate())

# mettre en binaire et identifier la cle de hash et publique
# uint16 (4 caracteres)
# signature avant chiffrement = + sécurisé !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
