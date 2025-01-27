from chat import Chat
from User import User
import DButilites
from message import Message


class GroupChat(Chat):
    def __init__(self, creator : User, name : str):
        last_id = DButilites.get_last_id(DButilites.GROUP_CHAT_DB_PATH)
        id = str(int(last_id) + 1)
        super().__init__(id)
        self.__name = name
        self.__creator = creator
        self.__users = [creator]
        self.__managers = {creator.user_id: True} #this is in order to check if someone is manager or not in O(1) time complexity


    @property
    def name(self):
        return self.__name


    @property
    def creator(self):
        return self.__creator


    @property
    def users(self):
        return self.__users


    @property
    def managers(self):
        return self.__managers


    def add_message(self, msg: Message):
        super().add_message(msg, DButilites.GROUP_CHAT_DB_PATH, self.to_dict())


    def add_user(self, user : User):
        self.__users.append(user)
        DButilites.save_data_to_json(DButilites.GROUP_CHAT_DB_PATH, self.to_dict())


    def to_dict(self):
        data_dict = super().to_dict()
        data_dict['creator'] = self.__creator.user_id
        data_dict['users'] = [self.__users.user_id for user in self.__users]
        data_dict['users'] = self.__managers
        return data_dict

