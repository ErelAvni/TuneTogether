import socket
from server_request_new import ServerRequest
import json
from hashlib import sha256
from server_response import ServerResponse


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")


    def send_request(self, request: ServerRequest):
        try:
            # Send the request to the server
            request_json = request.to_json()
            self.client_socket.send(request_json.encode('utf-8'))
            print(f"Sent request: {request_json}")

            # Wait for the server's response
            response_data = self.client_socket.recv(1024)
            print(f"Received response: {response_data}")
            response_json = response_data.decode('utf-8')
            response_dict = json.loads(response_json)
            response = ServerResponse(response_dict['status_code'], response_dict['message'])
            return response

        except Exception as e:
            print(f"Error sending request: {e}")
            return None


    def close(self):
        self.client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    client = Client()
    try:
        client.connect()
        request_code = input("Enter your request code for the server: ")
        if request_code == "LOGIN":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            password_hash = sha256(password.encode('utf-8')).hexdigest()
            request = ServerRequest.create_login_payload(username, password_hash)
        elif request_code == "REGISTER":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            password_hash = sha256(password.encode('utf-8')).hexdigest()
            age = int(input("Enter your age: "))
            request = ServerRequest.create_register_payload(username, password_hash, age)
            print(request)
        else:
            print("Invalid request code. Please enter either 'LOGIN' or 'REGISTER'.")
            raise ValueError("Invalid request code")        

        print(client.send_request(request))  # Send the request to the server

    finally:
        client.close()  # Ensure the connection is closed