import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=config.client_id,
            client_secret=config.secret_client_id,
            redirect_uri=config.redirect_url,
            scope="user-library-read"
        ))

    def get_artist_albums(self, artist_uri):
        results = self.sp.artist_albums(artist_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return [album['name'] for album in albums]