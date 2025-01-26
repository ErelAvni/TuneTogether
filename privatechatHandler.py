from User import User
from privateChat import PrivateChat
import DButilites


class PrivateChatHandler:
    def __init__(self, User: User):
        self.__user = User
        

    @property
    def user(self):
        return self.__user


    def start_chat(self, user_id: str):
        friend_ids = [friend.user_id for friend in self.__user.friends]
        if user_id not in friend_ids:
            print('You can only chat with your friends')
            return
        
        if user_id in self.__user.private_chats:
            print('You are already chatting with this user')
            return

        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        addressee = users[user_id]
        this_private_chat = PrivateChat(self.__user, addressee)
        self.__user.__private_chats[user_id] = this_private_chat
        addressee_private_chat = PrivateChat(addressee, self.__user, this_private_chat.encryption_key)
        addressee.__private_chats[self.__user.user_id] = addressee_private_chat

        #TODO: save the private chats to the database. This includes the chats and the users, I think that each are saved in a different database so it's a different function for each one
