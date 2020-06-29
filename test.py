#!/usr/bin/env python3
import os, sys
from certificat import duration, generate_key, get_motherboard_uuid, get_mac, get_serial_nb, gen_certif_serial_nb

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
    text = certif_serial_nb + gen_serial_nb + hashage + duree + pubkey + uuid + mac + serial_nb
    return text


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