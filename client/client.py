from socket import *

#serverIP = '172.30.1.8'
#serverIP = '10.223.124.8'
serverIP = '127.0.0.1'
serverPort = 80

def create_socket_and_send_message():

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))

    print('-------------------- Request Number List --------------------')
    print('1 - GET /index.html HTTP/1.1')
    print('2 - GET /index.html HTTP/2.0')
    print('3 - GET /other.html HTTP/1.1')
    print('4 - HEAD /index.html HTTP/1.1')
    print('5 - HEAD /index.html HTTP/2.0')
    print('6 - HEAD /other.html HTTP/1.1')
    print('7 - POST /user.json HTTP/1.1 | body: "name": ljw, "age": 23')
    print('8 - POST /user.json HTTP/2.0 | body: "name": ljw, "age": 23')
    print('9 - POST /other.json HTTP/1.1 | body: "name": ljw, "age": 23')
    print('10 - PUT /user.json/2 HTTP/1.1 | body: "name": Hong gil dong, "age": 30')
    print('11 - PUT /user.json/1 HTTP/1.1 | body: "age": 47')
    print('12 - PUT /user.json/1 HTTP/2.0 | body: "age": 47')
    print('13 - PUT /other.json/1 HTTP/1.1 | body: "age": 47') 
    print('-------------------------------------------------------------')
    print()

    requestList = ['GET /index.html HTTP/1.1', 'GET /index.html HTTP/2.0', 'GET /other.html HTTP/1.1',
                   'HEAD /index.html HTTP/1.1', 'HEAD /index.html HTTP/2.0', 'HEAD /other.html HTTP/1.1',
                   'POST /user.json HTTP/1.1', 'POST /user.json HTTP/2.0', 'POST /other.json HTTP/1.1',
                   '10 - PUT /user.json/2 HTTP/1.1', 'PUT /user.json/1 HTTP/1.1', '12 - PUT /user.json/1 HTTP/2.0']
    requestNum = int(input('Please enter request number: '))
    print()

    if requestNum == 1:
        request_message = GET_200()
    elif requestNum == 2:
        request_message = GET_400()
    elif requestNum == 3:
        request_message = GET_404()
    elif requestNum == 4:
        request_message = HEAD_200()
    elif requestNum == 5:
        request_message = HEAD_400()
    elif requestNum == 6:
        request_message = HEAD_404()
    elif requestNum == 7:
        request_message = POST_201()
    elif requestNum == 8:
        request_message = POST_400()
    elif requestNum == 9:
        request_message = POST_404()
    elif requestNum == 10:
        request_message = PUT_201()
    elif requestNum == 11:
        request_message = PUT_200()
    elif requestNum == 12:
        request_message = PUT_400()
    elif requestNum == 13:
        request_message = PUT_404()
    
    request_message += 'Host: 172.30.1.8:12000\r\n'
    request_message += 'Connection: Keep-Alive\r\n'
    request_message += 'Cache-Control: max-age=0\r\n'
    if 1 <= requestNum <= 6:
        request_message += 'Accept: text/html\r\n'
    else:
        request_message += 'Accept: application/json\r\n'
    request_message += 'Accept-Charset: utf-8\r\n'
    request_message += 'Accept-Encoding: gzip, deflate\r\n'
    request_message += 'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n'

    clientSocket.send(request_message.encode('utf-8'))

    recieve_message = clientSocket.recv(65535).decode()
    print('[Message received from the server]')
    print(recieve_message)
    
    clientSocket.close()

def GET_200():
    request_message = 'GET /index.html HTTP/1.1\r\n'
    return request_message

def GET_400():
    request_message = 'GET /index.html HTTP/2.0\r\n'
    return request_message

def GET_404():
    request_message = 'GET /other.html HTTP/1.1\r\n'
    return request_message

def HEAD_200():
    request_message = 'HEAD /index.html HTTP/1.1\r\n'
    return request_message

def HEAD_400():
    request_message = 'HEAD /index.html HTTP/2.0\r\n'
    return request_message

def HEAD_404():
    request_message = 'HEAD /other.html HTTP/1.1\r\n'
    return request_message

def POST_201():
    request_message = 'POST /user.json HTTP/1.1\r\n'
    return request_message

if __name__ == '__main__':
    create_socket_and_send_message()
