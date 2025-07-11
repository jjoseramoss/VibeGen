import streamlit as st
import spotipy
import openai
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

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
    st.write("Response Status Code:", response.status_code)
    #st.write("Response Text:", response.text)

    # Check if 'access_token' exists
    if "access_token" not in response.json():
        st.error("Failed to retrieve access token. Check the response details above.")
        return None

    return spotipy.Spotify(auth=response.json()["access_token"])


def login_spotify():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={os.environ['SPOTIFY_CLIENT_ID']}&response_type=code&redirect_uri=http://localhost:8501&scope=playlist-modify-private"
    query_param = st._get_query_params()
    if query_param:
        return query_param["code"][0]
    st.write(
        f"Please log in to <a target='_self' href='{auth_url}'>spotify",
        unsafe_allow_html=True,
    )
    query_param = st._get_query_params()
    if query_param:
        return query_param["code"][0]

def main():
    authorization_code = login_spotify()
    if not authorization_code:
        return

    spotify_client = get_spotify_client(authorization_code)

    with st.form("VibeGen: Playlist Generator"):
        prompt = st.text_input("Describe the music playlist you'd like to generate...")
        song_count = st.slider("Songs", 1, 30, 10)
        submitted = st.form_submit_button("Create")
    if not submitted:
        return
    

    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are MusicGPT, world's best music recommendation AI. Given a description of a users music preferences, you will recommend songs tailored to the user's preferences."
            },
            {
                "role": "user",
                "content": f"Create a playlist with {song_count} songs that fits the following description '''{prompt}'''. Come up with a creative and unique name for the playlist."
            },
        ],
        functions=[
                {
                    "name": "create_playlist",
                    "description": "Creates a spotify playlist based on a list of songs that should be added to the list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "playlist_name": {
                                "type": "string",
                                "description": "Name of playlist",
                            },
                            "playlist_description": {
                                "type": "string",
                                "description": "Description for the playlist. Please add that this playlist was generated by an AI.",
                            },
                            "songs": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "songname": {
                                            "type": "string",
                                            "description": "Name of the song that should be added to the playlist",
                                        },
                                        "artists": {
                                            "type": "array",
                                            "description": "List of all artists",
                                            "items": {
                                                "type": "string",
                                                "description": "Name of artist of the song",
                                            },
                                        },
                                    },
                                    "required": ["songname", "artists"],
                                },
                            },
                        },
                        "required": ["songs", "playlist_name", "playlist_description"],
                    },
                }
            ],
    )
    arguments = json.loads(response.choices[0].message.function_call.arguments)

    #st.write(arguments)
    playlist_name = "AI - " + arguments["playlist_name"]
    playlist_description = arguments["playlist_description"]
    recommended_songs = arguments["songs"]
    
    song_uris = [
            spotify_client.search(
                q=f"{song['songname']} {','.join(song['artists'])}", limit=1
            )["tracks"]["items"][0]["uri"]
            for song in recommended_songs
        ]
    #st.write(song_uris)
    user_id = spotify_client.me()["id"]
    playlist = spotify_client.user_playlist_create(user_id, playlist_name, False, description=playlist_description) # create playlist
    playlist_id = playlist["id"]
    spotify_client.playlist_add_items(playlist_id, song_uris) # add items

    st.write(
        f"Playlist created <a href='{playlist['external_urls']['spotify']}'>Click</a>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()