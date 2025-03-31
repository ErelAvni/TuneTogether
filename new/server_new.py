import socket
import threading
import json
from server_request_new import ServerRequest, LOGIN, REGISTER, PLAY_SONG, STOP_SONG, COMMENT, LOGOUT, DISCONNECT
import db.DButilites as DButilites
from server_response import ServerResponse, OK, DATA_NOT_FOUND, UNAUTHORIZED, INVALID_REQUEST, INVALID_DATA, INTERNAL_ERROR


class TuneTogetherServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_users = [] # list of connected users' usernames
        self.connected_clients = [] # list of connected clients' sockets


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
            self.connected_clients.append(conn_socket)
            while True:
                try:
                    data = conn_socket.recv(1024)
                    if not data:
                        break
                    request_json = data.decode('utf-8')
                    request_dict = json.loads(request_json)
                    request = ServerRequest(request_dict['request_code'], request_dict['payload'])
                    print(f"Received request from {addr}: {request}")
                    # Process the ServerRequest here
                    request = ServerRequest(request_dict['request_code'], request_dict['payload'])

                    if request.request_code == LOGIN:
                        response_json = self.login_user(request.payload['username'], request.payload['password_hash'], conn_socket)

                    elif request.request_code == REGISTER:
                        response_json = self.register_user(request.payload['username'], request.payload['password_hash'], request.payload['age'], conn_socket)

                    elif request.request_code == LOGOUT:
                        response_json = self.logout_user(request.payload['username'], conn_socket)

                    elif request.request_code == DISCONNECT:
                        response_json = self.disconnect_client(conn_socket)
                        print("response sending: ", response_json)

                        break

                    else:
                        response = ServerResponse(INVALID_REQUEST, "Invalid request code.")
                        response_json = response.to_json()

                    
                    print("response sending: ", response_json)
                    conn_socket.send(response_json.encode('utf-8'))

                except Exception as e:
                    print(f"Error handling request from {addr}: {e}")
                    break

    
    def connect_user(self, username: str):
        if username in self.connected_users:
            print(f"User {username} is already connected.")
            return False
        
        self.connected_users.append(username)
        print(f"User {username} connected.")
        return True


    def login_user(self, username: str, password_hash: str, conn_socket):
        """Handles the login request from the client."""
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)

        if username not in users:
            response = ServerResponse(DATA_NOT_FOUND, f"User {username} not found.")

        else:
            user = users[username]
            if user['password_hash'] != password_hash:
                response = ServerResponse(UNAUTHORIZED, "Invalid password.")
            
            else:
                if not self.connect_user(username):
                    response = ServerResponse(INVALID_DATA, f"User {username} is already connected.")
                else:
                    response = ServerResponse(OK, f"User {username} logged in.")
                print(f"User {username} logged in.")

        return response.to_json()


    def register_user(self, username: str, password_hash: str, age: int, conn_socket):
        """Handles the registration request from the client."""
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)

        if username in users:
            resopnse = ServerResponse(INVALID_DATA, f"Username \"{username}\" already taken.")
            return resopnse.to_json()
        
        if not self.connect_user(username):
            response = ServerResponse(INVALID_DATA, f"User {username} is already connected.")
            return response.to_json()

        user_dict = {
            "username": username,
            "password_hash": password_hash,
            "age": age
        }

        if (DButilites.update_data_to_json(user_dict, DButilites.USER_DB_PATH)):
            print(f"User {username} registered.")
            response = ServerResponse(OK, f"User {username} registered.").to_json()
        
        else:
            response = ServerResponse(INVALID_DATA, "Error while registering user.").to_json()
        
        return response


    def logout_user(self, username: str, conn_socket):
        """Handles the logout request from the client."""
        if not self.connect_user(username):
            response = ServerResponse(INVALID_DATA, f"User {username} is not connected.")
            return response.to_json()

        del self.connected_users[username]
        print(f"User {username} logged out.")
        response = ServerResponse(OK, f"User {username} logged out.").to_json()
        return response


    def disconnect_client(self, conn_socket):
        print("entered disconnect_client")
        """Disconnects the client from the server."""
        # Remove the client from the list of connected clients
        if conn_socket in self.connected_clients:
            self.connected_clients.remove(conn_socket)
            print("Client disconnected1.")
        else:
            print("Client not found in connected clients.")
            return
        conn_socket.close()
        print("Client disconnected2.")
        return ServerResponse(OK, "Client disconnected.").to_json()


def main():
    server = TuneTogetherServer()
    server.start()


if __name__ == "__main__":
    main()