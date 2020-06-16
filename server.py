#!/usr/bin/env python3
import socket
import threading
from getmac import get_mac_address as gma


port = 8080
host = '127.0.0.1'

threadsClients = []

def instanceServeur (client, infosClient):
	adresseIP = infosClient[0]
	port = str(infosClient[1])
	print("Instance de serveur prêt pour " + adresseIP + ":" + port)
	client.send("Server : Message reçu".encode("utf-8"))
	print("Connexion fermée avec " + adresseIP + ":" + port)
	client.close()

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((host, port))
print("Serveur prêt, en attente de requêtes ...")
serveur.listen(5) # max 5 connexions acceptées en parallèles
# réception de la mac du client
mac_address = serveur.recv(255).decode("utf-8")
print("Message reçu du client : " + mac_address)
if mac_address == '18:31:bf:12:94:2d':
	print("Connexion acceptée avec l'Admin !")
	client, infosClient = serveur.accept()
	threadsClients.append(threading.Thread(None, instanceServeur, None, (client, infosClient), {}))
	threadsClients[-1].start()
else :
	print("Connexion refusée avec l'Intru !")

serveur.close()

def drotis():
	pass

#################################
######### RESTE A FAIRE #########
#################################
# autoriser l'acces seulement aux MAC connues
# donner les droits à chaque client