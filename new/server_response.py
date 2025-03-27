import json


#CONSTS:
OK = "OK"
DATA_NOT_FOUND = "DATA_NOT_FOUND"
UNAUTHORIZED = "UNAUTHORIZED"
INVALID_REQUEST = "INVALID_REQUEST"
INVALID_DATA = "INVALID_DATA"
INTERNAL_ERROR = "INTERNAL_ERROR"


class ServerResponse:
    def __init__(self, response_code: str, message: str):
        """
        Initialize a ServerResponse object.

        :param response_code: string code of the result of the server's operation.
        :param message: A message providing additional information about the response.
        """
        self.response_code = response_code
        self.message = message if message else response_code


    def to_dict(self):
            """
            Convert the response to a dictionary for serialization.

            :return: A dictionary representation of the response.
            """
            return {
                "status_code": self.response_code,
                "message": self.message
            }


    def to_json(self):
        """
        Convert the response to a JSON string for transmission.

        :return: A JSON representation of the response.
        """
        return json.dumps(self.to_dict())
    

    def __str__(self):
        return f"ServerResponse(status_code={self.response_code}, message={self.message})"