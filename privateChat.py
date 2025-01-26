from chat import Chat
from User import User
import DButilites


class PrivateChat(Chat):
    def __init__(self, user1: User, user2: User, encryption_key=None):
        db_raw_id = DButilites.get_last_id(DButilites.MESSAGE_DB_PATH)
        id = str(int(db_raw_id) + 1)
        super().__init__(id, encryption_key)
        self.__user1 = user1
        self.__user2 = user2


    @property
    def user1(self):
        return self.__user1


    @property
    def user2(self):
        return self.__user2


    def add_message(self, msg):
        super().add_message(msg, DButilites.PRIVATE_CHAT_DB_PATH, self.to_dict())

    def to_dict(self):
        data_dict = super().to_dict()
        data_dict['user1'] = self.__user1.user_id
        data_dict['user2'] = self.__user2.user_id
        return data_dict
