from hashlib import sha256
import db_utils


def get_last_id():
    users_dict = db_utils.load_data_from_json(db_utils.USER_DB_PATH)
    sorted_ids = sorted(users_dict.keys())
    return sorted_ids[-1]

class User():
    def __init__(self, username: str, password: str, first_name: str, last_name: str, age: int):
        self._username = username
        
        hash_obj = sha256()
        hash_obj.update(password.encode('utf-8'))
        
        self._password_hash = hash_obj.hexdigest()

        self._user_id = self.get_last_id() + 1

        self._first_name = first_name
        self._last_name = last_name
        self._age = age

    @property
    def username(self):
        return self._username
    
    
    @property
    def password_hash(self):
        return self._password_hash
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name
    
    @property
    def age(self):
        return self._age
