# This class extends Playlist and represents playlists created by users.
import playlist

class UserPlaylist(playlist.Playlist):
    def __init__(self, name, user):
        super().__init__(name)
        self.__user = user # username of who created the playlist
    
    def remove_playlist(self):
        pass