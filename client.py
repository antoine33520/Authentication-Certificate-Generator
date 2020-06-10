#!/usr/bin/env python3
import socket
from getmac import get_mac_address as gma
import time

host = "127.0.0.1"	# Ici, le poste local
port = 8080	# Se connecter sur le port 8080
name = 'Client 1'
mac_address = str(gma())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print(name + " connecté au serveur")

message = mac_address
client.send(message.encode("utf-8"))
print('Client 1 : ' + message)
reponse = client.recv(255)
print(reponse.decode("utf-8"))

t = time.time()
while t == 100:
    print("Connexion fermée")
    client.close()