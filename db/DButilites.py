import json
import os

#CONSTS
BASE_PATH = os.path.dirname(__file__)
MESSAGE_DB_PATH = os.path.join(BASE_PATH, "message_db.json")
PRIVATE_CHAT_DB_PATH = os.path.join(BASE_PATH, "private_chat_db.json")
GROUP_CHAT_DB_PATH = os.path.join(BASE_PATH, "group_chat_db.json")
USER_DB_PATH = os.path.join(BASE_PATH, "user_db.json")


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

    try:
        with open(full_path, 'w') as file:
            json.dump(file_data, file, indent=4)
        print(f"Successfully wrote to {full_path}")
    except Exception as e:
        print(f"Error while writing to file: {e}")


if __name__ == "__main__":
    print("Why would you run this? It's a helper module...")
