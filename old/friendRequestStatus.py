from enum import Enum

class FriendRequestStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DENIED = 'denied'
    