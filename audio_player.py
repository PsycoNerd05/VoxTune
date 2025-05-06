import mutagen
import pygame

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.paused = False
        self.volume = 0.5

    def load(self, filepath):
        try:
            pygame.mixer.music.load(filepath)
            self.current_track = filepath
        except pygame.error as e:
            print(f"Error loading {filepath}: {e}")
            self.current_track = None

    def play(self):
        if self.current_track:
            try:
                pygame.mixer.music.play()
                self.paused = False
            except Exception as e:
                print(f"Error while trying to play: {e}")

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def unpause(self):
        if self.paused and self.current_track:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None
        self.paused = False

    def next(self, playlist):
        if not playlist or not self.current_track:
            return None
        try:
            current_index = playlist.index(self.current_track)
            next_index = (current_index + 1) % len(playlist)
            next_track = playlist[next_index]
            self.load(next_track)
            self.play()
            return next_track
        except ValueError:
            return None # Current track not in playlist

    def prev(self, playlist):
        if not playlist or not self.current_track:
            return None
        try:
            current_index = playlist.index(self.current_track)
            prev_index = (current_index - 1 + len(playlist)) % len(playlist)
            prev_track = playlist[prev_index]
            self.load(prev_track)
            self.play()
            return prev_track
        except ValueError:
            return None

    def skip_forward(self, seconds=5):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000  # in seconds
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(start=current_pos + seconds)

    def skip_backward(self, seconds=5):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000  # in seconds
            rewind_to = max(0, current_pos - seconds)
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(start=rewind_to)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def get_volume(self):
        return self.volume

    def get_current_time(self):
        if pygame.mixer.music.get_busy():
            return pygame.mixer.music.get_pos() / 1000  # in seconds
        return 0

    def get_track_length(self):
        if self.current_track:
            try:
                audio = mutagen.File(self.current_track)
                return audio.info.length
            except mutagen.MutagenError:
                return 0
        return 0
