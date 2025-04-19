import json
import os

class PlaylistManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.playlists = self._load_playlists()

    def _load_playlists(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    data = json.load(f)
                    return data.get('playlists', {})
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_playlists(self):
        data = {'playlists': self.playlists}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def create_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = []
            self._save_playlists()
            return True
        return False

    def get_playlists(self):
        return list(self.playlists.keys())

    def get_playlist_songs(self, name):
        return self.playlists.get(name, [])

    def add_song_to_playlist(self, playlist_name, song_filepath):
        if playlist_name in self.playlists and song_filepath not in self.playlists[playlist_name]:
            self.playlists[playlist_name].append(song_filepath)
            self._save_playlists()
            return True
        return False

    def remove_song_from_playlist(self, playlist_name, song_filepath):
        if playlist_name in self.playlists and song_filepath in self.playlists[playlist_name]:
            self.playlists[playlist_name].remove(song_filepath)
            self._save_playlists()
            return True
        return False

    def delete_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]
            self._save_playlists()
            return True
        return False

    def shuffle_playlist(self, playlist_name):
        if playlist_name in self.playlists:
            import random
            random.shuffle(self.playlists[playlist_name])
            self._save_playlists()
            return True
        return False