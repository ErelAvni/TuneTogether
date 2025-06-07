from dotenv import load_dotenv, dotenv_values
import os, sys

# Load environment variables from .env file
here = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(here, "..", ".."))  # Adjust the path to your project root
load_dotenv(os.path.join(project_root, "new", ".env"))

if project_root not in sys.path:
    sys.path.append(project_root)
    sys.path.insert(0, project_root)

import socket
import threading
import json
from new.shared.server_request_new import ServerRequest, LOGIN, REGISTER, LOGOUT, DISCONNECT, GET_LIVE_CHAT_MESSAGES, LIVE_CHAT_MESSAGE, ADD_COMMENT, GET_COMMENTS, GET_ALL_SONG_RATINGS
import new.shared.DButilites as DButilites
from new.shared.server_response import ServerResponse, OK, DATA_NOT_FOUND, UNAUTHORIZED, INVALID_REQUEST, INVALID_DATA, INTERNAL_ERROR
from new.shared.comment import Comment
from googleapiclient.discovery import build
import os
import socket, threading, json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
import time


YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


class TuneTogetherServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_users = [] # list of connected users' usernames
        self.connected_clients = [] # list of connected clients' sockets
        self.live_chat_messages = [ Comment("server", "Welcome to TuneTogether!") ]


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

            # Step 1: Generate RSA key pair
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            public_key = private_key.public_key()

            # Step 2: Send the public key to the client
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            conn_socket.send(public_pem)  # send to client

            # Step 3: Receive the encrypted Fernet key from the client
            encrypted_fernet_key = conn_socket.recv(512)
            fernet_key = private_key.decrypt(
                encrypted_fernet_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            fernet = Fernet(fernet_key)
            print("Secure Fernet key established.")

            while True:
                try:
                    data = conn_socket.recv(2048)
                    if not data:
                        break
                    # Decrypt the received data using Fernet
                    decrypted_data = fernet.decrypt(data)
                    request_json = decrypted_data.decode('utf-8')
                    request_dict = json.loads(request_json)
                    request = ServerRequest(request_dict['request_code'], request_dict['payload'])
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
                        break
                    
                    elif request.request_code == GET_LIVE_CHAT_MESSAGES:
                        response_json = self.get_live_chat_messages(conn_socket, fernet) # send messages in chunks inside the function

                    elif request.request_code == LIVE_CHAT_MESSAGE:
                        response_json = self.add_message_to_live_chat(Comment.from_dict(request.payload))
                    
                    elif request.request_code == ADD_COMMENT:
                        response_json = self.add_comment_to_comment_db(Comment.from_dict(request.payload['comment']), request.payload['song_name'])

                    elif request.request_code == "GET_COMMENTS":
                        response_json = self.get_comments_for_song(request.payload['song_name'], conn_socket, fernet)
                    
                    elif request.request_code == "GET_ALL_SONG_RATINGS":
                        response_json = self.get_all_song_ratings(request.payload['song_name'])
                    
                    elif request.request_code == "UPDATE_SONG_RATING":
                        response_json = self.update_song_rating(request.payload['song_name'], request.payload['username'], request.payload['rating'])

                    else:
                        response = ServerResponse(INVALID_REQUEST, "Invalid request code.")
                        response_json = response.to_json()
                    
                    # Encrypt the response using Fernet
                    encrypted_response = fernet.encrypt(response_json.encode('utf-8'))
                    print(f"Sending response: {response_json}")
                    conn_socket.send(encrypted_response)

                except Exception as e:
                    print(f"Error handling request from {addr}: {e}")
                    response = ServerResponse(INTERNAL_ERROR, "An error occurred while processing the request.")
                    encrypted_response = fernet.encrypt(response.to_json().encode('utf-8'))
                    conn_socket.send(encrypted_response)
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
        print(DButilites.USER_DB_PATH)

        if username not in users:
            response = ServerResponse(DATA_NOT_FOUND, f"User {username} not found.", LOGIN)

        else:
            user = users[username]
            if user['password_hash'] != password_hash:
                response = ServerResponse(UNAUTHORIZED, "Invalid password.", LOGIN)
            
            else:
                if not self.connect_user(username):
                    response = ServerResponse(INVALID_DATA, f"User {username} is already connected.", LOGIN)
                else:
                    response = ServerResponse(OK, f"User {username} logged in.", LOGIN, username)
                print(f"User {username} logged in.")

        return response.to_json()


    def register_user(self, username: str, password_hash: str, age: int):
        """Handles the registration request from the client."""
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)

        if username in users:
            resopnse = ServerResponse(INVALID_DATA, f"Username \"{username}\" already taken.", REGISTER)
            return resopnse.to_json()
        
        if not self.connect_user(username):
            response = ServerResponse(INVALID_DATA, f"User {username} is already connected.", REGISTER)
            return response.to_json()

        user_dict = {
            "username": username,
            "password_hash": password_hash,
            "age": age
        }

        if (DButilites.update_data_to_json(user_dict, DButilites.USER_DB_PATH)):
            print(f"User {username} registered.")
            response = ServerResponse(OK, f"User {username} registered.", REGISTER, username).to_json()
        
        else:
            response = ServerResponse(INVALID_DATA, "Error while registering user.", REGISTER).to_json()
        
        return response


    def logout_user(self, username: str):
        """Handles the logout request from the client."""
        if username not in self.connected_users:
            response = ServerResponse(INVALID_DATA, f"User {username} is not connected.", LOGOUT)
            return response.to_json()

        self.connected_users.remove(username)
        print(f"User {username} logged out.")
        response = ServerResponse(OK, f"User {username} logged out.", LOGOUT).to_json()
        return response


    def disconnect_client(self, conn_socket):
        """
        Handle client disconnection.
        """
        response = ServerResponse("OK", "Client disconnected.", DISCONNECT)
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

    
    def add_message_to_live_chat(self, message: Comment):
        """Adds a message to the live chat.
        """
        self.live_chat_messages.append(message)
        response = ServerResponse(OK, "Message added to live chat.", LIVE_CHAT_MESSAGE)
        return response.to_json()


    def get_live_chat_messages(self, conn_socket, fernet):
        """Returns all messages in the live chat in a response json."""
        all_messages = self.live_chat_messages  # get all messages
        response = ServerResponse(OK, "Ready to send chunks", GET_LIVE_CHAT_MESSAGES)
        conn_socket.send(fernet.encrypt(response.to_json().encode('utf-8')))

        # Wait for client's OK before proceeding
        client_response_encrypted = conn_socket.recv(2048)
        client_response_json = fernet.decrypt(client_response_encrypted).decode('utf-8')
        client_response = json.loads(client_response_json)
        if client_response["response_code"] == "OK" and client_response["message"] == "OK":
            print("Client is ready to receive chunks.")
            MAX_PER_PACKET = 10

            for i in range(0, len(all_messages), MAX_PER_PACKET):
                chunk = all_messages[i:i + MAX_PER_PACKET]
                chunk_response = ServerResponse(OK, "CHUNK", GET_LIVE_CHAT_MESSAGES, messages=chunk)
                print(f"Sending chunk: {chunk_response.to_dict()}")
                conn_socket.send(fernet.encrypt(chunk_response.to_json().encode('utf-8')))
                time.sleep(0.05)  # Optional: avoid packet merging

            # Final DONE message
            done_response = ServerResponse(OK, "DONE", GET_LIVE_CHAT_MESSAGES)
            return done_response.to_json()


    def add_comment_to_comment_db(self, comment: Comment, song_name: str):
        """Adds a comment to the comments database.
        """
        if not comment or not song_name:
            response = ServerResponse(INVALID_DATA, "Comment or song name is missing.", ADD_COMMENT)
            return response.to_json()
        
        all_comments = DButilites.load_data_from_json(DButilites.COMMENTS_PATH)
        song_comments = all_comments[song_name]
        song_comments.append(comment.to_dict())
        DButilites.update_data_to_json(all_comments, DButilites.COMMENTS_PATH, manual_update=True)

        response = ServerResponse(OK, "Comment added successfully.", ADD_COMMENT)
        return response.to_json()


    def get_comments_for_song(self, song_name: str, conn_socket, fernet):
        """Returns all comments for a given song."""
        if not song_name:
            response = ServerResponse(INVALID_DATA, "song name is missing.", GET_COMMENTS)
            return response.to_json()
        
        all_messages = DButilites.load_data_from_json(DButilites.COMMENTS_PATH)[song_name]
        response = ServerResponse(OK, "Ready to send chunks", GET_COMMENTS)
        conn_socket.send(fernet.encrypt(response.to_json().encode('utf-8')))

        # Wait for client's OK before proceeding
        client_response_encrypted = conn_socket.recv(2048)
        client_response_json = fernet.decrypt(client_response_encrypted).decode('utf-8')
        client_response = json.loads(client_response_json)
        if client_response["response_code"] == "OK" and client_response["message"] == "OK":
            print("Client is ready to receive chunks.")
            MAX_PER_PACKET = 10

            for i in range(0, len(all_messages), MAX_PER_PACKET):
                chunk = all_messages[i:i + MAX_PER_PACKET]
                for j in range(len(chunk)):
                    chunk[j] = Comment.from_dict(chunk[j])
                chunk_response = ServerResponse(OK, "CHUNK", GET_COMMENTS, messages=chunk)
                print(f"Sending chunk: {chunk_response}")
                conn_socket.send(fernet.encrypt(chunk_response.to_json().encode('utf-8')))
                print("sent chunk")
                time.sleep(0.05)  # Optional: avoid packet merging

            # Final DONE message
            done_response = ServerResponse(OK, "DONE", GET_COMMENTS)
            return done_response.to_json()


    def get_all_song_ratings(self, song_name: str):
        """Returns all song ratings from the database."""
        print(f"Getting all ratings for song: {song_name}")
        all_ratings = DButilites.load_data_from_json(DButilites.SONG_RATINGS_PATH)[song_name]
        response = ServerResponse(OK, "All song ratings retrieved.", GET_ALL_SONG_RATINGS, song_ratings=all_ratings)
        return response.to_json()


    def update_song_rating(self, song_name: str, username: str, rating: int):
        """Updates the rating for a song by a user."""
        all_ratings = DButilites.load_data_from_json(DButilites.SONG_RATINGS_PATH)
        if song_name not in all_ratings:
            all_ratings[song_name] = {}
        all_ratings[song_name][username] = rating
        if DButilites.update_data_to_json(all_ratings, DButilites.SONG_RATINGS_PATH, manual_update=True):
            response = ServerResponse(OK, "Song rating updated successfully.", "UPDATE_SONG_RATING")
        else:
            response = ServerResponse(INTERNAL_ERROR, "Error updating song rating.", "UPDATE_SONG_RATING")
        return response.to_json()


def main():
    # pass ip and port as arguments, otehrwise using localhost and 65432
    server = TuneTogetherServer('192.168.1.142', 65432) 
    server.start()


if __name__ == "__main__":
    main()