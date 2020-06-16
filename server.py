#!/usr/bin/env python3
import socket, threading, time
from getmac import get_mac_address as gma


port = 8080
host = '127.0.0.1'
threadsClients = []

def instanceServeur (client, infosClient):
	adresseIP = infosClient[0]
	port = str(infosClient[1])
	print("Instance de serveur prêt pour " + adresseIP + ":" + port)
	# réception de la mac du client
	mac_address = client.recv(255).decode("utf-8")
	print("Message reçu du client : " + mac_address)
	if mac_address == '18:31:bf:12:94:2d':
		print("Connexion acceptée avec l'Admin !")
		reponse = 'Connexion acceptée !'
		client.sendall(reponse.encode('utf-8'))
		# Délai de connexion au server, ici 10 secondes
		time.sleep(10)
		# Fermeture de la connexion au serveur
		print("Connexion fermée")
		client.close()
	else :
		print("Connexion refusée avec l'Intru !")
		reponse = 'Connexion refusée !'
		client.sendall(reponse.encode('utf-8'))
		client.close()

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((host, port))
print("Serveur prêt, en attente de requêtes ...")
serveur.listen(5) # max 5 connexions acceptées en parallèles

while True:
	client, infosClient = serveur.accept()
	threadsClients.append(threading.Thread(None, instanceServeur, None, (client, infosClient), {}))
	threadsClients[-1].start()

serveur.close()




#################################
######### RESTE A FAIRE #########
#################################
# autoriser l'acces seulement aux MAC connues
# donner les droits à chaque client