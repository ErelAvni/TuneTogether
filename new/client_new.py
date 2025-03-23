import socket
from server_request_new import ServerRequest
from hashlib import sha256


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))  # Connect in the constructor

    def send_request(self, request: ServerRequest):
        try:
            # Send the request to the server
            self.client_socket.send(request.encode('utf-8'))
            
            # Receive the response from the server
            response = self.client_socket.recv(1024).decode('utf-8')
            
            return response
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
        else:
            print("Invalid request code. Please enter either 'LOGIN' or 'REGISTER'.")
            raise ValueError("Invalid request code")        


    finally:
        client.close()  # Ensure the connection is closed