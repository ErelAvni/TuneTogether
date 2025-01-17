from datetime import datetime
from socialUser import SocialUser
import DButilites

def get_last_id():
    users_dict = DButilites.load_data_from_json(DButilites.MESSAGE_DB_PATH)
    sorted_ids = sorted(users_dict.keys())
    return sorted_ids[-1]


class Message():
    def __init__(self, text: str, sender: SocialUser, time_stamp: datetime):
        self.__message_id = str(int(get_last_id()) + 1)
        self.__text = text
        self.__sender = sender
        self.__time_stamp = time_stamp


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
        return {
            'message_id': self.message_id,
            'text': self.text,
            'sender': self.sender.user_id,
            'timestamp': self.timestamp
        }