import socket
import threading


class TuneTogetherServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server started. Listening on {self.host}:{self.port}...")
        
        while True:
            conn_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client_request, args=(conn_socket, addr)).start()


    def handle_client_request(self, conn_socket, addr):
        with conn_socket:
            print(f"Connected by {addr}")
            while True:
                try:
                    data = conn_socket.recv(1024)
                    if not data:
                        break
                    request = data.decode('utf-8')
                    print(f"Received request from {addr}: {request}")
                    # Process the ServerRequest here

                except Exception as e:
                    print(f"Error handling request from {addr}: {e}")
                    break


    def add_comment(self, comment: str):
        pass


def main():
    server = TuneTogetherServer()
    server.start()


if __name__ == "__main__":
    main()