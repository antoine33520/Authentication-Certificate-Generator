import socket
import ssl

PORT = 8080
hostname = "127.0.0.1"
context = ssl.create_default_context()

with socket.create_connection((hostname, PORT)) as sock1:
    with context.wrap_socket(sock1, server_hostname=hostname) as sock2:
        print(sock2.version())