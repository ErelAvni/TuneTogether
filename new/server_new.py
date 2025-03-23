import socket
import threading
import json
import os
import db.DButilites as DButilites


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


    def login(self, username: str, password_hash: str):
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        
        if username not in users:
            print(f"User {username} not found.")
            return False
        
        user = users[username]
        if user['password_hash'] != password_hash:
            print(f"Invalid password for user {username}.")
            return False
        
        print(f"User {username} logged in.")
        return True


def main():
    server = TuneTogetherServer()
    server.start()


if __name__ == "__main__":
    main()