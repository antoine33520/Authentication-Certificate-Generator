import socket
import ssl

PORT = 8080
hostname = "127.0.0.1"

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain('', '')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock1:
    sock1.bind((hostname, PORT))
    sock1.listen(5)
    with context.wrap_socket(sock1, server_side=True) as sock2:
        conn, addr = sock2.accept()
