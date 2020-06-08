import http.server
import socketserver

PORT = 8080 # Port utilisé
handler = http.server.SimpleHTTPRequestHandler # Gestionnaire simple utilisé

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("le serveur utilise le port", PORT)
    httpd.serve_forever() # méthode qui démarre le serveur, commence à écouter et répond aux demandes entrantes