from hashlib import sha256
import DButilites
from privatechatHandler import PrivateChatHandler


class User():
    def __init__(self, username: str, password: str, first_name: str, last_name: str, age: int,
                 user_id : str = None, friends : list = None, friend_requests : list = None, 
                 private_chats = None, group_chats = None,):
        self.__username = username
        
        hash_obj = sha256()
        hash_obj.update(password.encode('utf-8'))
        
        self.__password_hash = hash_obj.hexdigest()

        db_raw_id = DButilites.get_last_id(DButilites.MESSAGE_DB_PATH)
        self.__user_id = str(int(db_raw_id) + 1)

        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age

        self.__friends = []
        self.__friend_requests = []
        self.__private_chats = {} # {friend_id: Chat}
        self.__group_chats = {} # {name: Chat}
        self.__private_chat_handler = PrivateChatHandler(self)
        #TODO: add the group chat handler here

    
    @property
    def username(self):
        return self.__username
    
    
    @property
    def password_hash(self):
        return self.__password_hash
    

    @property
    def user_id(self):
        return self.__user_id
    

    @property
    def first_name(self):
        return self.__first_name
    

    @property
    def last_name(self):
        return self.__last_name
    

    @property
    def age(self):
        return self.__age


    @property
    def friends(self):
        return self.__friends


    @property
    def friend_requests(self):
        return self.__friend_requests


    @property
    def private_chats(self):
        return self.__private_chats


    @property
    def group_chats(self):
        return self.__group_chats
    

    @property
    def private_chat_handler(self):
        return self.__private_chat_handler


    def to_dict(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'friends': [friend.user_id for friend in self.friends],
            'friend_requests': [friend_request for friend_request in self.friend_requests],
            'private_chats': [private_chat.chat_id for private_chat in self.private_chats],
            'group_chats': [group_chat.chat_id for group_chat in self.group_chats],
            'private_chat_handler': self.private_chat_handler
        }
