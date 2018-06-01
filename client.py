import socket

s = socket.socket()
host = '192.168.5.25'
port = 8080
s.connect((host, port))
print(s.recv(1024))
s.close()
