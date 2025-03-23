class ServerRequest:
    """
    Represents a request sent by the client to the server.
    """
    # Request codes
    PLAY_SONG = "PLAY_SONG"
    STOP_SONG = "STOP_SONG"
    COMMENT = "COMMENT"
    LOGIN = "LOGIN"
    REGISTER = "REGISTER"

    def __init__(self, request_code, payload=None):
        """
        Initialize a ServerRequest instance.

        :param request_code: The type of request (e.g., COMMENT, LOGIN, REGISTER).
        :param payload: Additional data for the request (optional).
        """
        if request_code not in {self.COMMENT, self.LOGIN, self.REGISTER}:
            raise ValueError(f"Invalid request code: {request_code}")

        self.__request_code = request_code
        if payload:
            self.__payload = payload
        else:
            self.__payload = ""

    def to_dict(self):
        """
        Convert the request to a dictionary for serialization.

        :return: A dictionary representation of the request.
        """
        return {
            "request_code": self.__request_code,
            "payload": self.__payload
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a ServerRequest instance from a dictionary.

        :param data: A dictionary containing request data.
        :return: A ServerRequest instance.
        """
        return ServerRequest(data['request_code'], data['payload'])