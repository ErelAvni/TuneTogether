import json
import os

def load_data_from_json(full_path: str):
    if not os.path.exists(full_path):
        print("The file does not exist. Returning empty dict.")
        return {}
    
    with open(full_path, 'r') as file:
        raw_data = file.read()
        data = json.loads(raw_data)
    
    return data


def update_data_to_json(data: dict, full_path: str):
    if not os.path.exists(full_path):
        print("The file does not exist. Not updating anything.")
        return
    
    data_key = data['id']
    file_data = load_data_from_json(full_path)
    file_data[data_key] = data

    with open(full_path, 'w') as file:
        json.dump(file_data, file, indent=4)


if __name__ == "__main__":
    msg1 = {}
    msg1['id'] = "1"
    msg1['text'] = "this is the first message omg so exiting!!!"
    msg1['sender'] = 1 #this is the sender's id

    msg2 = {}
    msg2['id'] = "2"
    msg2['text'] = "this is the second message we're getting there"
    msg2['sender'] = 1 #this is the sender's id

    chat1 = {}
    chat1['id'] = "1"
    chat1['messages'] = ["1", "2"] #messages id
    chat1['encryption_key'] = "the first key!"

    user1 = {}
    user1['id'] = "1"
    user1['username'] = "kreker"
    user1['chats'] = ["1"] #chats id

    update_data_to_json(msg1, "C:\\Users\\משתמש\\Desktop\\TuneTogether\\TuneTogether\\test_json\\test_message_db.json")
    