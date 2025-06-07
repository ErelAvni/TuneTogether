import socket
from new.shared.server_request_new import ServerRequest
import json
from new.shared.server_response import ServerResponse
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import threading
from new.shared.comment import Comment


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None #username of the connected user. if none, the client is not connected to any user
        self.lock = threading.Lock()  # Lock for thread-safe operations


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


    def send_request(self, request: ServerRequest) -> ServerResponse:
        with self.lock:  # Ensure thread-safe access to the socket
            try:
                # Send initial request
                request_json = request.to_json()
                byte_request = request_json.encode('utf-8')
                encrypted_request = self.fernet.encrypt(byte_request)
                self.client_socket.send(encrypted_request)

                # First response (handshake start)
                encrypted_response = self.client_socket.recv(2048)
                byte_response = self.fernet.decrypt(encrypted_response)
                response_json = byte_response.decode('utf-8')
                response_dict = json.loads(response_json)

                if response_dict["request_code"] != request.request_code:
                    print(f"Request code mismatch: {response_dict['request_code']} != {request.request_code}")
                    raise Exception(f"Expected response for {request.request_code}, but got {response_dict['request_code']}")

                if (request.request_code == "GET_LIVE_CHAT_MESSAGES" or request.request_code == "GET_COMMENTS") and response_dict["message"] == "Ready to send chunks":
                    return self._receive_message_chunks()

                response = ServerResponse(
                    response_dict['response_code'], 
                    response_dict['message'], 
                    response_dict['request_code'],
                    response_dict['username'] if 'username' in response_dict else None)
                
                if response_dict['response_code'] == "OK" and request.request_code == "LOGOUT":
                    self.username = None

                if 'username' in response_dict:
                    self.username = response_dict['username']

                if 'messages' in response_dict:
                    response.messages = [Comment.from_dict(message) for message in response_dict['messages']]
            
                print(f"Server response: {response.response_code} - {response.message}")
                return response
            
            except Exception as e:
                print(f"Error sending request: {e}")
                return None


    def _receive_message_chunks(self):
        try:
            # Step 3: send OK to server
            ok_response = ServerResponse("OK", "OK")
            self.client_socket.send(self.fernet.encrypt(ok_response.to_json().encode('utf-8')))

            all_messages = []

            while True:
                encrypted_chunk = self.client_socket.recv(2048)
                if not encrypted_chunk:
                    return ServerResponse("INTERNAL_ERROR", "No data received from server.")

                chunk_json = self.fernet.decrypt(encrypted_chunk).decode('utf-8')
                chunk_dict = json.loads(chunk_json)

                if chunk_dict["message"] == "DONE":
                    break

                chunk_messages = [Comment.from_dict(m) for m in chunk_dict.get("messages", [])]
                all_messages.extend(chunk_messages)

            return ServerResponse("OK", "All messages retrieved", messages=all_messages)

        except Exception as e:
            print(f"Error receiving message chunks: {e}")
            return ServerResponse("INTERNAL_ERROR", "Error during message chunk reception")


    def close(self):
        """Close the client socket and disconnect from the server."""
        if self.username:  # If username is provided, send a logout request
            self.send_request(ServerRequest.create_logout_payload(self.username))
        try:
            # Send a DISCONNECT request before closing the socket
            disconnect_request = ServerRequest("DISCONNECT", {})
            response = self.send_request(disconnect_request)
        except Exception as e:
            print(f"Error sending DISCONNECT request: {e}")
        finally:
            self.client_socket.close()

