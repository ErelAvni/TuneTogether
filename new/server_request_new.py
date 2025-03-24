import json

# Request codes
LOGIN = "LOGIN"
REGISTER = "REGISTER"
PLAY_SONG = "PLAY_SONG"
STOP_SONG = "STOP_SONG"
COMMENT = "COMMENT"

class ServerRequest:
    """
    Represents a request sent by the client to the server.
    """

    def __init__(self, request_code, payload=None):
        """
        Initialize a ServerRequest instance.

        :param request_code: The type of request (e.g., COMMENT, LOGIN, REGISTER).
        :param payload: Additional data for the request.
        """
        self.request_code = request_code
        self.payload = payload


    @staticmethod
    def create_login_payload(username: str, password_hash: str):
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