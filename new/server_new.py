import socket
import threading
import json
from server_request_new import ServerRequest, LOGIN, REGISTER, PLAY_SONG, STOP_SONG, COMMENT, LOGOUT, DISCONNECT
import db.DButilites as DButilites
from server_response import ServerResponse, OK, DATA_NOT_FOUND, UNAUTHORIZED, INVALID_REQUEST, INVALID_DATA, INTERNAL_ERROR
from googleapiclient.discovery import build
import os
from song import Song
import dotenv
dotenv.load_dotenv()


YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


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
                        response_json = self.login_user(request.payload['username'], request.payload['password_hash'])

                    elif request.request_code == REGISTER:
                        response_json = self.register_user(request.payload['username'], request.payload['password_hash'], request.payload['age'])

                    elif request.request_code == LOGOUT:
                        response_json = self.logout_user(request.payload['username'])

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


    def login_user(self, username: str, password_hash: str):
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
                    response = ServerResponse(OK, f"User {username} logged in.", username)
                print(f"User {username} logged in.")

        return response.to_json()


    def register_user(self, username: str, password_hash: str, age: int):
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
            response = ServerResponse(OK, f"User {username} registered.", username).to_json()
        
        else:
            response = ServerResponse(INVALID_DATA, "Error while registering user.").to_json()
        
        return response


    def logout_user(self, username: str):
        """Handles the logout request from the client."""
        if username not in self.connected_users:
            response = ServerResponse(INVALID_DATA, f"User {username} is not connected.")
            return response.to_json()

        self.connected_users.remove(username)
        print(f"User {username} logged out.")
        response = ServerResponse(OK, f"User {username} logged out.").to_json()
        return response


    def disconnect_client(self, conn_socket):
        """
        Handle client disconnection.
        """
        response = ServerResponse("OK", "Client disconnected.")
        response_json = response.to_json()

        try:
            # Send the response to the client
            conn_socket.send(response_json.encode('utf-8'))
            print(f"Sent disconnect response: {response_json}")

            # Allow time for the client to receive the response
            conn_socket.shutdown(socket.SHUT_WR)  # Shutdown the write side of the socket
        except Exception as e:
            print(f"Error sending disconnect response: {e}")
        finally:
            # Remove the client from the connected clients list and close the socket
            if conn_socket in self.connected_clients:
                self.connected_clients.remove(conn_socket)
            conn_socket.close()
            print("Client socket closed.")

    
    #-----------song playing methods-------------------


    def search_song(self, query: str):
        '''Search for a song on YouTube using the provided query.
        :param query: The search query for the song (should be the song's name).
        :return: The URL of the first matching song to the search query.
        '''
        search_response = YOUTUBE.search().list(
            q=query,                   # Search query (song name)
            part="snippet",            # Request snippet data (title, ID, etc.)
            type="video",              # Only look for videos (not channels/playlists)
            videoCategoryId="10",      # Filter results to category 10 (Music)
            maxResults=1               # Get only the top result
        ).execute()

        # Extract video ID from the API response
        if search_response["items"]:
            song_id = search_response["items"][0]["id"]["videoId"]
            song_url = f"https://www.youtube.com/watch?v={song_id}"
            return song_url
        
        return None  # Return None if no result found


def main():
    server = TuneTogetherServer()
    server.start()


if __name__ == "__main__":
    main()