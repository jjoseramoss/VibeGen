import os
import requests
import spotipy
import streamlit as st

class SpotifyClient:
    @staticmethod
    @st.cache_data
    def get_spotify_client(authorization_code):
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": os.getenv("REDIRECT_URI"),
                "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
                "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        # Debugging: Print the response
        # st.write("Response Status Code:", response.status_code)
        # st.write("Response Text:", response.text)

        # Check if 'access_token' exists
        if "access_token" not in response.json():
            st.error("Failed to retrieve access token. Check the response details above.")
            return None

        return spotipy.Spotify(auth=response.json()["access_token"])

    @staticmethod
    def login_spotify():
        auth_url = f"https://accounts.spotify.com/authorize?client_id={os.environ['SPOTIFY_CLIENT_ID']}&response_type=code&redirect_uri=http://localhost:8501&scope=playlist-modify-private"
        query_param = st._get_query_params()
        if query_param:
            return query_param["code"][0]
        st.title("Log In")
        st.write(
            f"Please log in to <a target='_self' href='{auth_url}'>spotify",
            unsafe_allow_html=True,
        )
        query_param = st._get_query_params()
        if query_param:
            return query_param["code"][0]
        
    @staticmethod
    def create_playlist(spotify_client, playlist_name, playlist_description, song_uris):
        user_id = spotify_client.me()["id"]
        playlist = spotify_client.user_playlist_create(user_id, playlist_name, False, description=playlist_description)
        playlist_id = playlist["id"]
        spotify_client.playlist_add_items(playlist_id, song_uris)
        return playlist
    
    @staticmethod
    def search_songs(spotify_client, recommended_songs):
        song_uris = []
        for song in recommended_songs:
            try:
                result = spotify_client.search(
                    q=f"track:{song['songname'].encode('utf-8').decode('unicode_escape')} artist:{' '.join([artist.encode('utf-8').decode('unicode_escape') for artist in song['artists']])}",
                    type="track",
                    limit=1
                )
                tracks = result['tracks']['items']
                if tracks:
                    song_uris.append(tracks[0]['uri'])
                else:
                    continue
            except Exception as e:
                #Log error, but skip bad songname
                print(f"Error searching for {song['songname']} - {e}")
                continue
        return song_uris 
