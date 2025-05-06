import json
import os
from collections import Counter

class FavoritesManager:
    def __init__(self, data_file, max_size=20):
        self.data_file = data_file
        self.max_size = max_size
        self.play_counts = self._load_favorites()

    def _load_favorites(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    data = json.load(f)
                    return Counter(data.get('favorites', {}))
                except json.JSONDecodeError:
                    return Counter()
        return Counter()

    def _save_favorites(self):
        data = {'favorites': dict(self.play_counts)}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_to_favorites(self, song_filepath):
        self.play_counts[song_filepath] += 1
        self._save_favorites()
        self._sort_and_trim()

    def remove_from_favorites(self, song_filepath):
        if song_filepath in self.play_counts:
            del self.play_counts[song_filepath]
            self._save_favorites()

    def get_favorites(self):
        return self.play_counts.most_common(self.max_size)

    def get_play_count(self, song_filepath):
        return self.play_counts.get(song_filepath, 0)

    def _sort_and_trim(self):
        most_common = self.play_counts.most_common(self.max_size)
        self.play_counts = Counter(dict(most_common))
        self._save_favorites()
