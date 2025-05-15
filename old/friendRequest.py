from old.friendRequestStatus import FriendRequestStatus
from datetime import date
from old.User import User
import new.db.DButilites as DButilites
from datetime import datetime

class FriendRequest():
    def __init__(self, sender: User, addressee: User, status: FriendRequestStatus = FriendRequestStatus.PENDING, request_date: datetime = datetime.today()):
        """
        Creates a new friend request object
        :param sender: the user who sent the friend request
        :param addressee: the user who received the friend request
        :param status: the status of the friend request, Enum of FriendRequestStatus
        :param request_date: the date the friend request was sent
        """
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
            'status': self.status.value,
            'request_date': self.request_date.isoformat()
        }
    

    @classmethod
    def from_dict(data_dict: dict):
        """
        class method that creates a new FriendRequest object from a dictionary.
        Dictionary is expected to be the output of the to_dict method.
        """
        users = DButilites.load_data_from_json(DButilites.USER_DB_PATH)
        sender = User.from_dict(users[data_dict['sender']])
        addressee = User.from_dict(users[data_dict['addressee']])

        status = FriendRequestStatus(data_dict['status'])
        request_date = datetime.fromisoformat(data_dict['request_date'])
        return FriendRequest(sender, addressee, status, request_date)