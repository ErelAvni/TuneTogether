from chat import Chat
from User import User
from message import Message
import DButilites


class PrivateChat(Chat):
    def __init__(self, user1: User, user2: User, id: str = None, encryption_key=None, messages : list = None):
        """
        Creates a new private chat object. Params are in the following order:
        :param user1: the first user object
        :param user2: the second user object
        :param id: the unique chat id. If not provided, a new id will be generated. If provided it should be unique, in order to create an existing chat object
        :param encryption_key: the encryption key for the chat, expected to be 32 bytes long. If not provided, a new key will be generated. This is a parameter of the parent class
        :param messages: a list of the ids of the messages in the chat. If not provided, an empty list will be created. This is a parameter of the parent class
        """

        last_id = DButilites.get_last_id(DButilites.PRIVATE_CHAT_DB_PATH)
        id = str(int(last_id) + 1)
        super().__init__(id, encryption_key, messages)

        self.__user1 = user1
        self.__user2 = user2


    @property
    def user1(self):
        return self.__user1


    @property
    def user2(self):
        return self.__user2


    def add_message(self, msg):
        """
        Adds a message to the chat. The message is expected to be a Message object. The message will be added to the chat's messages list and the chat will be updated in the database
        """
        super().add_message(msg, DButilites.PRIVATE_CHAT_DB_PATH, self.to_dict())

    def to_dict(self):
        """
        Returns a dictionary with the chat data.
        All nested obejcts are saved only by their ids, so if using this method to create an instance the nested objects should be created first.
        """
        data_dict = super().to_dict()
        data_dict['user1'] = self.__user1.user_id
        data_dict['user2'] = self.__user2.user_id
        return data_dict


    @classmethod
    def from_dict(cls, data_dict: dict):
        """
        Creates a new private chat object from a dictionary. 
        The dictionary is expected to be the outut of the the to_dict method.
        """
        all_users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        user1 = User.from_dict(all_users[data_dict['user1']])
        user2 = User.from_dict(all_users[data_dict['user2']])

        chat_id = data_dict['chat_id']
        encryption_key = data_dict['encryption_key']

        all_messages = DButilites.load_data_from_json(DButilites.MESSAGE_DB_PATH)
        messages = [Message.from_dict(all_messages[message_id]) for message_id in data_dict['messages']]

        return PrivateChat(user1, user2, chat_id, encryption_key, messages)