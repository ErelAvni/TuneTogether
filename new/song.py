#TODO: learn how to use spotify API to get the song image and the artist. 
import db.DButilites as DButilities
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from PIL import Image
from io import BytesIO
from comment import Comment
from datetime import datetime
import json
import os
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
import dotenv
dotenv.load_dotenv()

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')


# Authenticate using Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


class Song:
    def __init__(self, song_name: str):
        '''Initializes a song object. Will work only for songs that are in the database.
        :param song_name: the name of the song. Needs to be in \"Some Song Name\" format.
        '''
        print("entered init with song: ", song_name)
        self.song_name = song_name
        
        song_paths_dict = DButilities.load_data_from_json(DButilities.SONG_PATHS_PATH)
        try:
            self.song_audio_file_path = song_paths_dict[self.song_name]

        except KeyError:
            print(f"Song {self.song_name} not found in the database.")

        self.artist = None
        self.album_cover = None
        print("past song_paths_dict with song: ", self.song_name)
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
            print("past good results with song: ", self.song_name)
        
        else:
            print(f"Song {self.song_name} not found in Spotify.")
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
    

    def get_youtube_URL(self, query: str = None):
        '''Search for a song on YouTube using the provided query.
        :param query: The search query for the song (should be the song's name).
        :return: The URL of the first matching song to the search query.
        '''
        if query is None:
            query = self.song_name
        search_response = youtube.search().list(
            q=query,                   # Search query (song name)
            part="snippet",            # Request snippet data (title, ID, etc.)
            type="video",              # Only look for videos (not channels/playlists)
            videoCategoryId="10",      # Filter results to category 10 (Music)
            maxResults=1               # Get only the top result
        ).execute()

        # Extract video ID from the API response
        if search_response["items"]:
            song_id = search_response["items"][0]["id"]["videoId"]
            song_url = f"https://www.youtube.com/watch?v={song_id}"
            return song_url
        
        return None  # Return None if no result found


    def get_comments_by_url(self, max_results: int = 20):
        # Extract video ID from URL
        url = self.get_youtube_URL()
        query = urlparse(url).query
        video_id = parse_qs(query).get("v")
        if not video_id:
            raise ValueError("Invalid YouTube URL or missing video ID.")
        video_id = video_id[0]

        # Call commentThreads endpoint
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        try:     
            response = request.execute()

            comments = []
            for item in response.get("items", []):
                top_comment = item["snippet"]["topLevelComment"]["snippet"]
                timestamp = datetime.fromisoformat(top_comment["publishedAt"].replace("Z", ""))
                commnet = Comment(
                    username = top_comment["authorDisplayName"],
                    content = top_comment["textDisplay"],
                    timestamp = timestamp
                    
                )
                comments.append(commnet)

            return comments
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    

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
    

if __name__ == "__main__":
    # Example usage
    song = Song("Bohemian Raphsody")
    print(song.to_dict())
    print(song.get_youtube_URL())
    print(song.get_comments_by_url())