import json
import os

#CONSTS
BASE_PATH = os.path.dirname(__file__)
USER_DB_PATH = os.path.join(BASE_PATH, "users.json")
SONG_PATHS_PATH = os.path.join(BASE_PATH, "song_paths.json")
COMMENTS_PATH = os.path.join(BASE_PATH, "comments.json")


def load_data_from_json(full_path: str):
    if not os.path.exists(full_path):
        print("The file does not exist. Returning empty dict.")
        return {}
    
    with open(full_path, 'r') as file:
        raw_data = file.read()
        data = json.loads(raw_data)
    
    return data


def update_data_to_json(data: dict, full_path: str, manual_update: bool = False):
    """
    Updates the data in the file at the given path.
    If the file does not exist, it will not update anything.
    Expecting the data to be a dictionary with a key 'username' that is unique.
    if manual_update is True, it will not add the data to the file, but will just write it as is.
    this means that if manual_update is True, the data should be a dictionary with the same structure as the file.
    """
    if not manual_update:
        data_key = data['username']
        file_data = load_data_from_json(full_path)
        file_data[data_key] = data

    else: 
        file_data = data

    if not os.path.exists(full_path):
        print("The file does not exist. Not updating anything.")
        return False
    
    try:
        with open(full_path, 'w') as file:
            json.dump(file_data, file, indent=4)
        print(f"Successfully wrote to {full_path}")
        return True
    except Exception as e:
        print(f"Error while writing to file: {e}")
        return False


if __name__ == "__main__":
    print("Why would you run this? It's a helper module...")
