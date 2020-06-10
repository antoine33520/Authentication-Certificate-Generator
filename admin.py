#!/usr/bin/env python3
import socket, time
from getmac import get_mac_address as gma


host = "127.0.0.1"
port = 8080
name = 'Admin'
# Récupération de l'adresse MAC du client
mac_address = str(gma())

# Création du socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connexion du socket au serveur
client.connect((host, port))
print(name + " connecté au serveur")

message = mac_address
# Envoi du message vers le serveur
client.send(message.encode("utf-8"))
print('Client 1 : ' + message)
# Réception de la réponse du serveur
reponse = client.recv(255)
print(reponse.decode("utf-8"))
# Délai de connexion au server, ici 10 secondes
time.sleep(10)
# Fermeture de la connexion au serveur
print("Connexion fermée")
client.close()

#################################
######### RESTE A FAIRE #########
#################################
# envoie du certificat par le client à sa connexion