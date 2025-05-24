import json
import os

#CONSTS
BASE_PATH = os.path.dirname(__file__).replace("\\", "/")
BASE_PATH = os.path.abspath(os.path.join(BASE_PATH, ".."))
USER_DB_PATH = os.path.join(BASE_PATH, "Server", "db", "users.json").replace("\\", "/")
SONG_PATHS_PATH = os.path.join(BASE_PATH, "Client", "db", "song_paths.json").replace("\\", "/")
COMMENTS_PATH = os.path.join(BASE_PATH, "Client", "db", "comments.json").replace("\\", "/")
SONG_RATINGS_PATH = os.path.join(BASE_PATH, "Client", "db", "song_ratings.json").replace("\\", "/")


def load_song_paths():
    """
    Loads the song paths from the JSON file.
    Returns a dictionary with song names as keys and their paths as values.
    """    
    with open(SONG_PATHS_PATH, 'r') as file:
        raw_data = file.read()
        data = json.loads(raw_data)

    # add the absolute path to each song and traverse to Client directory
    for song_name, song_path in data.items():
        song_path = os.path.join(BASE_PATH, "Client", song_path)
        data[song_name] = os.path.abspath(song_path).replace("\\", "/")
    
    return data


def load_data_from_json(full_path: str):
    if not os.path.exists(full_path):
        print("The file does not exist. Returning empty dict.")
        return {}
    
    if full_path == SONG_PATHS_PATH:
        return load_song_paths()

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
    print(USER_DB_PATH)
    print(os.path.exists(USER_DB_PATH))
    print(load_data_from_json(USER_DB_PATH))
