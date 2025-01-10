import json
import os

def load_data_from_json(file_name : str, path = ""):
    if path == "":
        full_path = file_name
    else:
        full_path = os.path.join(file_name, path)

    if not os.path.exists(full_path):
        print("The file does not exist. Returning empty dict.")
        return {}
    
    with open(full_path, 'r') as file:
        raw_data = file.read()
        data = json.loads(raw_data)
    
    return data


def update_data_to_json(data: dict, file_name : str, path = ""):
    if path == "":
        full_path = file_name
    else:
        full_path = os.path.join(file_name, path)

    if not os.path.exists(full_path):
        print("The file does not exist. Not updating anything.")
        return
    
    data_key = data['id']
    file_data = load_data_from_json(file_name, path)
    file_data[data_key] = data

    with open(full_path, 'w') as file:
        json.dump(file_data, file, indent=4)


if __name__ == "__main__":
    print(load_data_from_json("test_chat_db.json"))