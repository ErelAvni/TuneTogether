import socket
from server_request_new import ServerRequest
import json
from hashlib import sha256


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))  # Connect in the constructor


    def send_request(self, request: ServerRequest):
        try:
            request_json = request.to_json()
            self.client_socket.sendall(request_json.encode('utf-8'))  # Send the request
            
            
        
            '''Receive the response from the server. The response is yet to be determined (type-structure wise).
            TODO: Determine the structure of the response and update the code accordingly.'''
            # response_json = self.client_socket.recv(1024).decode('utf-8')  # Receive the response
            # response_dict = json.loads(response_json)
            # response = ServerRequest(response_dict['request_code'], response_dict['payload'])
            # return response
        
        except Exception as e:
            return f"An error occurred: {e}"


    def close(self):
        self.client_socket.close()  # Close the connection when done


if __name__ == "__main__":
    client = Client()
    try:
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