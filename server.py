from socket import *
from datetime import datetime
import sys

#serverIP = '172.30.1.8'
#serverIP = '10.223.124.8'
serverIP = '127.0.0.1'
serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))

serverSocket.listen()
print('The server is running')

while True:
    connectionSocket, addr = serverSocket.accept()
    
    message = connectionSocket.recv(65535).decode()
    print(message)
    connectionSocket.send(message[::-1].encode('utf-8'))
        
