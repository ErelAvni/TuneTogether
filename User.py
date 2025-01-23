from hashlib import sha256
import DButilites
from chatHandler import ChatHandler


class User():
    def __init__(self, username: str, password: str, first_name: str, last_name: str, age: int):
        self.__username = username
        
        hash_obj = sha256()
        hash_obj.update(password.encode('utf-8'))
        
        self.__password_hash = hash_obj.hexdigest()

        self.__user_id = self.get_last_id() + 1

        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age

        self.__friends = []
        self.__friend_requests = []
        self.__private_chats = {} # {friend_id: Chat}
        self.__group_chats = {} # {friend_id: Chat}
        self.__chat_handler = ChatHandler(self)

    
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
    

    def to_dict(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age
        }
