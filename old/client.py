import socket
import select
import msvcrt  # For keyboard input in Windows
from datetime import datetime
import sys
import logging
from old.User import User
from old.message import Message

class Client:
    def __init__(self, user: User, host='127.0.0.1', port=12345):
        self.user = user
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages_to_send = []
        self.log_in = 0

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")

    def login(self):
        if self.log_in == 0:
            user_name = self.user.username
            now = datetime.now()
            time = now.strftime("%H:%M")
            header = f"{time};{user_name};0;".encode()
            message = header + b"verify user"
            print(message)
            self.messages_to_send.append((self.socket, message))
            self.log_in = 1

    def send_message(self, message_text: str):
        message = Message(message_text, self.user.username)
        try:
            self.socket.sendall(message.text.encode('utf-8'))
            print(f"Sent message: {message.text}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def receive_message(self):
        try:
            response = self.socket.recv(1024).decode('utf-8')
            print(f"Received message: {response}")
            return response
        except Exception as e:
            print(f"Failed to receive message: {e}")
            return None

    def close(self):
        try:
            self.socket.close()
            print("Connection closed")
        except Exception as e:
            print(f"Failed to close connection: {e}")

    def run(self):
        self.connect()
        self.login()
        while True:
            rlist, wlist, xlist = select.select([self.socket], [self.socket], [])
            for current_socket in rlist:
                if current_socket is self.socket:
                    data = self.receive_message()
                    if data:
                        print(data)
            for current_socket in wlist:
                if self.messages_to_send:
                    message = self.messages_to_send.pop(0)
                    self.send_message(message[1].decode())

if __name__ == "__main__":
    user = User(username="john_doe", password="password", first_name="John", last_name="Doe", age=30)
    client = Client(user)
    client.run()