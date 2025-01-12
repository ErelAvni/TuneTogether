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
    print("entered the update method")
    if not os.path.exists(full_path):
        print("The file does not exist. Not updating anything.")
        return
    
    print("passed the first if statement")
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
    msg1 = {}
    msg1['id'] = "1"
    msg1['text'] = "nig"
    msg1['sender'] = "1" #this is the sender's id

    msg2 = {}
    msg2['id'] = "2"
    msg2['text'] = "ger"
    msg2['sender'] = "1" #this is the sender's id

    chat1 = {}
    chat1['id'] = "1"
    chat1['messages'] = ["1", "2"] #messages id
    chat1['encryption_key'] = "the first key!"

    user1 = {}
    user1['id'] = "1"
    user1['username'] = "kreker"
    user1['chats'] = ["1"] #chats id

    base_path = os.path.dirname(__file__)
    message_db_path = os.path.join(base_path, "test_message_db.json")
    
    print(f"Base path: {base_path}")
    print(f"Message DB path: {message_db_path}")

    print("The file exists: " + str(os.path.exists(message_db_path)))

    try:
        print("Calling update_data_to_json for msg1")
        update_data_to_json(msg1, message_db_path)
        print("Called update_data_to_json for msg1")
    except Exception as e:
        print(f"Error during msg1 update: {e}")

    print("working from this path: " + os.getcwd())

    try:
        print("Calling update_data_to_json for msg2")
        update_data_to_json(msg2, message_db_path)
        print("Called update_data_to_json for msg2")
    except Exception as e:
        print(f"Error during msg2 update: {e}")