import socket
from server_request_new import ServerRequest
import json
from server_response import ServerResponse
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None #username of the connected user. if none, the client is not connected to any user


    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

            # Step 1: Receive server public key
            public_pem = self.client_socket.recv(1024)
            public_key = serialization.load_pem_public_key(public_pem)

            # Step 2: Generate Fernet key and encrypt it
            self.fernet_key = Fernet.generate_key()
            encrypted_fernet_key = public_key.encrypt(
                self.fernet_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Step 3: Send encrypted Fernet key to server
            self.client_socket.send(encrypted_fernet_key)
            self.fernet = Fernet(self.fernet_key)
            print("Secure Fernet key established.")

        except Exception as e:
            print(f"Failed to connect to server: {e}")


    def send_request(self, request: ServerRequest):
        try:
            # Send the request to the server
            request_json = request.to_json()
            byte_request = request_json.encode('utf-8')
            encrypted_request = self.fernet.encrypt(byte_request)
            self.client_socket.send(encrypted_request)
            # Wait for the server's response
            encrypted_response = self.client_socket.recv(2048)
            byte_response = self.fernet.decrypt(encrypted_response)
            response_json = byte_response.decode('utf-8')
            response_dict = json.loads(response_json)
            response = ServerResponse(
                response_dict['status_code'], 
                response_dict['message'], 
                response_dict['username'] if 'username' in response_dict else None, 
                response_dict['messages'] if 'messages' in response_dict else None)
            
            if 'username' in response_dict:
                self.username = response_dict['username']

            print("Request: ", request.to_dict())
            print("response: ", response.to_dict())
            return response

        except Exception as e:
            print(f"Error sending request: {e}")
            return None


    def close(self):
        """Close the client socket and disconnect from the server."""
        if self.username:  # If username is provided, send a logout request
            self.send_request(ServerRequest.create_logout_payload(self.username))
        try:
            # Send a DISCONNECT request before closing the socket
            disconnect_request = ServerRequest("DISCONNECT", {})
            response = self.send_request(disconnect_request)
            if response:
                print(f"Server response to DISCONNECT: {response.response_code} - {response.message}")
            else:
                print("No response received for DISCONNECT request.")
        except Exception as e:
            print(f"Error sending DISCONNECT request: {e}")
        finally:
            self.client_socket.close()

