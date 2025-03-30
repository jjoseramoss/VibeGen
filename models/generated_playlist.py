import playlist

class GeneratedPlaylist(playlist.Playlist):
    def __init__(self, name, mood):
        super().__init__(name)
        self.mood = mood

    def display_playlist(self): # overrides parent display
        super().display_playlist()