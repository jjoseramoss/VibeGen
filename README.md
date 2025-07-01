# VibeGen 🎵 - AI Powered Spotify Playlist Generator

Welcome to **VibeGen** — the AI-driven tool that creates the perfect Spotify playlists based on your vibe, mood, or activity!  
Built with a focus on **Object-Oriented Programming (OOP)** principles.

---

## 🚀 Features
- 🎷 Generate playlists based on any vibe, mood, or activity you describe
- 🤖 Smart AI (powered by OpenAI) ensures real, popular songs that match the vibe
- 🎵 Directly creates and saves playlists to your Spotify account
- 📚 View history of all playlists you've generated
- 🎨 Clean and user-friendly CLI + web interface (Streamlit)

---

## 🧐 Technologies Used
- **Python 3.11+**
- **Streamlit** (for UI)
- **Spotipy** (Spotify API integration)
- **OpenAI API** (ChatGPT model for smart music recommendation)
- **Local JSON** (playlist storage and retrieval)
- **OOP Principles**:
  - Encapsulation
  - Inheritance
  - Polymorphism

---

## 💖 How It Works
1. Log into your Spotify account securely.
2. Describe your mood or vibe (e.g., "chill study night" or "hype gym session").
3. VibeGen generates a curated playlist with real, popular songs matching your description.
4. Playlist is saved to your Spotify account instantly.
5. Past playlists are stored locally and viewable anytime.

---

## 📸 Screenshot
- [![Demo of login page](/python_project/VibeGen/Project%20Details/vibegen-gif.gif)] 


---

## 🔥 Setup Instructions

1. Clone the repository
2. Create a `.env` file with:
    ```
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    REDIRECT_URI=http://localhost:8501
    OPENAI_API_KEY=your_openai_api_key
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run locally:
    ```bash
    streamlit run main.py
    ```

---

## ✨ Future Improvements
- Add support for user authentication persistence (multi-user login)
- Mood presets for faster playlist generation
- Deploy on a public server

---
