#TODO: learn how to use spotify API to get the song image and the artist. 
import db.DButilites as DButilities
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import dotenv
dotenv.load_dotenv()


CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


# Authenticate using Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))


class Song:
    def __init__(self, song_name: str, song_image, artist: str):
        '''Initializes a song object.
        :param song_name: the name of the song.
        :param song_image: the image of the song. Most likely to be an album cover.
        :param artist: the artist who made the song.
        '''
        self.song_name = song_name
        
        song_paths_dict = DButilities.load_data_from_json(DButilities.SONG_PATHS_PATH)
        self.song_audio_file_path = song_paths_dict[self.song_name]

    
    def get_song_info(song_name):
        '''Gets info on a song by its name using the Spotify API.
        :Returns: tuple of the artist and the song image URL'''
        query = song_name
        results = sp.search(q=query, type="track", limit=1)

        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            artist_name = track["artists"][0]["name"]
            album_cover = track["album"]["images"][0]["url"]  # Highest quality image
        
        else:
            return None, None
        
        return artist_name, album_cover
    

    def get_album_cover_from_URL(image_URL):
        ''''''