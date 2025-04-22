from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel, QListWidgetItem, \
    QMessageBox
from PyQt5.QtCore import Qt
from ui.components import SongListItem

class FavoritesPage(QWidget):
    def __init__(self, favorites_manager, library_manager, audio_player, main_window, parent=None):
        super().__init__(parent)
        self.favorites_manager = favorites_manager
        self.library_manager = library_manager
        self.audio_player = audio_player
        self.main_window = main_window  # To interact with the main window
        self.layout = QVBoxLayout(self)

        # Title Label
        self.title_label = QLabel("My Favorite Songs")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Favorites List
        self.favorites_list_widget = QListWidget()
        self._populate_favorites()
        self.layout.addWidget(self.favorites_list_widget)
        self.favorites_list_widget.itemDoubleClicked.connect(self._play_selected_favorite)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh Favorites")
        self.refresh_button.clicked.connect(self._populate_favorites)
        self.clear_button = QPushButton("Clear All Favorites")
        self.clear_button.clicked.connect(self._clear_favorites)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.clear_button)
        self.layout.addLayout(buttons_layout)

        # Apply button styles
        self._apply_button_style(self.refresh_button)
        self._apply_button_style(self.clear_button)

    def _apply_button_style(self, button):
        stylesheet = """
            QPushButton {
                background-color: transparent;
                border: 1px solid #00FF00; /* Neon Green Border */
                color: #00FF00; /* Neon Green Text */
                padding: 5px;
                border-radius: 3px;
                min-width: 140px; /* Adjusted min-width for longer text */
                text-align: center;
            }
            QPushButton:hover {
                background-color: #460060; /* Darker purple on hover */
                color: #00CC00; /* Slightly darker neon green on hover */
                border-color: #00CC00;
            }
            QPushButton:pressed {
                background-color: #00FF00;
                color: black;
                border-color: black;
            }
        """
        button.setStyleSheet(stylesheet)

    def _populate_favorites(self):
        self.favorites_list_widget.clear()
        favorite_songs = self.favorites_manager.get_favorites()  # Returns a list of (filepath, play_count) tuples
        if not favorite_songs:
            self.favorites_list_widget.addItem("No favorite songs yet.")  # Add a message
            self.favorites_list_widget.setDisabled(True)
        else:
            self.favorites_list_widget.setDisabled(False)
            for filepath, play_count in favorite_songs:
                song_info = self.library_manager.songs.get(filepath)  # Get song info from LibraryManager
                if song_info:
                    song_info['play_count'] = play_count # Add play count to the song info.
                    item = SongListItem(song_info)
                    list_item = QListWidgetItem()
                    list_item.setSizeHint(item.sizeHint())
                    self.favorites_list_widget.addItem(list_item)
                    self.favorites_list_widget.setItemWidget(list_item, item)

    def _clear_favorites(self):
        #  No direct method to clear all favorites in FavoritesManager.
        #  Remove them one by one.
        favorite_songs = self.favorites_manager.get_favorites()
        if not favorite_songs:
            QMessageBox.information(self, "Info", "No favorite songs to clear.")
            return

        reply = QMessageBox.question(self, "Clear Favorites",
                                     "Are you sure you want to clear all your favorite songs?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for filepath, _ in favorite_songs:
                self.favorites_manager.remove_from_favorites(filepath)
            self._populate_favorites()  # Refresh the list
            QMessageBox.information(self, "Info", "Favorites list cleared.")

    def _play_selected_favorite(self, item):
        widget = self.favorites_list_widget.itemWidget(item)
        if widget and widget.song_info:
            song = widget.song_info
            self.main_window._play_selected_song_from_list(song)  # Use the general play function
            self.main_window.current_playlist = [filepath for filepath, _ in self.favorites_manager.get_favorites()] # Update current playlist