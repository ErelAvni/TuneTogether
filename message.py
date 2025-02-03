from datetime import datetime
from User import User
import DButilites


class Message():
    def __init__(self, text: str, sender: User, time_stamp: datetime = None, message_id: str = None):
        """
        Creates a new message object. 
        :param text: The text of the message.
        :param sender: The user object of the sender.
        :param time_stamp: The date-time the message was sent
        :param message_id: The unique id of the message. If not provided, it will be generated.
        """
        db_raw_id = DButilites.get_last_id(DButilites.MESSAGE_DB_PATH)
        self.__message_id = str(int(db_raw_id) + 1)
        self.__text = text
        self.__sender = sender
        if time_stamp:
            self.__time_stamp = time_stamp
        else:
            time_stamp = datetime.now()


    @property
    def message_id(self):
        return self.__message_id


    @property
    def text(self):
        return self.__text
    

    @property
    def sender(self):
        return self.__sender
    

    @property
    def time_stamp(self):
        return self.__time_stamp
    

    def to_dict(self):
        """
        Retuns a dictionary representation of the message object.
        Any nested objects will be saved only by their euniqe id.
        """
        return {
            'message_id': self.message_id,
            'text': self.text,
            'sender': self.sender.user_id,
            'timestamp': self.time_stamp.isoformat()
        }
    

    @classmethod
    def from_dict(data_dict: dict):
        """
        class method that creates a new Message object from a dictionary.
        Dictionary is expected to be the output of the to_dict method.
        """
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        sender = User.from_dict(users[data_dict['sender']])

        message_id = data_dict['message_id']
        text = data_dict['text']
        time_stamp = datetime.fromisoformat(data_dict['timestamp'])
        return Message(text, sender, time_stamp, message_id)