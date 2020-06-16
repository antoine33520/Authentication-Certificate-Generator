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
name = 'Admin'
# Récupération de l'adresse MAC et de l'uuid de la carte mère du client
mac_address = str(gma())
uuid = get_motherboard_uuid()


# Création du socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connexion du socket au serveur
client.connect((host, port))
print("Demande de connection envoyée pour : " + name)

# Envoi du message vers le serveur avec la mac pour authentification
message = mac_address
client.sendall(message.encode("utf-8"))
print(name + " : " + message)
# Réception de la réponse du serveur
reponse = client.recv(255)
print("Server : " + reponse.decode("utf-8"))
if reponse == 'OK':
    print(name + " est connecté au server")
    # Délai de connexion au server, ici 10 secondes
    time.sleep(10)
    # Fermeture de la connexion au serveur
    print("Connexion fermée")
    client.close()
else :
    print(name + " n'est pas autorisé à se connecter au serveur.")
    client.close()

################################
######## RESTE A FAIRE #########
################################
# envoie du certificat par le client à sa connexion