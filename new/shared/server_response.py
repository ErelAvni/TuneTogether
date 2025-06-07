import json


#CONSTS:
OK = "OK"
DATA_NOT_FOUND = "DATA_NOT_FOUND"
UNAUTHORIZED = "UNAUTHORIZED"
INVALID_REQUEST = "INVALID_REQUEST"
INVALID_DATA = "INVALID_DATA"
INTERNAL_ERROR = "INTERNAL_ERROR"


class ServerResponse:
    def __init__(self, response_code: str, message: str, request_code: str = None, username: str = None, messages: list = None, song_ratings: dict = None):
        """
        Initialize a ServerResponse object.

        :param response_code: string code of the result of the server's operation.
        :param message: A message providing additional information about the response.
        :param request_code: The type of request that was made which the response is for (e.g., COMMENT, LOGIN, REGISTER ect).
        :param username: The username of the user connected to the server. Should only be used in the login or register request.
        :param messages: All of the messages in the live chat. Should only be used in the live chat request.
        :param song_ratings: All of the ratings for a song. Should only be used in the get_song_rating request. Should be a dictionary with usernames as keys and their ratings to the song as values.
        """
        self.response_code = response_code
        self.message = message if message else response_code
        self.request_code = request_code
        self.username = username
        self.messages = messages
        self.song_ratings = song_ratings


    def to_dict(self):
            """
            Convert the response to a dictionary for serialization.

            :return: A dictionary representation of the response.
            """
            if self.username:
                return {
                    "response_code": self.response_code,
                    "message": self.message,
                    "request_code": self.request_code,
                    "username": self.username, 
                }
            
            if self.messages:
                return {
                    "response_code": self.response_code,
                    "message": self.message,
                    "request_code": self.request_code,
                    "messages": [message.to_dict() for message in self.messages],
                }
            
            if self.song_ratings:
                 return {
                    "response_code": self.response_code,
                    "message": self.message,
                    "request_code": self.request_code,
                    "song_ratings": self.song_ratings,
                }

            return {
                "response_code": self.response_code,
                "message": self.message,
                "request_code": self.request_code,
            }


    def to_json(self):
        """
        Convert the response to a JSON string for transmission.

        :return: A JSON representation of the response.
        """
        return json.dumps(self.to_dict())
