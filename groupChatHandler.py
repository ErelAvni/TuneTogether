from User import User
from groupChat import GroupChat
import new.db.DButilites as DButilites
from message import Message


class GroupChatHandler:
    def __init__(self, user: User):
        """
        Creates a group chat handler for the user.
        This handler is exclusive to the user and is used to manage the group chats that the user is in.
        :param User: the user that the handler is created for. User should pass itself by reference in 
        it's constructor, giving the handler access to the user's properties.
        """
        self.__user = user


    def create_group_chat(self, name: str):
        """
        Creates a group chat with the given name.
        :param name: the name of the group chat.
        """
        group_chat = GroupChat(name, self.__user)
        self.__user.__group_chats.append(group_chat)

        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        users[self.__user.user_id] = self.__user.to_dict()
        DButilites.update_data_to_json(DButilites.USER_DB_PATH, users)
        DButilites.update_data_to_json(DButilites.GROUP_CHAT_DB_PATH, group_chat.to_dict())

        print(f"group chat \"{name}\" was created successfully.")

    
    def add_self_user_to_group_chat(self, group_chat: GroupChat):
        """
        Adds self.__user to the given group chat. Should only be called from the add_user_to_group_chat method in this class
        """
        if group_chat:
            self.__user.__group_chats.append(group_chat)

            users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
            users[self.__user.user_id] = self.__user.to_dict()
            DButilites.update_data_to_json(DButilites.USER_DB_PATH, users)
        else:
            print("Group chat that was given does not exist. Not doing anything")


    def add_user_to_group_chat(self, group_chat: GroupChat, user: User):
        """
        Adds a user to the group chat. Only available to the group managers.
        :param group_chat: the group chat to add the user to.
        :param user: the user to add to the group chat.
        """
        if self.__user.user_id not in group_chat.managers.keys():
            print(f"You cannot add a user to group chat \"{group_chat.name}\" if you are not a manager.")
            return

        group_chat.add_user(user)
        user.group_chat_handler.add_self_user_to_group_chat(group_chat)

        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        users[user.user_id] = user.to_dict()
        DButilites.update_data_to_json(DButilites.USER_DB_PATH, users)
        #not updating the group chat DB because it's already being updated in the group_chat.add_user() method

        print(f"user \"{user.username}\" was added to group chat \"{group_chat.name}\" successfully.")

    
    def remove_self_user_from_group_chat(self, group_chat: GroupChat):
        """
        Removes self.__user from the given group chat. Should only be called from the remove_user_to_group_chat method in this class
        """
        if group_chat:
            if group_chat not in self.__user.group_chats:
                self.__user.__group_chats.remove(group_chat)

                users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
                users[self.__user.user_id] = self.__user.to_dict()
                DButilites.update_data_to_json(DButilites.USER_DB_PATH, users)
            else:
                print("User already not in the given group chat.")
        else:
            print("Group chat that was given does not exist. Not doing anything.")


    def remove_user_from_group_chat(self, group_chat: GroupChat, user: User):
        """
        Removes the user from the given group chat. Only available to the group managers.
        :param group_chat: the group chat to remove the user from
        :param uesr: the user that is being removed.
        """
        if self.__user.user_id not in group_chat.managers.keys():
            print(f"You cannot remove a user to group chat \"{group_chat.name}\" if you are not a manager.")
            return
        
        if user not in group_chat.users:
            print("You cannot remove a user from a group chat that he is not already in.")
            return
        
        group_chat.remove_user(user)
        user.group_chat_handler.remove_self_user_from_group_chat(group_chat)
        
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        users[user.user_id] = user.to_dict()
        DButilites.update_data_to_json(DButilites.USER_DB_PATH, users)


    def receive_message(self, group_chat: GroupChat, message: str):
        """
        Receives a message from the group chat. Only available to the users that are in the group chat.
        Not responsible for sending the message, nor for saving it for everyone else in the group chat or saving it in the db
        :param group_chat: the group chat that the message is from.
        :param message: the message that was received.
        """
        if group_chat not in self.__user.group_chats:
            print("You cannot receive a message from a group chat that you are not in.")
            return
        
        self.__user.group_chats[group_chat].add_message(message)

        print(f"Message received from group chat \"{group_chat.name}\" successfully.")

    
    def send_message(self, group_chat: GroupChat, message: Message):
        """
        Sends a message to the group chat. Only available to the users that are in the group chat.
        Calls the receive_message method for each user in the group chat, meaning that the method is responsible for sending the message to everyone in the group chat.
        """
        if group_chat not in self.__user.group_chats:
            print("You cannot send a message to a group chat that you are not in.")
            return
        
        for user in group_chat.users:
            user.group_chat_handler.receive_message(group_chat, message)

        print(f"Message sent to group chat \"{group_chat.name}\" successfully.")