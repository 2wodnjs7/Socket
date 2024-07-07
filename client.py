from socket import *

#serverIP = ''                  # external IP
serverIP = '127.0.0.1'          # loopback
serverPort = 80

# 소켓 생성 및 보낼 메시지를 정하는 함수
def create_socket_and_send_message():
    clientSocket = socket(AF_INET, SOCK_STREAM)     # 클라이언트 소켓 생성
    clientSocket.connect((serverIP, serverPort))    # 특정 서버 IP, Port에 연결 요청
    print('[Connected to the server.]')

    while True:
        # request할 http 구문을 미리 배열에 저장하여 사용
        # POST, PUT의 경우 body를 함께 저장
        requestList = ['', ('GET /index.html HTTP/1.1'), ('GET /index.html HTTP/2.0'), ('GET /other.html HTTP/1.1'),
                           ('HEAD /index.html HTTP/1.1'), ('HEAD /index.html HTTP/2.0'), ('HEAD /other.html HTTP/1.1'),
                           ('POST /user.json HTTP/1.1', '"name": "ljw", "age": 23'), 
                           ('POST /user.json HTTP/2.0', '"name": "ljw", "age": 23'),
                           ('POST /other.json HTTP/1.1', '"name": "ljw", "age": 23'),
                           ('PUT /user.json/2 HTTP/1.1', '"name": "Hong gil dong", "age": 30'),
                           ('PUT /user.json/2 HTTP/1.1', '"age": 15'),
                           ('PUT /user.json/1 HTTP/2.0', '"age": 47'),
                           ('PUT /other.json/1 HTTP/1.1', '"age": 47')]
        print()
        print('------------------------- Request Number List --------------------')
        for i in range(1, len(requestList)):
            if len(requestList[i]) != 2:   # body가 없는 GET, HEAD 
                print('%d - %s'%(i, requestList[i]))
            elif len(requestList[i]) == 2: # body가 있는 POST, PUT
                print('%d - %s %s'%(i, requestList[i][0], requestList[i][1]))
        print('------------------------------------------------------------------')
        print()

        # 출력되는 requestList에 해당하는 requestNum을 입력받음
        # 계속 request 할 경우에 대한 입력을 keep_alive 에 받음
        requestNum = int(input('Please enter request number: '))
        keep_alive = input('Do you want to stay connected?[y/n]: ')
        print()

        # 입력받은 requestNum, keep_alive 유효성 확인
        if 1 > requestNum or len(requestList)-1 < requestNum and keep_alive not in ('y', 'n'):
            print('[Invalid number.]')
            continue

        # 1 <= requestNum <= 6은 body가 없는 GET, HEAD / 그 외에는 body가 있는 POST, PUT
        # 입력받은 requestNum에 맞는 request를 request_message에 저장
        if 1 <= requestNum <= 6:
            request_message = requestList[requestNum] + '\r\n'
        else:
            request_message = requestList[requestNum][0] + '\r\n'
        
        # http response header 
        request_message += 'Host: ' + serverIP + ':' + str(serverPort) + '\r\n'             # Host: server의 도메인을 입력
        if keep_alive == 'y':                                                               # Connection: HTTP 1.1의 특성 중 하나인 TCP Connection을 계속 유지할 지 정하는 헤더
            request_message += 'Connection: Keep-Alive\r\n'                                 # 입력받은 keep_alive가 'y'면 Connection: Keep-Alive
        elif keep_alive == 'n':
            request_message += 'Connection: close\r\n'                                      # 입력받은 keep_alive가 'n'면 Connection: close
        request_message += 'Cache-Control: max-age=0\r\n'                                   # Cache_Control: 불필요한 데이터 요청을 줄이기 위해 사용하는 헤더
        if 1 <= requestNum <= 6:                                                            # Accept: client에서 받을데이터 형식
            request_message += 'Accept: text/html\r\n'                                      # GET, HEAD는 text/html
        else:
            request_message += 'Accept: application/json\r\n'                               # POST, PUT는 application/json
        request_message += 'Accept-Charset: utf-8\r\n'                                      # Accept-Charset: 클라이언트가 지원하는 문자 인코딩을 알리는 헤더
        request_message += 'Accept-Encoding: gzip, deflate\r\n'                             # Accept-Encoding: 요청에 대한 응답 메시지에 승인되는 인코딩을 표시하기 위한 헤더
        request_message += 'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n'   # Accept-Language: 클라이언트가 서버로부터 받고자 하는 언어를 나타내는 헤더
        
        # POST, PUT의 경우 body field 추가
        if requestNum >= 7:
            request_message += '{\r\n  ' + requestList[requestNum][1] + '\r\n}\r\n'

        # 각 로직에 따라 구성된 request_message를 server에게 전송
        clientSocket.send(request_message.encode('utf-8'))

        # server에게 송신받은 데이터를 decode하여 저장
        recieve_message = clientSocket.recv(65535).decode()
        print('[Message received from the server]')
        print(recieve_message)

        # keep_alive가 'n'이면 연결 종료
        if keep_alive == 'n':
            break
    
    # client 소켓 연결 종료 및 프로그램 종료
    clientSocket.close()

if __name__ == '__main__':
    create_socket_and_send_message()