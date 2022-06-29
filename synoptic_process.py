import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 52415  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = input()
    while True:
        s.sendall(bytes(json.dumps(data).encode()))
        data_rcv = json.loads(s.recv(1024))
        print(f"{data_rcv}")

