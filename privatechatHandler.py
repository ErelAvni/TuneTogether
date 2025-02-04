from User import User
from privateChat import PrivateChat
import DButilites


class PrivateChatHandler:
    def __init__(self, user: User):
        """
        Creates a private chat handler for the user. 
        This handler is exclusive to the user and is used to manage the private chats of the user.
        :param User: the user that the handler is created for. User should pass itself by reference in 
        it's constructor, giving the handler access to the user's properties.
        """
        self.__user = user
        

    @property
    def user(self):
        return self.__user


    def start_chat(self, user_id: str, flag: bool = False, private_chat : PrivateChat = None):
        """
        starts a chat with a user based on theirs user_id. Only friends can be chatted with.
        For each successful chat creation, both users are updated with the new chat.
        This causes the function to be ran twice for each chat creation, once for each user.
        :param user_id: the user_id of the user that the chat is started with.
        :param flag = False: first time using this method. True: second time using this method.
        :param private_chat = If provided, this param is the chat needed to be created. Should only be provided if flag is True. If not provided, a new chat is created.
        """
        friend_ids = [friend.user_id for friend in self.__user.friends]
        if user_id not in friend_ids:
            print('You can only chat with your friends')
            return
        
        if user_id in self.__user.private_chats:
            print('You are already chatting with this user')
            return

        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        addressee = User.from_dict(users[user_id])
        if not private_chat:
            private_chat = PrivateChat(self.__user, addressee)
        self.__user.__private_chats[user_id] = private_chat

        users[self.__user.user_id] = self.__user.to_dict()

        if not flag:
            addressee.private_chat_handler.start_chat(self.__user.user_id, True, private_chat)

        private_chat_dict = private_chat.to_dict()
        DButilites.update_data_to_json(DButilites.PRIVATE_CHAT_DB_PATH, private_chat_dict)
        DButilites.update_data_to_json(DButilites.USER_DB_PATH, users)

        print(f"Private chat created between user {self.__user.username} and user {addressee.username}")
