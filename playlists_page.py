from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QPushButton,
                             QInputDialog, QMessageBox, QHBoxLayout, QListWidgetItem)
from PyQt5.QtCore import Qt
from ui.components import SongListItem

class PlaylistsPage(QWidget):
    def __init__(self, playlist_manager, library_manager, audio_player, main_window, parent=None):
        super().__init__(parent)
        self.playlist_manager = playlist_manager
        self.library_manager = library_manager
        self.audio_player = audio_player
        self.main_window = main_window
        self.layout = QVBoxLayout(self)

        # Playlist List
        self.playlist_list_widget = QListWidget()
        self._populate_playlists()
        self.layout.addWidget(self.playlist_list_widget)
        self.playlist_list_widget.itemDoubleClicked.connect(self._show_playlist_songs)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        self.add_playlist_button = QPushButton("Create Playlist")
        self.add_playlist_button.clicked.connect(self._create_new_playlist)
        self.delete_playlist_button = QPushButton("Delete Playlist")
        self.delete_playlist_button.clicked.connect(self._delete_selected_playlist)
        self.view_songs_button = QPushButton("View Playlist Songs")
        self.view_songs_button.clicked.connect(self._show_playlist_songs)
        buttons_layout.addWidget(self.add_playlist_button)
        buttons_layout.addWidget(self.delete_playlist_button)
        buttons_layout.addWidget(self.view_songs_button)
        self.layout.addLayout(buttons_layout)
        self._apply_button_style(self.add_playlist_button)
        self._apply_button_style(self.delete_playlist_button)
        self._apply_button_style(self.view_songs_button)

        # Song List for Selected Playlist (Initially Hidden)
        self.playlist_songs_widget = QListWidget()
        self.playlist_songs_widget.setVisible(False)
        self.layout.addWidget(self.playlist_songs_widget)
        self.playlist_songs_widget.itemDoubleClicked.connect(self._play_selected_playlist_song)

        # Buttons for Managing Songs in Playlist (Initially Hidden)
        self.remove_song_button = QPushButton("Remove Song")
        self.remove_song_button.clicked.connect(self._remove_song_from_playlist)
        self.play_playlist_button = QPushButton("Play Playlist")
        self.play_playlist_button.clicked.connect(self._play_current_playlist)
        self.back_to_playlists_button = QPushButton("Back to Playlists", clicked=self._hide_playlist_songs_view)

        self.manage_songs_widget = QWidget() # Create a container widget for the buttons
        self.manage_songs_layout = QHBoxLayout(self.manage_songs_widget)
        self.manage_songs_layout.addWidget(self.remove_song_button)
        self.manage_songs_layout.addWidget(self.play_playlist_button)
        self.manage_songs_layout.addWidget(self.back_to_playlists_button)
        self.layout.addWidget(self.manage_songs_widget)
        self.manage_songs_widget.setVisible(False) # Hide the container widget
        self._apply_button_style(self.remove_song_button)
        self._apply_button_style(self.play_playlist_button)
        self._apply_button_style(self.back_to_playlists_button)

        self.current_playlist_name = None

    def _apply_button_style(self, button):
        stylesheet = """
            QPushButton {
                background-color: transparent;
                border: 1px solid #00FF00; /* Neon Green Border */
                color: #00FF00; /* Neon Green Text */
                padding: 5px;
                border-radius: 3px;
                min-width: 120px; /* Increased min-width for longer text */
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

    def _populate_playlists(self):
        self.playlist_list_widget.clear()
        playlists = self.playlist_manager.get_playlists()
        for playlist_name in playlists:
            self.playlist_list_widget.addItem(playlist_name)

    def _create_new_playlist(self):
        text, ok = QInputDialog.getText(self, "Create New Playlist", "Enter playlist name:")
        if ok and text:
            if self.playlist_manager.create_playlist(text):
                self._populate_playlists()
            else:
                QMessageBox.warning(self, "Warning", f"Playlist '{text}' already exists.")

    def _delete_selected_playlist(self):
        selected_item = self.playlist_list_widget.currentItem()
        if selected_item:
            playlist_name = selected_item.text()
            reply = QMessageBox.question(self, "Delete Playlist",
                                         f"Are you sure you want to delete '{playlist_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.playlist_manager.delete_playlist(playlist_name):
                    self._populate_playlists()
                    self._hide_playlist_songs_view() # Hide song list if it was open
                else:
                    QMessageBox.critical(self, "Error", f"Could not delete playlist '{playlist_name}'.")

    def _show_playlist_songs(self):
        selected_item = self.playlist_list_widget.currentItem()
        if selected_item:
            self.current_playlist_name = selected_item.text()
            songs_in_playlist = self.playlist_manager.get_playlist_songs(self.current_playlist_name)
            self.playlist_songs_widget.clear()
            if songs_in_playlist:
                for filepath in songs_in_playlist:
                    song_info = self.library_manager.songs.get(filepath)
                    if song_info:
                        item = SongListItem(song_info)
                        list_item = QListWidgetItem()
                        list_item.setSizeHint(item.sizeHint())
                        self.playlist_songs_widget.addItem(list_item)
                        self.playlist_songs_widget.setItemWidget(list_item, item)
            else:
                QMessageBox.information(self, "Info", f"Playlist '{self.current_playlist_name}' is empty.")

            self.playlist_list_widget.setVisible(False)
            self.view_songs_button.setVisible(False)
            self.playlist_songs_widget.setVisible(True)
            self.manage_songs_widget.setVisible(True) # Show the container widget

    def _hide_playlist_songs_view(self):
        self.playlist_songs_widget.setVisible(False)
        self.manage_songs_widget.setVisible(False) # Hide the container widget
        self.playlist_list_widget.setVisible(True)
        self.view_songs_button.setVisible(True)
        self.current_playlist_name = None

    def _remove_song_from_playlist(self):
        selected_item = self.playlist_songs_widget.currentItem()
        if selected_item and self.current_playlist_name:
            widget = self.playlist_songs_widget.itemWidget(selected_item)
            if widget and widget.song_info:
                song_filepath = widget.song_info['filepath']
                song_title = widget.song_info['title']
                if self.playlist_manager.remove_song_from_playlist(self.current_playlist_name, song_filepath):
                    self._show_playlist_songs() # Refresh the song list
                    QMessageBox.information(self, "Info", f"'{song_title}' removed from '{self.current_playlist_name}'.")
                else:
                    QMessageBox.critical(self, "Error", f"Could not remove '{song_title}' from '{self.current_playlist_name}'.")

    def _play_selected_playlist_song(self, item):
        widget = self.playlist_songs_widget.itemWidget(item)
        if widget and widget.song_info:
            song = widget.song_info
            self.main_window._play_selected_song_from_list(song) # Use a general play function in main window
            self.main_window.current_playlist = self.playlist_manager.get_playlist_songs(self.current_playlist_name) # Update current playlist

    def _play_current_playlist(self):
        if self.current_playlist_name:
            playlist_songs = self.playlist_manager.get_playlist_songs(self.current_playlist_name)
            if playlist_songs:
                self.main_window.play_virtual_playlist(playlist_songs)
            else:
                QMessageBox.information(self, "Info", f"Playlist '{self.current_playlist_name}' is empty.")