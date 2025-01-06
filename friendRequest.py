from friendRequestStatus import FriendRequestStatus
from datetime import date

class FriendRequest():
    def __init__(self, sender: SocialUser, addressee: SocialUser):
        self.__sender = sender
        self.__addressee = addressee
        self.__status = FriendRequestStatus.PENDING
        self.__request_date = date.today()

    @property
    def sender():
        return self.__sender
    
    @property
    def addressee():
        return self.__addressee
    
    @property
    def status():
        return self.__status
    
    @property
    def request_date():
        return self.__request_date
    