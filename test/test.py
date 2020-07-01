#!/usr/bin/env python3
import os, sys, hashlib
from getmac import get_mac_address as gma
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta
from getmac import get_mac_address as gma

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
print(certificat)