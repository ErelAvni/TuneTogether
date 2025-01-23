from friendRequestStatus import FriendRequestStatus
from datetime import date
from User import User

class FriendRequest():
    def __init__(self, sender: User, addressee: User):
        self.__sender = sender
        self.__addressee = addressee
        self.__status = FriendRequestStatus.PENDING
        self.__request_date = date.today()

    @property
    def sender(self):
        return self.__sender
    
    @property
    def addressee(self):
        return self.__addressee
    
    @property
    def status(self):
        return self.__status
    
    @property
    def request_date(self):
        return self.__request_date
    

    def to_dict(self):
        return {
            'sender': self.sender.user_id,
            'addressee': self.addressee.user_id,
            'status': self.status,
            'request_date': self.request_date
        }