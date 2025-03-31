import json


#CONSTS:
OK = "OK"
DATA_NOT_FOUND = "DATA_NOT_FOUND"
UNAUTHORIZED = "UNAUTHORIZED"
INVALID_REQUEST = "INVALID_REQUEST"
INVALID_DATA = "INVALID_DATA"
INTERNAL_ERROR = "INTERNAL_ERROR"


class ServerResponse:
    def __init__(self, response_code: str, message: str, username: str = None):
        """
        Initialize a ServerResponse object.

        :param response_code: string code of the result of the server's operation.
        :param message: A message providing additional information about the response.
        :param username: The username of the user connected to the server. Should only be used in the login or register request.
        """
        self.response_code = response_code
        self.message = message if message else response_code
        self.username = username


    def to_dict(self):
            """
            Convert the response to a dictionary for serialization.

            :return: A dictionary representation of the response.
            """
            if self.username:
                return {
                    "status_code": self.response_code,
                    "message": self.message,
                    "username": self.username
                }

            return {
                "status_code": self.response_code,
                "message": self.message,
            }


    def to_json(self):
        """
        Convert the response to a JSON string for transmission.

        :return: A JSON representation of the response.
        """
        return json.dumps(self.to_dict())
