#!/usr/bin/env python3
import socket

host = "127.0.0.1"	# Ici, le poste local
port = 8080	# Se connecter sur le port 8080
name = 'Client 1'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print("Connecté au serveur")

print("Tapez FIN pour terminer la conversation. ")
message = ""
while message.upper() != "FIN":
	message = input("> ")
	client.send(message.encode("utf-8"))
	reponse = client.recv(255)
	print(reponse.decode("utf-8"))

print("Connexion fermée")
client.close()