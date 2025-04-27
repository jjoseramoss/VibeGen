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
            st.subheader("🎧 Describe Your Playlist")
            st. caption("Give a vibe, feeling, mood, or activity. Example: 'Hype gym session.'")

            prompt = st.text_input("📃 Playlist Vibe", placeholder="e.g, Late night coding vibes")
            st.divider()

            st.subheader("🔢 Number of Songs")
            song_count = st.slider("Select how many songs you'd like:", 1, 30, 10)
            submitted = st.form_submit_button("Generate Playlist")
        
        if submitted:
            return prompt, song_count
        return None, None
    
    def generate_and_create_playlist(self, prompt, song_count):
        with st.spinner('🎶 Generating your playlist... Please wait:)'):
            # Generate playlist recommendations using OpenAI
            arguments = self.openai_client.generate_playlist(prompt, song_count)

            #Testing 
            print(arguments)
             # ⚠️Validate OpenAI output
            if "songs" not in arguments or not arguments["songs"]:
                st.error("⚠️ The AI could not generate a playlist based on your description. Please try a different vibe!")
                return
            
            # Format playlist name and get song details
            playlist_name = "AI - " + arguments["playlist_name"]
            playlist_description = arguments["playlist_description"]
            recommended_songs = arguments["songs"]

            #Save playlist json
            self.history.save_playlist(arguments)
            
            # Search for songs on Spotify
            song_uris = SpotifyClient.search_songs(self.spotify_client, recommended_songs)   

            # ⚠️ Validate Spotify search results too
            if not song_uris:
                st.error("⚠️ Could not find any matching songs on Spotify. Please try a different vibe!")
                return

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

        

