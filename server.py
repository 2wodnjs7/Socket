from socket import *   # python socket programming을 위해 사용
from datetime import datetime, timezone, timedelta  # http response heeader의 data 정보를 표현하기 위해 사용 
import json, os.path, sys   # json: json 파일 사용 / os.path: server 폴더에 client가 요청한 파일이 있는지 확인 / sys: 출력 버퍼링을 없애기 위해 사용

#serverIP = '0.0.0.0'   # public IP   
serverIP = '127.0.0.1'  # loopback
serverPort = 80         # HTTP port

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

# POST, PUT request로 인해 json파일에 user를 새로 추가하는 함수
# id는 POST과 PUT의 구별을 위해 사용 (id가 없으면 POST, 있으면 POST)
def userAppend(path, json_data, item_dic, id=0):
    
    # id가 파라미터로 전달되지 않았을 경우 새로 추가될 user의 id를 정하는 로직
    # 새로 추가될 user의 id는 현재 json파일에 저장된 유저들 중 [가장 큰 id + 1] 로 설정
    if id == 0:
        max = 0
        for i in json_data['user']:
            if max < i['id']:
                max = i['id']
        id = max + 1

    # 추가될 유저 정보를 json_data에 추가
    json_data['user'].append({
        "id": int(id),
        "name": item_dic["name"],
        "age": int(item_dic["age"])
    })

    # json 형식에 맞춰 msgBody를 설정
    msgBody = "{\r\n" 
    msgBody += "  \"id\": {},\r\n".format(id)
    msgBody += "  \"name\": {},\r\n".format(item_dic["name"])
    msgBody += "  \"age\": {}\r\n".format(item_dic["age"])
    msgBody += "}"

    # 유저정보가 추가된 json_data를 다시 json파일에 저장
    with open(path, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

    return msgBody



if __name__ == '__main__':

    print('[The server is running]')
    print()
    sys.stdout.flush()                                  # 출력이 buffering 되지 않도록 사용

    serverSocket = socket(AF_INET, SOCK_STREAM)         # 서버 소켓 생성 
    serverSocket.bind((serverIP, serverPort))           # 서버 바인딩   : 소켓을 서버 IP, Port에 바인딩
    serverSocket.listen()                               # 서버 리스닝   : 클라이언트 연결을 대기
    connectionSocket, addr = serverSocket.accept()      # 연결 수락     : 클라이언트 연결을 수락 및 클라이언트와 연결할 새로운 소켓 생성
    print('[Connected to the client.]')
    print()
    print('[Waiting for client\'s request..]')
    print()
    sys.stdout.flush()                                  # 출력이 buffering 되지 않도록 사용

    while True:
        try:
            print('[Message received from the client]')
            
            # client에게 받은 데이터를 decode하여 message에 저장 / message를 출력하기 위해 먼저 '\r\n'으로 Parsing 한다.
            # '\r\n'으로 Parsing된 message를 다시 공백문자를 기준으로 Parsing 한다.
            # 처음부터 공백문자를 기준으로 Parsing하면 server에서 출력하는데 어려움이 있기 때문에 이런 방식으로 진행한다.
            message = connectionSocket.recv(65535).decode().split('\r\n')
            body = message[-3].split(',')
            parsedMessage = []
            for i in message:
                print(i)
                for j in i.split():
                    parsedMessage.append(j)
        
            httpMethod = parsedMessage[0].upper()   # httpMethod = client의 http request Method
            url = parsedMessage[1]                  # url = client의 http request url
            version = parsedMessage[2]              # version = client의 http request http version


            msgDATE = 'Date: ' + str(datetime.now().strftime('%a, %d %b %Y %X %Z'))     # response 에 담을 현재 DATE 정보를 저장
            
            if httpMethod == 'GET' or httpMethod == 'HEAD':     # GET과 HEAD의 차이점은 body가 있고 없고의 차이일 뿐이기에 묶어서 구현한다.

                # version이 http 1.1이 아닐경우 응답코드 400 Bad Request 설정 및 BadRequest.html를 읽어 msgBody에 저장
                if version != "HTTP/1.1":   
                    sendMessage = 'HTTP/1.1 400 Bad Request\r\n'
                    msgBody = readURL('/BadRequest.html')

                # client가 요청한 파일이 있는 경우 응답코드 200 OK 설정 및 요청파일을 읽어 msgBody에 저장
                elif inDir(url): 
                    sendMessage = 'HTTP/1.1 200 OK\r\n'
                    msgBody = readURL(url)

                # client가 요청한 파일이 없는 경우 응답코드 404 Not Found 설정 및 NotFound.html를 읽어 msgBody에 저장
                else:
                    sendMessage = 'HTTP/1.1 404 Not Found\r\n'
                    msgBody = readURL('/NotFound.html')
                
                # http header 
                sendMessage += msgDATE + '\r\n'
                sendMessage += 'Server: Apache\r\n'
                sendMessage += 'Content-Type: text/html; charset=utf-8\r\n'
                sendMessage += 'Content-Length: {}\r\n\r\n'.format(len(msgBody))

                # http Method 가 GET이면 body에 client가 요청한 파일 저장, HEAD면 skip
                if httpMethod == 'GET':
                    sendMessage += msgBody
                elif httpMethod == 'HEAD':
                    pass

            elif httpMethod == 'POST':
                msgBody = ""
                
                # version이 http 1.1이 아닐경우
                if version != "HTTP/1.1":
                    sendMessage = 'HTTP/1.1 400 Bad Request\r\n'

                # client가 요청한 파일이 있는 경우 
                elif inDir(url):
                    path = './server' + url
                    
                    with open(path, "r") as json_file:      # json 파일 읽기
                        json_data = json.load(json_file)
                    
                    # request의 body를 parsing하여 dictionary로 저장
                    item_dic = {}
                    for item in body:
                        item_list = item.replace(" ","").replace("\"", "").split(':')
                        item_dic[item_list[0]] = item_list[1]

                    # 새로운 유저를 추가하는 함수를 호출하고, response의 body를 저장
                    msgBody = userAppend(path, json_data, item_dic)
                    
                    sendMessage = 'HTTP/1.1 201 Created\r\n'

                # client가 요청한 파일이 없는 경우
                else:
                    sendMessage = 'HTTP/1.1 404 Not Found\r\n'
                
                # http header 
                sendMessage += msgDATE + '\r\n'
                sendMessage += 'Server: Apache\r\n'
                sendMessage += 'Content-Type: application/json; charset=utf-8\r\n'
                sendMessage += 'Content-Length: {}\r\n\r\n'.format(len(msgBody))
                sendMessage += msgBody
            
            elif httpMethod == 'PUT':
                msgBody = ""
                curr_id = int(url.split('/')[-1])   # url에서 PUT될 user id를 파싱
                
                # version이 http 1.1이 아닐경우
                if version != "HTTP/1.1":
                    sendMessage = 'HTTP/1.1 400 Bad Request\r\n'
                
                # client가 요청한 파일이 있는 경우
                elif inDir(url):
                    # url에서 PUT될 user id를 제거한 문자열을 다시 설정하여 server의 경로 설정
                    path = './server' + '/' + '/'.join(url.split('/')[1:len(url.split('/'))-1])     
                    
                    with open(path, "r") as json_file:      # json 파일 읽기
                        json_data = json.load(json_file)
                    
                    # request의 body를 parsing하여 dictionary로 저장
                    item_dic = {}
                    for item in body:
                        item_list = item.replace(" ","").replace("\"", "").split(':')
                        item_dic[item_list[0]] = item_list[1]
                    

                    # PUT될 curr_id가 이미 json파일에 있을 경우 수정, 없을 경우 새로 추가하는 로직
                    # bool 변수로 수정이 된 경우 새로 추가 X, 수정이 안 된 경우 새로 추가 O
                    bool = True
                    for i in range(len(json_data['user'])):
                        if json_data['user'][i]['id'] == curr_id:
                            if 'name' in item_dic:
                                json_data['user'][i]['name'] = item_dic['name']
                            if 'age' in item_dic:
                                json_data['user'][i]['age'] = int(item_dic['age'])
                            with open(path, 'w') as outfile:
                                json.dump(json_data, outfile, indent=4)
                            bool = False
                    
                    # 수정이 안 된 경우 유저를 새로 추가하는 함수를 호출하고, 201 Created 메시지를 저장
                    if bool:
                        msgBody = userAppend(path, json_data, item_dic, curr_id)
                        sendMessage = 'HTTP/1.1 201 Created\r\n'

                    # 수정된 경우 204 No Content 메시지를 저장
                    else:
                        sendMessage = 'HTTP/1.1 204 No Content\r\n'
                
                # client가 요청한 파일이 없는 경우
                else:
                    sendMessage = 'HTTP/1.1 404 Not Found\r\n'

                # http header 
                sendMessage += msgDATE + '\r\n'
                sendMessage += 'Server: Apache\r\n'
                sendMessage += 'Content-Type: application/json; charset=utf-8\r\n'
                sendMessage += 'Content-Length: {}\r\n\r\n'.format(len(msgBody))
                sendMessage += msgBody

            # 각 client request 마다 출력이 buffering 되지 않도록 사용
            sys.stdout.flush()

            # 각 로직에 따라 구성된 sendMessage를 client에게 전송
            connectionSocket.send(sendMessage.encode('utf-8'))

            # HTTP 1.1의 특성을 살려 Connection: Keep-Alive 일 경우 소켓 연결을 끊지 않고 계속 유지하는 로직 
            keep_alive = True
            for i in range(len(parsedMessage)):
                if parsedMessage[i] == "Connection:":
                    if parsedMessage[i+1] == "close":
                        keep_alive = False
                    break
            
            # keep_alive가 아닐 경우 client와 연결된 socket 연결 종료 및 프로그램 종료
            if not keep_alive:
                connectionSocket.close()
                break
                

        # 예외 발생 시 연결된 소켓 연결 끊기 및 프로그램 종료
        except Exception as err:
            connectionSocket.close()
            break