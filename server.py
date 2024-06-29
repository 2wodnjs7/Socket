from socket import *
from datetime import datetime, timezone, timedelta
import sys
import os.path

def inDir(url):
    dir = './server'
    dirLst = os.listdir(dir)
    bool = False
    for filename in dirLst:
        if filename in url:
            bool = True

    return bool
        

def readURL(url):
    dir = './server' + url
    msg = ''

    with open (dir, 'rt') as myfile:
        for line in myfile:
            msg += line
    
    return msg
    

if __name__ == '__main__':

    #serverIP = '172.30.1.8'
    serverIP = '10.223.124.8'
    #serverIP = '127.0.0.1'
    serverPort = 80
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))

    serverSocket.listen()
    print('The server is running')

    while True:
        connectionSocket, addr = serverSocket.accept()
        
        message = connectionSocket.recv(65535).decode().split()
        print(message)
        httpMethod = message[0].upper()

        msgDATE = 'Date: ' + str(datetime.now().strftime('%a, %d %b %Y %X %Z'))

        if httpMethod == 'GET':
            url = message[1]
            if inDir(url):
                msgURL = readURL(url)
                sendMessage = 'HTTP/1.1 200 OK\r\n'
                sendMessage += 'Content-Type: text/html\r\n'
                sendMessage += 'Content-Length: {}\r\n'.format(len(msgURL))
                sendMessage += msgDATE
                sendMessage += '\r\n\r\n'
                sendMessage += msgURL
            else:
                sendMessage = 'HTTP/1.1 404 Not Found\r\n'

        elif httpMethod == 'HEAD':
            url = message[1]
            if url == '/index.html':
                sendMessage = 'HTTP/1.1 100 Continue\r\n'
            else:
                sendMessage = 'HTTP/1.1 404 Not Found\r\n'

        #elif httpMethod == 'POST':

        #elif httpMethod == 'PUT':
        

        

        

        connectionSocket.send(sendMessage.encode('utf-8'))
        
