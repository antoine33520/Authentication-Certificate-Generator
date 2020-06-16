#!/usr/bin/env python3
import socket, time, os, sys
from getmac import get_mac_address as gma


# fonction pour obtenir l'uuid de la carte mère 
def get_motherboard_uuid():
	os_type = sys.platform.lower()
	if "win" in os_type:
		commande = "wmic bios get serialnumber"
	elif "linux" in os_type:
		commande = "dmidecode | grep -i uuid"
	elif "darwin" in os_type:
		commande = "ioreg -l | grep IOPlatformeSerialNumber"
	return os.popen(commande).read().replace("\n","").replace("	","").replace(" ","")


host = "127.0.0.1"
port = 8080
name = 'User'
# Récupération de l'adresse MAC du client
mac_address = str(gma())
uuid = get_motherboard_uuid()
message = mac_address + "/" + uuid

# Création du socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connexion du socket au serveur
client.connect((host, port))
