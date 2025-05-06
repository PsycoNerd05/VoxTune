from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt


class PlaylistsPage(QWidget):
    def __init__(self, playlist_manager, library_manager, audio_player, main_window):
        super().__init__()
        self.playlist_manager = playlist_manager
        self.library_manager = library_manager
        self.audio_player = audio_player
        self.main_window = main_window

        # Initialize UI components
        self.layout = QVBoxLayout(self)
        self.playlist_list_widget = QListWidget()
        self.add_playlist_button = QPushButton("Add Playlist")
        self.delete_playlist_button = QPushButton("Delete Playlist")
        self.view_songs_button = QPushButton("View Songs")
        self.play_playlist_button = QPushButton("Play Playlist")
        self.back_to_playlists_button = QPushButton("Back to Playlists")
        self.remove_song_button = QPushButton("Remove Song")
        self.manage_songs_widget = QWidget()
        self.manage_songs_layout = QVBoxLayout(self.manage_songs_widget)
        self.playlist_songs_widget = QListWidget()
        self.current_playlist_name = None  # Hold the name of the currently selected playlist

        # Add widgets to the layout
        self.layout.addWidget(self.playlist_list_widget)
        self.layout.addWidget(self.add_playlist_button)
        self.layout.addWidget(self.delete_playlist_button)
        self.layout.addWidget(self.view_songs_button)
        self.layout.addWidget(self.play_playlist_button)
        self.layout.addWidget(self.manage_songs_widget)

        # Apply button styles
        self._apply_button_style()

    def apply_theme(self):
        """
        Apply a consistent theme to the PlaylistsPage widget and all its components.
        """
        self.setStyleSheet("""
            QWidget {
                background-color: #320046;
                color: white;
            }
            QPushButton {
                background-color: #460060;
                color: white;
                border: none;
                margin: 5px;
                padding: 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #00FF00;
                color: black;
            }
            QPushButton:pressed {
                background-color: #00CC00;
                color: white;
            }
            QListWidget {
                background-color: #28003C;
                color: white;
                border: 1px solid #460060;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #460060;
                color: #00FF00;
            }
        """)

    def _apply_button_style(self):
        """
        Set consistent styling for the buttons in the widget.
        """
        button_stylesheet = """
        QPushButton {
            background-color: #460060;
            color: white;
            border: none;
            margin: 5px;
            padding: 10px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #00FF00;
            color: black;
        }
        QPushButton:pressed {
            background-color: #00CC00;
            color: white;
        }
        """
        self.add_playlist_button.setStyleSheet(button_stylesheet)
        self.delete_playlist_button.setStyleSheet(button_stylesheet)
        self.view_songs_button.setStyleSheet(button_stylesheet)
        self.play_playlist_button.setStyleSheet(button_stylesheet)
        self.back_to_playlists_button.setStyleSheet(button_stylesheet)
        self.remove_song_button.setStyleSheet(button_stylesheet)

    # Placeholder method (implementation depends on your data model)
    def _populate_playlists(self):
        """
        Populate the playlist list widget with playlist names.
        This should fetch playlist details from the playlist_manager.
        """
        self.playlist_list_widget.clear()
        playlists = self.playlist_manager.get_all_playlists()
        for playlist in playlists:
            self.playlist_list_widget.addItem(playlist.name)

    # Other methods for playlist management and interaction ...
