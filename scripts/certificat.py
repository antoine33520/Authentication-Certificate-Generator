#!/usr/bin/env python3
import os, sys, hashlib, getpass, binascii

from Crypto.Hash import SHA256
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from datetime import datetime, timedelta


######################################################################################################################################################
######################################################################################################################################################
############################################                 IDENTIFIANTS DU PC                 ######################################################
######################################################################################################################################################
######################################################################################################################################################
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
        commande = "dmidecod | grep -i uuid"
    elif "darwin" in os_type:
        commande = "dmidecode --string system-uuid"
    else :
        print('Erreur: Je ne suis pas en mesure d\'identifier votre OS.')
    motherboard_uuid = "UUID:" + os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")
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
    else :
        print('Erreur: Je ne suis pas en mesure d\'identifier votre OS.')
    serial_nb = "SerialNumber:" + os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")
    return serial_nb


######################################################################################################################################################
######################################################################################################################################################
########################################                 SIGNATURE, HACHAGE, ENCRYPTION                 ##############################################
######################################################################################################################################################
######################################################################################################################################################
"""
Cette fonction génère une paire de clés rsa.
Elle les enregistre dans un fichier appelé 'mykey.pem'.
Puis elle exporte la clé publique et la retourne.
"""
def generate_keys():
    global keys, pubkey, privkey
# Dévérouiller l'accès aux fichiers
    unlock()
# Générer une paire de clés RSA
    keys = RSA.generate(2048) # Taille de la clé en bits
    privkey, pubkey = keys, keys.publickey()
# Exporter les clés
    pubkey = pubkey.exportKey('PEM')
    privkey = privkey.exportKey('PEM')
# Enregistrer les clés dans 2 fichiers
    # pour la clé publique
    with open('./private/public.pem', 'wb') as file_pubkey:
        file_pubkey.write(pubkey)
        file_pubkey.close()
    # pour la clé privée
    with open('./private/private.pem', 'wb') as file_privkey:
        file_privkey.write(privkey)
        file_privkey.close()
# Décoder les clés
    #pubkey = pubkey.decode('ascii')
    #privkey = privkey.decode('ascii')
# Vérouiller l'accès aux fichiers
    lock()
    return pubkey, privkey
"""
Cette fonction hash les données du certificat et les retourne.
Elle utilise la fonction de hachage SHA256.
"""
def hash_func(data):
    global hash_message
# Encodage avant hachage
    data = data.encode('ascii')
# Fonction de hachage
    hash_message = SHA256.new(data)
# Passage en hexadecimal
    hash_message = hash_message.hexdigest()
    return hash_message
"""
Cette fonction récupère la clé publique et encrypte les données du certificat.
Elle retourne les données encryptées.
"""
def encrypt_func(data):
    unlock()
    with open('./private/private.pem', 'r') as priv_key_file:
        privkey_list = priv_key_file.readlines()
        key = "".join(privkey_list)
        privkey = RSA.import_key(key)
    encryptor = PKCS1_OAEP.new(privkey, SHA256)
    encrypt_data = encryptor.encrypt(data.encode('ascii'))
    lock()
    return encrypt_data


######################################################################################################################################################
######################################################################################################################################################
#################################################                 CONTENU CERTIFICAT              ####################################################
######################################################################################################################################################
######################################################################################################################################################
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
# Autoriser l'accès en mode écriture aux fichiers
    unlock()
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
# Fermer l'accès aux fichier
    lock()
    return certif_serial_nb
"""
Cette fonction représentant la structure du certificat en clair, haché puis chiffré.
Elle réuni toutes les fonctions précédentes pour afficher les informations qui se trouvent sur notre certificat.
"""
def gen_certificate():
# Vérouiller les fichiers supplémentaires
    lock()
# Récupérer la clé publique
#     pubkey = generate_keys()
# numéro de série du certificat
    certif_serial_nb = 'CertificateSerialNumber:' + str(gen_certif_serial_nb())
    certif_serial_nb = hash_func(certif_serial_nb)
    certif_serial_nb = encrypt_func(certif_serial_nb)
    print(certif_serial_nb)
# numéro de série du générateur en uint16 [0,65535] de 4 caractères
    gen_serial_nb = 'GeneratorSerialNumber:0001'
    gen_serial_nb = hash_func(gen_serial_nb)
# durée du certificat
    duree = duration()
    duree = hash_func(duree)
# identifiants pc
    # uuid carte mère
    uuid = get_motherboard_uuid() 
    uuid = hash_func(uuid)
    # adresse mac carte réseau
    mac = get_mac() 
    mac = hash_func(mac)
    # numéro de série du pc
    serial_nb = get_serial_nb() 
    serial_nb = hash_func(serial_nb)
# algorithme de chiffrement utilisé pour signer le certificat
    hachage = 'SHA256'
    hachage = hash_func(hachage)
# clé publique du propriétaire du certificat
    pubkey = str(generate_keys())
    pubkey = hash_func(pubkey)
    hashtext = f"""
    {str(certif_serial_nb)}
    {str(gen_serial_nb)}
    {str(hachage)}
    {str(duree)}
    {str(pubkey)}
    {str(uuid)}
    {str(mac)}
    {str(serial_nb)}
    """
    return hashtext


######################################################################################################################################################
######################################################################################################################################################
#################################################              PROTÉGER LES FICHIERS              ####################################################
######################################################################################################################################################
######################################################################################################################################################
"""
Cette fonction permet de bloquer l'accès aux 2 fichiers protégés dont se sert le certificat.
Ils ne sont pas lisibles, exécutables ou modifiables.
"""
def lock():
    os_type = sys.platform.lower()
    if "win" in os_type:
        lock_file_sn = "cacls ./private/certif_serialnb.txt /e /p Everyone:n"
        lock_file_pubkey = "cacls ./private/public.pem /e /p Everyone:n"
        lock_file_privkey = "cacls ./private/private.pem /e /p Everyone:n"
        print('Fichiers vérouillés.')
    elif "linux" or "darwin" in os_type:
        lock_file_sn = "sudo chmod a-w+rx ./private/certif_serialnb.txt"
        lock_file_pubkey = "sudo chmod a-rwx ./private/public.pem"
        lock_file_privkey = "sudo chmod a-rwx ./private/private.pem"
        print('Fichiers vérouillés.')
    else :
        print('Erreur: Je ne suis pas en mesure d\'identifier votre OS.')
    lock_file_sn = os.popen(lock_file_sn).read().replace("\n","").replace("	","").replace(" ","")
    lock_file_pubkey = os.popen(lock_file_pubkey).read().replace("\n","").replace("	","").replace(" ","")
    lock_file_privkey = os.popen(lock_file_privkey).read().replace("\n","").replace("	","").replace(" ","")
    return lock_file_sn, lock_file_pubkey, lock_file_privkey
"""
Cette fonction permet d'authoriser l'accès aux 2 fichiers protégés dont se sert le certificat.
Il est possible d'écrire
"""
def unlock():
    os_type = sys.platform.lower()
    mdp = getpass.getpass(prompt='Veuillez entrer le mot de passe svp (q pour quitter): ')
    if mdp == "q":
        sys.exit()
    else :
        while mdp != "ok":
            mdp = getpass.getpass(prompt='Veuillez entrer le mot de passe svp (q pour quitter): ')
            if mdp == "q":
                sys.exit()
        else:
            if "linux" or "darwin" in os_type:
                unlock_file_sn = "sudo chmod a+w ./private/certif_serialnb.txt"
                unlock_file_privkey = "sudo chmod a+rwx ./private/private.pem"
                unlock_file_pubkey = "sudo chmod a+rwx ./private/public.pem"
                print('Fichiers dévérouillés.')
            elif "win" in os_type:
                unlock_file_sn = "cacls ./private/certif_serialnb.txt /e /p Everyone:f"
                unlock_file_privkey = "cacls ./private/private.pem /e /p Everyone:f"
                unlock_file_pubkey = "cacls ./private/public.pem /e /p Everyone:f"
                print('Fichiers dévérouillés.')
            else :
                print('Erreur: Je ne suis pas en mesure d\'identifier votre OS.')
            unlock_file_sn = os.popen(unlock_file_sn).read().replace("\n","").replace("	","").replace(" ","")
            unlock_file_pubkey = os.popen(unlock_file_pubkey).read().replace("\n","").replace("	","").replace(" ","")
            unlock_file_privkey = os.popen(unlock_file_privkey).read().replace("\n","").replace("	","").replace(" ","")
    return unlock_file_pubkey, unlock_file_sn, unlock_file_privkey


######################################################################################################################################################
######################################################################################################################################################
##################################################            CERTIFICAT HASHÉ ET CRYPTÉ            ##################################################
######################################################################################################################################################
######################################################################################################################################################


# signature avant chiffrement = + sécurisé !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# chiffrer avec la clé de hash OK!
# puis crypter avec la clé privée ENCOURS!
# mettre en binaire et identifier la cle de hash et publique

certificat = gen_certificate()
print('Voici votre certificat :\n' + certificat)