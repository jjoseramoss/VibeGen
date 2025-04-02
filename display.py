import streamlit as st
import spotipy
import openai
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

class display():
    def __int__(self, auth_url, query_param, prompt, song_count, submitted):
        self.auth_url = auth_url
        self.query_param = query_param
        self.prompt = prompt
        self.song_count = song_count
        self.submitted = submitted
    
    def login_display(self):
        st.title("LogIn")
        st.markdown('''
                    ''')
        self.auth_url = f"https://accounts.spotify.com/authorize?client_id={os.environ['SPOTIFY_CLIENT_ID']}&response_type=code&redirect_uri=http://localhost:8501&scope=playlist-modify-private"
        self.query_param = st._get_query_params()
        if self.query_param:
            return self.query_param["code"][0]
        st.write(
            f"Please log in to <a target='_self' href='{self.auth_url}'>spotify",
            unsafe_allow_html=True,
        )
        self.query_param = st._get_query_params()
        if self.query_param:
            return self.query_param["code"][0]
        
    def decor(self):
        st.title("Welcome to :blue[VibeGen] :headphones::notes:")
        st.divider()
        st.markdown('''
                    Music should always fit the vibe! So why not try and find the perfect playlist that fits the mood?''')
        
    def ask(self):
        with st.form("VibeGen: Playlist Generator"):
            self.prompt = st.text_input("Describe the music playlist you'd like to generate...")
            self.song_count = st.slider("Songs",1, 30, 10)
            self.submitted = st.form_submit_button("Create")
            if not self.submitted:
                return
  
if __name__ == "__main__":
    d = display()
    d.login_display()
    d.decor()
    d.ask()
