import streamlit as st
class display():
    def __int__(self, prompt, song_count, submitted):
        self.prompt = prompt
        self.song_count = song_count
        self.submitted = submitted
    
    def decor(self):
        st.title("Welcome to VibeGen :headphones::notes:")
        st.markdown('''
                    Music should always fit the vibe! So why not try and find the perfect playlist that is the mood?''')
        
    def ask(self):
        with st.form("VibeGen: Playlist Generator"):
            self.prompt = st.text_input("Describe the music playlist you'd like to generate...")
            self.song_count = st.slider("Songs",1, 30, 10)
            self.submitted = st.form_submit_button("Create")
            if not self.submitted:
                return
  
if __name__ == "__main__":
    d = display()
    d.decor()
    d.ask()
