class Playlist: 
    def __init__(self, name, songs=None):
        self.name = name
        self.songs = songs if songs else [] # list of song dictionaries

    def add_songs(self, song):
        pass

    def display_playlist(self):
        pass

    def edit_playlist_name(self, newName):
        pass