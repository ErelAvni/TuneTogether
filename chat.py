from cryptography.fernet import Fernet
from message import Message
from abc import ABC
import DButilites


class Chat(ABC):
    def __init__(self, chat_id: str, encryption_key: bytes = None):
        self.__chat_id = chat_id

        if encryption_key:# this is to handle logic of creaintg new chat with new encryption key (when the chat is created with insperation of a different chat)
            self.__encryption_key = encryption_key
        else:
            self.__encryption_key = Fernet.generate_key()

        self.__chiper = Fernet(self.__encryption_key)
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
        self.__messages.append(msg)
        DButilites.save_data_to_json(path, data)
    

    def decrypt_message(self, msg: Message) -> str:
        decrypted_text_bytes = self.__chiper.decrypt(msg.text)
        return decrypted_text_bytes.decode()
    
    
    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'chiper': self.chiper,
            'encryption_key': self.encryption_key,
            'messages': [msg.message_id for msg in self.messages]
        }