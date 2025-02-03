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


    def start_chat(self, user_id: str, flag: bool = False):
        """
        starts a chat with a user based on theirs user_id. Only friends can be chatted with.
        """
        friend_ids = [friend.user_id for friend in self.__user.friends]
        if user_id not in friend_ids:
            print('You can only chat with your friends')
            return
        
        if user_id in self.__user.private_chats:
            print('You are already chatting with this user')
            return

        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        addressee = users[user_id]
        private_chat = PrivateChat(self.__user, addressee)
        self.__user.__private_chats[user_id] = private_chat

        users[self.__user.user_id] = self.__user.to_dict()

        if not flag:
            addressee.private_chat_handler.start_chat(self.__user.user_id, True)

        
        #TODO: save the private chats to the database. This includes the chats and the users, I think that each are saved in a different database so it's a different function for each one
