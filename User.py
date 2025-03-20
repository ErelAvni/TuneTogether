from hashlib import sha256
import db.DButilites as DButilites
from privateChat import PrivateChat
from groupChat import GroupChat
from privatechatHandler import PrivateChatHandler
from friendRequest import FriendRequest
from groupChatHandler import GroupChatHandler


class User():
    def __init__(self, username: str, password: str, first_name: str, last_name: str, age: int,
                 user_id : str = None, friends : list = None, friend_requests : list = None, 
                 private_chats : list = None, group_chats : list = None, called_from_from_dict : bool = False):
        """
        Creates a new user object. Params are in the following order:
        :param username: the username of the user
        :param password: the password of the user. It will be hashed using sha256
        :param first_name: the first name of the user
        :param last_name: the last name of the user
        :param age: the age of the user
        :param user_id: the unique id of the user. Should be unique and only provided if using the from_dict method. If not provided, it will be generated
        :param friends: a list of the user's friends. Should only be provided if using the from_dict method. If not provided, an empty list will be created
        :param friend_requests: a list of the user's friend requests. Should only be provided if using the from_dict method. If not provided, an empty list will be created
        :param private_chats: a list of the user's private chats. Should only be provided if using the from_dict method. If not provided, an empty list will be created
        :param group_chats: a list of the user's group chats. Should only be provided if using the from_dict method. If not provided, an empty list will be created
        :param called_from_from_dict: a boolean that indicates if the method was called from the from_dict method. Should not be provided by the user
        """
        self.__username = username

        if called_from_from_dict:
            self.__password_hash = password
        else:
            hash_obj = sha256()
            hash_obj.update(password.encode('utf-8'))
            self.__password_hash = hash_obj.hexdigest()

        db_raw_id = DButilites.get_last_id(DButilites.USER_DB_PATH)
        self.__user_id = str(int(db_raw_id) + 1)

        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age

        if friends:
            self.__friends = friends
        else:
            self.__friends = []
        
        if friend_requests:
            self.__friend_requests = friend_requests
        else:
            self.__friend_requests = []
        
        if private_chats:
            self.__private_chats = private_chats
        else:
            self.__private_chats = []
        
        if group_chats:
            self.__group_chats = group_chats
        else:
            self.__group_chats = []
        
        self.__private_chat_handler = PrivateChatHandler(self)
        self.__group_chat_handler = GroupChatHandler(self)

    
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


    @property
    def group_chat_handler(self):
        return self.__group_chat_handler


    def to_dict(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'friends': [friend.user_id for friend in self.friends],
            'friend_requests': [friend_request.to_dict() for friend_request in self.friend_requests],
            'private_chats': [private_chat.chat_id for private_chat in self.private_chats],
            'group_chats': [group_chat.chat_id for group_chat in self.group_chats]
        }


    @classmethod
    def from_dict(cls, data_dict: dict):
        """
        returns a new User object from a dictionary. data_dict is expected to be the output of the to_dict method.
        """
        username = data_dict['username']
        password_hash = data_dict['password_hash']
        user_id = data_dict['user_id']
        first_name = data_dict['first_name']
        last_name = data_dict['last_name']
        age = data_dict['age']
        
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        friends = [User.from_dict(users[friend_id]) for friend_id in data_dict['friends']]

        friend_requests = [FriendRequest.from_dict(friend_request) for friend_request in data_dict['friend_requests']]

        all_private_chats = DButilites.load_data_from_json(DButilites.PRIVATE_CHAT_DB_PATH)
        private_chats = [PrivateChat.from_dict(all_private_chats[chat_id]) for chat_id in data_dict['private_chats']]
        all_group_chats = DButilites.load_data_from_json(DButilites.GROUP_CHAT_DB_PATH)
        Group_chats = [GroupChat.from_dict(all_group_chats[chat_id]) for chat_id in data_dict['group_chats']]

        return User(username, password_hash, first_name, last_name, age, user_id, friends, friend_requests, private_chats, Group_chats, True)
