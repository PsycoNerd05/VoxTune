from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class SongListItem(QWidget):
    def __init__(self, song_info, parent=None):
        super().__init__(parent)
        self.song_info = song_info  # Store the song information
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)  # Add some vertical margin

        # Create labels for song information
        title_label = QLabel(song_info['title'])
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        artist_label = QLabel(song_info['artist'])
        artist_label.setFont(QFont("Arial", 10))
        album_label = QLabel(song_info['album'])
        album_label.setFont(QFont("Arial", 10, italic=True))

        # Use QHBoxLayout for title and artist, and put album below
        title_artist_layout = QHBoxLayout()
        title_artist_layout.addWidget(title_label)
        title_artist_layout.addWidget(artist_label)
        title_artist_layout.addStretch(1)  # Push title and artist to the left

        self.layout.addLayout(title_artist_layout)
        self.layout.addWidget(album_label)

        if 'play_count' in song_info:
            play_count_label = QLabel(f"Play Count: {song_info['play_count']}")
            play_count_label.setFont(QFont("Arial", 10))
            self.layout.addWidget(play_count_label)
        else:
             play_count_label = QLabel("")
             self.layout.addWidget(play_count_label)

        self.setStyleSheet("background-color: #1E0028; color: white;")
        title_label.setStyleSheet("color: #FFFFFF;")
        artist_label.setStyleSheet("color: #EEEEEE;")
        album_label.setStyleSheet("color: #CCCCCC;")

        # Calculate the minimum size based on the layout
        self.minimum_height = self.layout.minimumSize().height()
        self.minimumWidth = self.layout.minimumSize().width()  # Corrected spelling

    def sizeHint(self):
        # Return the minimum size required by the layout
        return QSize(self.minimumWidth, self.minimum_height)  # Corrected spelling here too
