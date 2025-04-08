#TODO: learn how to use spotify API to get the song image and the artist. 
import db.DButilites as DButilities
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from PIL import Image
from io import BytesIO
import json
import os
import dotenv
dotenv.load_dotenv()

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


# Authenticate using Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))


class Song:
    def __init__(self, song_name: str):
        '''Initializes a song object. Will work only for songs that are in the database.
        :param song_name: the name of the song. Needs to be in \"Some Song Name\" format.
        '''
        self.song_name = song_name
        
        song_paths_dict = DButilities.load_data_from_json(DButilities.SONG_PATHS_PATH)
        try:
            self.song_audio_file_path = song_paths_dict[self.song_name]

        except KeyError:
            print(f"Song {self.song_name} not found in the database.")

        self.artist = None
        self.album_cover = None

        song_info = self.get_song_info()
        if song_info:
            self.artist = song_info[0]
            self.album_cover = self.get_album_cover_from_URL(song_info[1])
            self.song_duration = song_info[2]

        else:
            raise ValueError(f"Song {song_name} not found in Spotify.")

    
    def get_song_info(self):
        '''Gets info on a song by its name using the Spotify API.
        :Returns: tuple of the artist and the song image URL'''
        query = self.song_name
        results = sp.search(q=query, type="track", limit=1)

        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            artist_name = track["artists"][0]["name"]
            album_cover = track["album"]["images"][0]["url"]  # Highest quality image
            song_length = track["duration_ms"] * 0.001  # Convert milliseconds to seconds
            song_length = int(song_length)  # Convert to integer seconds
            song_length = f"{song_length // 60}:{song_length % 60:02d}" 
        
        else:
            return None, None
        
        return [artist_name, album_cover, song_length]
    

    def get_album_cover_from_URL(self, image_URL):
        '''
        Returns the album cover image from the URL. Resizes it to 100x100 pixels for use in a button.
        :param image_URL: the URL of the image.
        :return: the image in a format that can be used for the button. To use it, you need to convert it to a PhotoImage object.
        '''
        response = requests.get(image_URL)  # Download image
        img_data = Image.open(BytesIO(response.content))  # Convert to Image
        img_data = img_data.resize((100, 100), Image.Resampling.LANCZOS)  # Resize for button
        return img_data


    def to_dict(self):
        '''Returns a dictionary representation of the song object.
        :return: a dictionary with the song name, artist, and album cover'''
        return {
            "song_name": self.song_name,
            "song_audio_file_path": self.song_audio_file_path,
            "artist": self.artist,
            "album_cover": self.album_cover
        }
    

    def to_json(self):
        '''Returns a JSON representation of the song object.
        :return: a JSON string with the song name, artist, and album cover'''
        return json.dumps(self.to_dict())