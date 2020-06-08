import http.client

PORT = 8080
url = " "
connection = http.client.HTTPConnection(url, PORT, timeout=10)
print(connection)