import json
from new.shared.comment import Comment

# Request codes
LOGIN = "LOGIN"
REGISTER = "REGISTER"
LOGOUT = "LOGOUT"
DISCONNECT = "DISCONNECT"
LIVE_CHAT_MESSAGE = "LIVE_CHAT_MESSAGE"
GET_LIVE_CHAT_MESSAGES = "GET_LIVE_CHAT_MESSAGES"
ADD_COMMENT = "ADD_COMMENT"
GET_COMMENTS = "GET_COMMENTS"
GET_ALL_SONG_RATINGS = "GET_ALL_SONG_RATINGS"
UPDATE_SONG_RATING = "UPDATE_SONG_RATING"


class ServerRequest:
    """
    Represents a request sent by the client to the server.
    """

    def __init__(self, request_code, payload={}):
        """
        Initialize a ServerRequest instance.

        :param request_code: The type of request (e.g., COMMENT, LOGIN, REGISTER).
        :param payload: Additional data for the request.
        """
        self.request_code = request_code
        self.payload = payload


    @staticmethod
    def create_login_payload(username: str, password_hash: str):
        '''creates a payload for the login request. returns a ServerRequest object'''
        payload = {
            "username": username,
            "password_hash": password_hash
        }
        return ServerRequest(LOGIN, payload)
    

    @staticmethod
    def create_register_payload(username: str, password_hash: str, age: int):
        payload = {
            "username": username,
            "password_hash": password_hash, 
            "age": age
        }
        return ServerRequest(REGISTER, payload)
    

    @staticmethod
    def create_logout_payload(username: str):
        payload = {
            "username": username
        }
        return ServerRequest(LOGOUT, payload)
    
    
    def to_dict(self):
        """
        Convert the request to a dictionary for serialization.

        :return: A dictionary representation of the request.
        """
        return {
            "request_code": self.request_code,
            "payload": self.payload
        }


    def to_json(self):
        """
        Convert the request to a JSON string for transmission.

        :return: A JSON representation of the request.
        """
        return json.dumps(self.to_dict())
    

    def __str__(self):
        return f"ServerRequest(request_code={self.request_code}, payload={self.payload})"