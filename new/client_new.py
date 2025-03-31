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


    def close(self, username: str = None):
        """Close the client socket and disconnect from the server."""
        if username: ## If username is provided, send a logout request, otherwise skip (means that the app is closing without a user thats logged in)
            self.send_request(ServerRequest.create_logout_payload(username))
        try:
            # Send a DISCONNECT request before closing the socket
            disconnect_request = ServerRequest("DISCONNECT", {})
            self.send_request(disconnect_request)
        except Exception as e:
            print(f"Error sending DISCONNECT request: {e}")
        finally:
            self.client_socket.close()
            print("Connection closed.")
