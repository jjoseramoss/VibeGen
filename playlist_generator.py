import streamlit as st
from spotify_client_api import SpotifyClient
from playlist_history import PlaylistHistory

class PlaylistGenerator:
    def __init__(self, spotify_client, openai_client):
        self.spotify_client = spotify_client
        self.openai_client = openai_client
        self.history = PlaylistHistory()
    
    def get_user_input(self):
        with st.form("VibeGen: Playlist Generator"):
            prompt = st.text_input("Describe the music playlist you'd like to generate...")
            song_count = st.slider("Songs", 1, 30, 10)
            submitted = st.form_submit_button("Create")
        
        if submitted:
            return prompt, song_count
        return None, None
    
    def generate_and_create_playlist(self, prompt, song_count):
        # Generate playlist recommendations using OpenAI
        arguments = self.openai_client.generate_playlist(prompt, song_count)
        
        # Format playlist name and get song details
        playlist_name = "AI - " + arguments["playlist_name"]
        playlist_description = arguments["playlist_description"]
        recommended_songs = arguments["songs"]

        #Save playlist json
        self.history.save_playlist(arguments)
        
        # Search for songs on Spotify
        song_uris = SpotifyClient.search_songs(self.spotify_client, recommended_songs)   

        # Create the playlist
        playlist = SpotifyClient.create_playlist(
            self.spotify_client, 
            playlist_name, 
            playlist_description, 
            song_uris
        )
        
        # Display success message
        
        st.success("✅ Your playlist was created successfully!")

        st.markdown(
            f"### 🎸 [Open your Playlist on Spotify]({playlist['external_urls']['spotify']})",
            unsafe_allow_html=True,
        )

        st.info("Enjoy your personalized vibes! ✨ Feel free to generate more playlists!")
        st.divider()

        

