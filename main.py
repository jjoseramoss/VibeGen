import streamlit as st
import os
from dotenv import load_dotenv
from spotify_client_api import SpotifyClient
from openai_client_api import OpenAIClient
from playlist_generator import PlaylistGenerator
from playlist_history import PlaylistHistory

load_dotenv()

def main():
    #Title
    st.title("Welcome to :blue[VibeGen] :headphones::notes:")
    st.divider()
    st.markdown('''Music should always fit the vibe! So why not try and find the perfect playlist that fits the mood?''')
        
    # Login to Spotify
    authorization_code = SpotifyClient.login_spotify()
    if not authorization_code:
        return

    # Get Spotify client
    spotify_client = SpotifyClient.get_spotify_client(authorization_code)
    if not spotify_client:
        return
    
    # Initialize OpenAI client
    openai_client = OpenAIClient()
    
    # Initialize playlist generator
    playlist_generator = PlaylistGenerator(spotify_client, openai_client)
    
    # Get user input
    prompt, song_count = playlist_generator.get_user_input()
    if not prompt:
        return
    
    # Generate and create playlist
    playlist_generator.generate_and_create_playlist(prompt, song_count)

    #Playlist History
    st.subheader("Playlist History:")
    history = PlaylistHistory()
    playlists = history.load_all_playlists()

    for p in playlists:
        st.markdown(f"### {p['playlist_name']}")
        for song in p['songs']:
            st.markdown(f"- **{song['songname']}** by *{', '.join(song['artists'])}*")

if __name__ == "__main__":
    main()
