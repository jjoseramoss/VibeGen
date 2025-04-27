import os
import json
import re


class PlaylistHistory:
    def __init__(self, storage_path="history"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    @staticmethod
    def sanitize_filename(name):
        # Remove illegal characters for filenames
        safe_name = re.sub(r'[<>:"/\\|?*]', '', name)
        safe_name = safe_name.strip().replace(' ', '_')
        return safe_name
    
    
    def save_playlist(self, playlist_data):
        safe_name = self.sanitize_filename(playlist_data['playlist_name'])
        filename = f"{safe_name}.json"
        full_path = os.path.join(self.storage_path, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(playlist_data, f, indent=4, ensure_ascii=False)
    
    def load_all_playlists(self):
        playlists = []
        for file in os.listdir(self.storage_path):
            if file.endswith(".json"):
                with open(os.path.join(self.storage_path, file), "r") as f:
                    playlists.append(json.load(f))
        return playlists