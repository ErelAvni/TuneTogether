from cryptography.fernet import Fernet
from message import Message
from abc import ABC

def get_last_id():
    '''TODO: load from DB adn get the last last id'''
    return 0

class Chat():
    def __init__(self):
        self.__chat_id = get_last_id() + 1

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
    
    def add_message(self, msg: Message):
        '''TODO: update this in the chat DB'''
        self.__messages.append(msg)
    
    def decrypt_message(self, msg: Message) -> str:
        decrypted_text_bytes = self.__chiper.decrypt(msg.text)
        return decrypted_text_bytes.decode()