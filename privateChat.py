from chat import Chat
import DButilites

def get_last_id():
    users_dict = DButilites.load_data_from_json(DButilites.PRIVATE_CHAT_DB_PATH)
    sorted_ids = sorted(users_dict.keys())
    return sorted_ids[-1]


class PrivateChat(Chat):
    def __init__(self, user1, user2):
        id = str(int(get_last_id()) + 1)
        super().__init__(id)
        self.__user1 = user1
        self.__user2 = user2


    @property
    def user1(self):
        return self.__user1


    @property
    def user2(self):
        return self.__user2


    def add_message(self, msg):
        super().add_message(msg, DButilites.PRIVATE_CHAT_DB_PATH)

    def to_dict(self):
        data_dict = super().to_dict()
        data_dict['user1'] = self.__user1.user_id
        data_dict['user2'] = self.__user2.user_id
        return data_dict
