import os
import mutagen
import datetime

class LibraryManager:
    def __init__(self, music_directory):
        self.music_directory = music_directory
        self.songs = {} # {filepath: {title, artist, album, release_date, filepath}}
        self.albums = {} # {artist: {album_name: [filepaths]}}

    def scan_library(self):
        self.songs = {}
        for root, _, files in os.walk(self.music_directory):
            for file in files:
                if file.endswith(('.mp3', '.flac', '.wav', '.ogg')): # Add more formats as needed
                    filepath = os.path.join(root, file)
                    try:
                        audio_info = mutagen.File(filepath)
                        title = audio_info.get('TIT2', [file])[0]
                        artist = audio_info.get('TPE1', ['Unknown Artist'])[0]
                        album = audio_info.get('TALB', ['Unknown Album'])[0]
                        release_date_str = audio_info.get('TDRC', [''])[0]
                        release_date = None
                        if release_date_str:
                            try:
                                release_date = datetime.datetime.strptime(str(release_date_str), '%Y').date()
                            except ValueError:
                                pass
                        self.songs[filepath] = {'title': str(title), 'artist': str(artist), 'album': str(album), 'release_date': release_date, 'filepath': filepath}
                    except mutagen.MutagenError:
                        print(f"Error reading metadata from {filepath}")
        self._create_albums()
        return list(self.songs.values())

    def _create_albums(self):
        self.albums = {}
        for song_info in self.songs.values():
            artist = song_info['artist']
            album = song_info['album']
            filepath = song_info['filepath']
            if artist not in self.albums:
                self.albums[artist] = {}
            if album not in self.albums[artist]:
                self.albums[artist][album] = []
            self.albums[artist][album].append(filepath)
        for artist_albums in self.albums.values():
            for album_files in artist_albums.values():
                album_files.sort(key=lambda fp: self.songs[fp].get('release_date') or datetime.date.min)

    def delete_song(self, filepath):
        if filepath in self.songs:
            del self.songs[filepath]
            try:
                os.remove(filepath)
                self._create_albums() # Re-scan albums after deletion
                return True
            except OSError as e:
                print(f"Error deleting {filepath}: {e}")
                return False
        return False

    def get_all_songs(self):
        return list(self.songs.values())

    def sort_songs(self, song_list, sort_by, ascending=True):
        if sort_by == 'name':
            return sorted(song_list, key=lambda song: song['title'].lower(), reverse=not ascending)
        elif sort_by == 'date':
            return sorted(song_list, key=lambda song: song.get('release_date') or datetime.date.min, reverse=not ascending)
        return song_list

    def get_albums_by_artist(self, artist):
        return self.albums.get(artist, {})