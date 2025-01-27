from friendRequestStatus import FriendRequestStatus
from datetime import date
from User import User
import DButilites

class FriendRequest():
    def __init__(self, sender: User, addressee: User, status: FriendRequestStatus = FriendRequestStatus.PENDING, request_date: date = date.today()):
        self.__sender = sender
        self.__addressee = addressee
        self.__status = status
        self.__request_date = request_date

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
    

    @staticmethod
    def from_dict(data_dict: dict):
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        sender = users[data_dict['sender']]#this is extracting the user object from the user id, therefore datadict gets the id, not the full user object
        addressee = users[data_dict['addressee']]
        status = data_dict['status']
        request_date = data_dict['request_date']
        return FriendRequest(sender, addressee, status, request_date)