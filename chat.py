from cryptography.fernet import Fernet
from message import Message
from abc import ABC
import DButilites


class Chat(ABC):
    def __init__(self, chat_id: str, encryption_key: bytes = None,
                 messages: list = None):
        """
        Creates a new chat object.
        Chiper is created with the encryption key, not a parameter.

        :param chat_id: the unique chat id, provided by the subclasses
        :param encryption_key: the encryption key for the chat, expected to be 32 bytes long. If not provided, a new key will be generated
        :param messages: a list of the ids of the messages in the chat. If not provided, an empty list will be created
        """
        self.__chat_id = chat_id

        if encryption_key:
            self.__encryption_key = encryption_key
        else:
            self.__encryption_key = Fernet.generate_key()

        self.__chiper = Fernet(self.__encryption_key)
        
        if messages:
            self.__messages = messages
        else:
            self.__messages = []
    
    @property
    def chat_id(self):
        return self.__chat_id
    
    @property
    def chiper(self):
        return self.__chiper
    
    @property
    def encryption_key(self):
        return self.__encryption_key
    
    @property
    def messages(self):
        return self.__messages
    

    def add_message(self, msg: Message, path: str, data: dict):
        """
        Adds a message to the chat.
        
        :param msg: the message to be added
        :param path: the path to the json file. Provided by the subclasses
        """
        self.__messages.append(msg)
        DButilites.save_data_to_json(path, data)
    

    def decrypt_message(self, msg: Message) -> str:
        """
        returns the decrypted text of the message.
        """
        decrypted_text_bytes = self.__chiper.decrypt(msg.text)
        return decrypted_text_bytes.decode()
    
    
    def to_dict(self):
        """
        Returns a dictionary representation of the chat.
        When saving to a json file, this method should be used.
        When saving a nested object, the id of said object is being saved.
        Not saving the chiper object, as it is not serializable and there is no need to save it.
        """
        return {
            'chat_id': self.chat_id,
            'encryption_key': self.encryption_key,
            'messages': [msg.message_id for msg in self.messages]
        }
