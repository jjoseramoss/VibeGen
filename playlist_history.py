import os
import json

class PlaylistHistory:
    def __init__(self, storage_path="history"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
    
    def save_playlist(self, playlist_data):
        filename = f"{playlist_data['playlist_name'].replace(' ', '_')}.json"
        full_path = os.path.join(self.storage_path, filename)
        with open(full_path, "w") as f:
            json.dump(playlist_data, f, indent=4)
    
    def load_all_playlists(self):
        playlists = []
        for file in os.listdir(self.storage_path):
            if file.endswith(".json"):
                with open(os.path.join(self.storage_path, file), "r") as f:
                    playlists.append(json.load(f))
        return playlists