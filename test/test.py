#!/usr/bin/env python3
import os, sys, hashlib
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta
from getmac import get_mac_address as gma

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

path = "/home/eve/Documents/Cours/Stage/private/"

def lock():
    os_type = sys.platform.lower()
    if "win" in os_type:
        lock_folder = "chmod..."
        lock_file_sn = "chmod a-w+rx ./private/certif_serialnb.txt"
        lock_file_key = "chmod a-rwx ./private/mykey.pem"
    elif "linux" in os_type:
        lock_folder = "chmod a-w+rx ./private/"
        lock_file_sn = "chmod a-w+rx ./private/certif_serialnb.txt"
        lock_file_key = "chmod a-rwx ./private/mykey.pem"
    elif "darwin" in os_type:
        lock_folder = "chmod a-w+rx ./private/"
        lock_file_sn = "chmod a-w+rx ./private/certif_serialnb.txt"
        lock_file_key = "chmod a-rwx ./private/mykey.pem"
    lock_folder = os.popen(lock_folder).read().replace("\n","").replace("	","").replace(" ","")
    lock_file_sn = os.popen(lock_file_sn).read().replace("\n","").replace("	","").replace(" ","")
    lock_file_key = os.popen(lock_file_key).read().replace("\n","").replace("	","").replace(" ","")
    return lock_folder, lock_file_sn, lock_file_key












lock()
unlock()
lock()
# dossier interdit d'ecrire et d'exécuter
# demander mot de passe
    # si autorisé :
        # changer mode fichier pour lecture et écriture
        # faire le taff
        # remettre en privé
    # si pas autorisé :
        # rien changer et mettre message erreur




































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