from hashlib import sha256
current_id_counter = 0


class User():
    def __init__(self, username: str, password: str, first_name: str, last_name: str, age: int):
        global current_id_counter

        self._username = username
        
        hash_obj = sha256()
        hash_obj.update(password.encode('utf-8'))
        
        self._password_hash = hash_obj.hexdigest()

        self._user_id = current_id_counter
        current_id_counter += 1

        self._first_name = first_name
        self._last_name = last_name
        self._age = age

    @property
    def username():
        return self._username
    
    
    @property
    def password_hash():
        return self._password_hash
    
    @property
    def user_id():
        return self._user_id
    
    @property
    def first_name():
        return self._first_name
    
    @property
    def last_name():
        return self._last_name
    
    @property
    def age():
        return self._age
