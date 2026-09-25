import socket


HOST = "localhost"
PORT = 8080


client = socket.create_connection(
    (HOST, PORT)
)

requests = [
    "GET /add?a=2&b=3 HTTP/1.1\r\nHost: localhost\r\n\r\n",
    "GET /sub?a=10&b=4 HTTP/1.1\r\nHost: localhost\r\n\r\n",
    "GET /mul?a=6&b=7 HTTP/1.1\r\nHost: localhost\r\n\r\n",
    "GET /div?a=9&b=3 HTTP/1.1\r\nHost: localhost\r\n\r\n",
]

for req in requests:
    client.sendall(req.encode())

    response = client.recv(4096)

    print(response.decode())
    print("-" * 50)

client.close()