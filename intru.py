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
name = 'Intru'
# Récupération de l'adresse MAC du client
mac_address = '18:31:bf:12:94:2e'
uuid = get_motherboard_uuid()

# Création du socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connexion du socket au serveur
client.connect((host, port))
print(name + " connecté au serveur")

# Envoi de l'adresse MAC vers le serveur avec la mac pour authentification
client.sendall(mac_address.encode("utf-8"))
print("Demande de connection envoyée pour : " + mac_address)
# Réception de la réponse du serveur
reponse = client.recv(255).decode("utf-8")
print("Server : " + reponse)
if reponse == 'Connexion acceptée !':
    print(name + " est connecté au server !\nVous avez le droit à 10s de connexion.")
    # Délai de connexion au server, ici 10 secondes
    time.sleep(10)
    # Fermeture de la connexion au serveur
    print("Connexion refusée !")
    client.close()
else :
    print(name + " n'est pas autorisé à se connecter au serveur.")
    client.close()