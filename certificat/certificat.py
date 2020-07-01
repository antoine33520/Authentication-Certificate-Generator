#!/usr/bin/env python3
import os, sys, hashlib
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from datetime import datetime, timedelta
from getmac import get_mac_address as gma

############################################################################################
############################################################################################
####################                 IDENTIFIANTS DU PC              #######################
############################################################################################
############################################################################################
"""
Cette fonction retourne l'uuid de la carte mère.
Elle exécute une commande en focntion de l'os utilisé (windows, linux, macos).
"""
def get_motherboard_uuid():
    global motherboard_uuid
    os_type = sys.platform.lower()
    if "win" in os_type:
        commande = "wmic csproduct get name,identifyingnumber,uuid"
    elif "linux" in os_type:
        commande = "dmidecode | grep -i uuid"
    elif "darwin" in os_type:
        commande = "dmidecode --string system-uuid"
    motherboard_uuid = os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")
    return motherboard_uuid
"""
Cette fonction retourne l'adresse mac de la carte réseau utilisée.
"""
def get_mac():
    global mac_address
    mac_address = str("MAC:" + gma())
    return mac_address
"""
Cette fonction retourne le numéro de série de l'ordinateur, se trouvant sur le bios.
Elle exécute une commande en fonction de l'os utlisée (windows, linux, macos).
"""
def get_serial_nb():
    global serial_nb
    os_type = sys.platform.lower()
    if "win" in os_type:
        commande = "wmic bios get serialnumber"
    elif "linux" in os_type:
        commande = "dmidecode -t system | grep Serial"
    elif "darwin" in os_type:
        commande = "ioreg -l | grep IOPlatformeSerialNumber"
    serial_nb = os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")
    return serial_nb


############################################################################################
############################################################################################
####################          SIGNATURE, HACHAGE, ENCRYPTION         #######################
############################################################################################
############################################################################################
"""
Cette fonction génère une paire de clés rsa.
Elle les enregistre dans un fichier appelé 'mykey.pem'.
Puis elle exporte la clé publique et la retourne.
"""
def generate_keys():
    global keys, pubkey
    # Générer paire de clés RSA
    keys = RSA.generate(2048) # Taille de la clé en bits
    # Enregistrer la clé dans un fichier
    file = open('./private/mykey.pem', 'wb')
    file.write(keys.export_key('PEM'))
    file.close()
    pubkey = keys.publickey().exportKey('PEM')
    return pubkey
"""
Cette fonction récupère la clé publique et encrypte les données du certificat.
Elle retourne les données encryptées.
"""
def encrypt(data):
    global encrypt_data, keys
    keys = generate_keys()
    cipher = PKCS1_OAEP.new(keys)
    encrypt_data = cipher.encrypt(data)
    return encrypt_data
"""
Cette fonction hash les données du certificat et les retourne.
Elle utilise la fonction de hachage SHA256.
"""
def hash_func(data):
    global hash_message
    # Encodage avant hachage
    data = data.encode('utf-8')
    # Fonction de hachage
    hash_message = hashlib.sha256(data)
    # Passage en hexadecimal
    hash_message = hash_message.hexdigest()
    return hash_message


############################################################################################
############################################################################################
####################                 CONTENU CERTIFICAT              #######################
############################################################################################
############################################################################################
"""
Cette fonction détermine la durée du certificat.
Elle prend la date de création du certificat.
Elle demande à l'utilisateur de choisir sa durée en jours à sa génération.
"""
# dates de début et de fin de validité
def duration():
    # date de création du certificat et début de validité
    date_debut = datetime.now()
    date_debut = str(date_debut.day) + '-' + str(date_debut.month) + '-' + str(date_debut.year)
    # date de fin de validité du certificat
    duration = int(input('Quelle est la durée du certificat ? \nVeuillez entrer un nombre de jours : '))
    date_fin = datetime.now() + timedelta(days=duration)
    date_fin = str(date_fin.day) + '-' + str(date_fin.month) + '-' + str(date_fin.year)
    duree = 'Du ' + date_debut + ' au ' + date_fin
    return(duree)
"""
Cette fonction génère le numéro de série du certificat.
Elle stocke tous les numéros de série dans l'ordre dans le fichier 'certif_serial_nb.txt'.
Elle y récupère le dernier numéro utilisé pour y ajouter 1 et l'enregistrer à la fin du fichier.
"""
def gen_certif_serial_nb():
    # Ouvrir le fichier en mode lecture
    serial_nb_file = open('./private/certif_serialnb.txt', 'r')
    # Récupérer la dernière ligne
    last_line = len(serial_nb_file.readlines()) - 1
    # Fermer le fichier
    serial_nb_file.close()
    # Créer nouveau numéro de série
    certif_serial_nb = int(last_line) + 1
    # Ouvrir le fichier en mode ajout
    serial_nb_file = open('./private/certif_serialnb.txt', 'a')
    # Ajouter nouveau numéro de série au fichier
    serial_nb_file.write('\n' + str(certif_serial_nb))
    # Fermer le fichier
    serial_nb_file.close()
    return certif_serial_nb
"""
Cette fonction représentant la structure du certificat.
Elle réuni toutes les fonctions précédentes pour afficher les informations qui se trouvent sur notre certificat.
"""
# Structure d'un certificat :
def gen_certificate():
    # numéro de série du certificat
    certif_serial_nb = 'CertificateSerialNumber:' + str(gen_certif_serial_nb())
    certif_serial_nb = hash_func(certif_serial_nb)
    certif_serial_nb = encrypt(certif_serial_nb)
    # numéro de série du générateur en uint16 [0,65535] de 4 caractères
    gen_serial_nb = 'GeneratorSerialNumber:0001'
    gen_serial_nb = hash_func(gen_serial_nb)
    # algorithme de chiffrement utilisé pour signer le certificat
    hashage = 'SHA256'
    hashage = hash_func(hashage)
    # durée
    duree = duration()
    duree = hash_func(duree)
    # clé publique du propriétaire du certificat
    pubkey = str(generate_keys())
    pubkey = hash_func(pubkey)
    # identifiants pc
    uuid = get_motherboard_uuid()
    uuid = hash_func(uuid)
    mac = get_mac()
    mac = hash_func(mac)
    serial_nb = get_serial_nb()
    serial_nb = hash_func(serial_nb)
    text = certif_serial_nb + '\n' + gen_serial_nb + '\n' + hashage + '\n' + duree + '\n' + pubkey + '\n' + uuid + '\n' + mac + '\n' + serial_nb
    return text

certificat = gen_certificate()
print('Voici votre certificat :\n' + certificat)
############################################################################################
############################################################################################
####################            CERTIFICAT HASHÉ ET CRYPTÉ           #######################
############################################################################################
############################################################################################


# signature avant chiffrement = + sécurisé !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# chiffrer avec la clé de hash OK!
# puis chiffrer avec la clé publique ENCOURS!
# mettre en binaire et identifier la cle de hash et publique