from chat import Chat
from User import User
import DButilites
from message import Message


class GroupChat(Chat):
    def __init__(self, name : str, creator : User, id : str = None,
                  users : list = None, managers : dict = None,
                    encryption_key : bytes = None, messages : list = None):
        """
        Creates a new group chat object. Params are in the following order:
        :param name: the name of the chat
        :param creator: the user that created the chat. Expected to be the user object, not the user id. Therefore, if using the from_dict method, the user object should be created first  
        :param id: the unique chat id. If not provided, a new id will be generated. If provided it should be unique, in order to create an existing chat object
        :param users: a list of the users (objects, not ids) in the chat. If not provided, an empty list will be created
        :param managers: a dictionary with the user ids as keys and a boolean as value. If the value is True, the user is a manager. If not provided, the creator is the only manager
        :param encryption_key: the encryption key for the chat, expected to be 32 bytes long. If not provided, a new key will be generated. This is a parameter of the parent class
        :param messages: a list of the ids of the messages in the chat. If not provided, an empty list will be created. This is a parameter of the parent class
        """
        last_id = DButilites.get_last_id(DButilites.GROUP_CHAT_DB_PATH)
        id = str(int(last_id) + 1)
        super().__init__(id, encryption_key, messages)

        self.__name = name
        self.__creator = creator

        if users:
            self.__users = users
        else:
            self.__users = [creator]

        if managers:
            self.__managers = managers
        else:
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
        """
        Adds a message to the chat. Gives the path for the group chat database and the data to be saved
        """
        super().add_message(msg, DButilites.GROUP_CHAT_DB_PATH, self.to_dict())


    def add_user(self, user : User):
        """
        Adds a user to the chat. Saves the data to the group chat database
        """
        self.__users.append(user)
        DButilites.update_data_to_json(DButilites.GROUP_CHAT_DB_PATH, self.to_dict())


    def to_dict(self):
        """
        Returns a dictionary with the chat data.
        All nested obejcts are saved only by their ids, so if using this method to create an instance the nested objects should be created first.
        """
        data_dict = super().to_dict()
        data_dict['name'] = self.__name
        data_dict['creator'] = self.__creator.user_id
        data_dict['users'] = [self.__users.user_id for user in self.__users]
        data_dict['managers'] = self.__managers
        return data_dict


    @classmethod
    def from_dict(cls, data_dict : dict):
        """
        Creates a group chat object from a dictionary.
        data_dict is expected to be the output of the to_dict method.
        """
        all_users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        creator = User.from_dict(all_users[data_dict['creator']])
        users = [User.from_dict(all_users[user_id]) for user_id in data_dict['users']]
        managers = data_dict['managers']

        name = data_dict['name']
        chat_id = data_dict['chat_id']
        encryption_key = data_dict['encryption_key']

        all_messages = DButilites.load_data_from_json(DButilites.MESSAGE_DB_PATH)
        messages = [Message.from_dict(all_messages[message_id]) for message_id in data_dict['messages']]

        return GroupChat(name, creator, chat_id, users, managers, encryption_key, messages)