from socket import *
from datetime import datetime, timezone, timedelta
import json, os.path

# server 폴더 안에 client가 요청한 파일이 있는지 확인하는 함수
def inDir(url):
    dir = './server'
    dirLst = os.listdir(dir)
    bool = False
    for filename in dirLst:
        if filename in url:
            bool = True

    return bool
        
# client가 요청한 파일을 읽어서 msg에 저장하는 함수
def readURL(url):
    dir = './server' + url
    msg = ''

    with open (dir, 'rt') as myfile:
        for line in myfile:
            msg += line
    
    return msg
    
if __name__ == '__main__':

    print('The server is running')
    print()

    #serverIP = '172.30.1.8' # home main
    #serverIP = '10.223.124.8' # laptop main
    #serverIP = '172.24.68.21' # home wsl
    serverIP = '127.0.0.1' # loopback
    serverPort = 80
    
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))
    serverSocket.listen()
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        
        try:
            print('[Message received from the client]')

            # client에게 받은 message를 출력하기 위해 먼저 '\r\n'으로 Parsing 한다.
            # '\r\n'으로 Parsing된 message를 다시 공백문자를 기준으로 Parsing 한다.
            # 처음부터 공백문자를 기준으로 Parsing하면 server에서 출력하는데 어려움이 있기 때문에 이런 방식으로 진행한다.
            message = connectionSocket.recv(65535).decode().split('\r\n')
            parsedMessage = []
            for i in message:
                print(i)
                for j in i.split():
                    parsedMessage.append(j)
        
            httpMethod = parsedMessage[0].upper()   # httpMethod = client의 http request Method
            url = parsedMessage[1]                  # url = client의 http request url
            version = parsedMessage[2]              # version = client의 http request http version

            
            msgDATE = 'Date: ' + str(datetime.now().strftime('%a, %d %b %Y %X %Z'))     # response 에 담을 현재 DATE 정보를 저장
            
            print(parsedMessage)
            
            if httpMethod == 'GET' or httpMethod == 'HEAD':     # GET과 HEAD의 차이점은 body가 있고 없고의 차이일 뿐이기에 묶어서 구현한다.

                # version이 http 1.1이 아닐경우 응답코드 400 Bad Request 설정 및 BadRequest.html를 읽어 msgURL에 저장
                if version != "HTTP/1.1":   
                    sendMessage = 'HTTP/1.1 400 Bad Request\r\n'
                    msgURL = readURL('/BadRequest.html')

                # client가 요청한 파일이 있는 경우 응답코드 200 OK 설정 및 요청파일을 읽어 msgURL에 저장
                elif inDir(url): 
                    sendMessage = 'HTTP/1.1 200 OK\r\n'
                    msgURL = readURL(url)

                # client가 요청한 파일이 없는 경우 응답코드 404 Not Found 설정 및 NotFound.html를 읽어 msgURL에 저장
                else:
                    sendMessage = 'HTTP/1.1 404 Not Found\r\n'
                    msgURL = readURL('/NotFound.html')
                
                # http header 
                sendMessage += msgDATE + '\r\n'
                sendMessage += 'Server: Apache\r\n'
                sendMessage += 'Content-Type: text/html; charset=utf-8\r\n'
                sendMessage += 'Content-Length: {}'.format(len(msgURL))

                # http Method 가 GET이면 body에 client가 요청한 파일 저장, HEAD면 skip
                if httpMethod == 'GET':
                    sendMessage += '\r\n\r\n'
                    sendMessage += msgURL
                elif httpMethod == 'HEAD':
                    pass

            
            elif httpMethod == 'POST' or httpMethod == 'PUT': # POST와 PUT의 차이점은 멱등성의 차이일 뿐이기에 큰 틀에서 묶어서 구현한다.
                path = './server/user.json'

                with open(path, "r") as json_file:
                    json_data = json.load(json_file)

                


            


            connectionSocket.send(sendMessage.encode('utf-8'))
            

        # 예외 발생 시 연결된 소켓 끊기
        except Exception as err:
            connectionSocket.close()
            break
    
        # 모든 작업이 종료 후 연결 끊기
        finally:
            connectionSocket.close()
            break 

            
        
