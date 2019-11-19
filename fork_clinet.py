from socket import *

s = socket()
s.connect(('127.0.0.1', 10000))

while True:
    data = input('>>')
    s.send(data.encode())
s.close()
