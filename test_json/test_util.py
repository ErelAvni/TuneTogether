import json
import os

def get_data_by_path(file_name: str, file_path: str = '') -> dict:
    if file_path == '':
        full_path = file_name
    else:
        full_path = os.path.join(file_path, file_name)

    with open(full_path, 'r') as file:
        data_dict = json.load(file)
    return data_dict
    

def update_DB_by_path(new_data_dict: dict, file_name: str, file_path: str = '') -> dict:
    if file_path == '':
        full_path = file_name
    else:
        full_path = os.path.join(file_path, file_name)

    total_data_dict = get_data_by_path(file_name, file_path)
    total_data_dict.update(new_data_dict)

    with open(full_path, 'w') as file:
        json.dump(total_data_dict, file, indent=4)


if __name__ == '__main__':
    chat1 = {}
    chat1['chat_id'] = 1
    chat1['messages'] = ["hello", "world"]
    chat1['encryption_key'] = ["asefasefasdfase"]

    update_DB_by_path(chat1, "test_chat_db.json")
