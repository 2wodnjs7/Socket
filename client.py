from socket import *

serverIP = '172.30.1.8'
#serverIP = '10.223.124.8'
#serverIP = '127.0.0.1'
serverPort = 80

def create_socket_and_send_message():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))
    clientSocket.send(request_message.encode('utf-8'))

    recieve_message = clientSocket.recv(65535).decode()
    print(recieve_message)
    
    clientSocket.close()



request_message = 'GET /index.html HTTP/1.1\r\n'
request_message += 'Host: 172.30.1.8:12000\r\n'
#request_message += 'Connection: Keep-Alive\r\n'
#request_message += 'Cache-Control: max-age=0\r\n'
request_message += 'Accept: text/html\r\n\r\n'
#request_message += 'Accept-Encoding: gzip, deflate\r\n'
#request_message += 'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n'

#request_message += 'Host: 127.0.0.1:80\r\n'
#request_message += 'Host: 172.24.68.21:80\r\n'

create_socket_and_send_message()
