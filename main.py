import streamlit as st
import os
from dotenv import load_dotenv
from spotify_client_api import SpotifyClient
from openai_client_api import OpenAIClient
from playlist_generator import PlaylistGenerator

load_dotenv()

def main():
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

if __name__ == "__main__":
    main()
