import socket


class socketServer:
    def __init__(self, srv_port, listen_num):
        self.port = srv_port
        self.listen = listen_num
        self.mySock = None

    # sock 생성
    def create_sock(self):
        self.serverSock = socket.socket(socketServer.AF_INET, socketServer.SOCK_STREAM)
        self.serverSock.bind(("0.0.0.0", int(self.port)))
        self.serverSock.listen(int(self.listen))
        return self.serverSock

    # client 대기
    def ready_for_client(self):
        return self.serverSock.accept()

    # sock 반환
    def get_sock(self):
        return self.serverSock