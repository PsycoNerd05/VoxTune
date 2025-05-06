from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel,
                             QScrollArea, QFrame)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AlbumsPage(QWidget):
    def __init__(self, library_manager, parent=None):
        super().__init__(parent)
        self.library_manager = library_manager
        self.layout = QVBoxLayout(self)

        # Title Label
        title_label = QLabel("My Albums")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(title_label)

        # Scroll Area to contain the albums grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.albums_content = QWidget()
        self.grid_layout = QGridLayout(self.albums_content)
        self.scroll_area.setWidget(self.albums_content)
        self.layout.addWidget(self.scroll_area)

        self._populate_albums()

    def _populate_albums(self):
        # Clear any existing widgets in the grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        albums_data = self.library_manager.albums
        row = 0
        col = 0
        for artist, albums in albums_data.items():
            for album_name in sorted(albums.keys()):
                album_widget = self._create_album_widget(artist, album_name, len(albums[album_name]))
                self.grid_layout.addWidget(album_widget, row, col)
                col += 1
                if col > 2:  # Display 3 albums per row
                    col = 0
                    row += 1

        # Add a stretch at the end to prevent empty space if the grid doesn't fill the last row
        self.grid_layout.addItem(QVBoxLayout(), row + 1, 0, 1, self.grid_layout.columnCount())

    def _create_album_widget(self, artist, album_name, song_count):
        album_frame = QFrame()
        album_frame_layout = QVBoxLayout(album_frame)
        album_frame.setStyleSheet("background-color: #28003C; border-radius: 5px; padding: 10px;")

        album_label = QLabel(album_name)
        album_label.setFont(QFont("Arial", 12, QFont.Bold))
        album_label.setAlignment(Qt.AlignCenter)
        album_label.setStyleSheet("color: #FFFFFF;")
        album_frame_layout.addWidget(album_label)

        artist_label = QLabel(artist)
        artist_label.setFont(QFont("Arial", 10, italic=True))  # Corrected line: using keyword argument
        artist_label.setAlignment(Qt.AlignCenter)
        artist_label.setStyleSheet("color: #AAAAAA;")
        album_frame_layout.addWidget(artist_label)

        count_label = QLabel(f"{song_count} songs")
        count_label.setFont(QFont("Arial", 9))
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("color: #BBBBBB;")
        album_frame_layout.addWidget(count_label)

        # You could add a placeholder for album art here if you have that functionality

        return album_frame

    def apply_theme(self):
        """
        Apply consistent theming to the AlbumsPage.
        """
        # Modify the main background and album grid style
        self.setStyleSheet("background-color: #28003C; color: white;")
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QFrame):
                widget.setStyleSheet("background-color: #320046; border-radius: 5px; padding: 10px;")
