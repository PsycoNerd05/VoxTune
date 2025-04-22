from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QLabel, QPushButton, QSpacerItem,
                             QSizePolicy, QStackedWidget, QInputDialog,
                             QMessageBox, QToolBar, QAction, QListWidgetItem)
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPalette, QPainter
from PyQt5.QtCore import Qt, QTimer, QSize

from ui.playlists_page import PlaylistsPage
from ui.albums_page import AlbumsPage
from ui.favorites_page import FavoritesPage
from ui.components import SongListItem
from core.audio_player import AudioPlayer
from core.library_manager import LibraryManager
from core.playlist_manager import PlaylistManager
from core.favorites_manager import FavoritesManager
from voice.voice_assistant import VoiceAssistant

class MainWindow(QMainWindow):
    def __init__(self, library_manager, playlist_manager, audio_player, favorites_manager):
        super().__init__()
        self.library_manager = library_manager
        self.playlist_manager = playlist_manager
        self.audio_player = audio_player
        self.favorites_manager = favorites_manager
        self.voice_assistant = VoiceAssistant("VoxTune", library_manager, playlist_manager, audio_player, self)

        self.setWindowTitle("VoxTune")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.side_nav = QWidget()
        self._setup_side_navigation()
        self.layout.addWidget(self.side_nav)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.stacked_widget = QStackedWidget()
        self._setup_main_page()
        self.playlists_page = PlaylistsPage(playlist_manager, library_manager, audio_player, self)
        self.albums_page = AlbumsPage(library_manager)
        self.favorites_page = FavoritesPage(favorites_manager, library_manager, audio_player, self)

        self.stacked_widget.addWidget(self.main_page_widget)
        self.stacked_widget.addWidget(self.playlists_page)
        self.stacked_widget.addWidget(self.albums_page)
        self.stacked_widget.addWidget(self.favorites_page)
        self.content_layout.addWidget(self.stacked_widget)

        self.playback_controls_widget = QWidget()
        self._setup_playback_controls()
        self.content_layout.addWidget(self.playback_controls_widget)

        self.layout.addWidget(self.content_widget) # Ensure content widget is added to the main layout

        self._apply_theme()
        self.voice_assistant.start()

    def closeEvent(self, event):
        self.voice_assistant.stop()
        super().closeEvent(event)

    def _play_selected_song_from_list(self, song):
        self.audio_player.load(song['filepath'])
        self.audio_player.play()
        self._update_current_song_info(song)
        self.play_pause_button.setIcon(QIcon("ui/neon_pause.png")) # Assuming you have a neon pause icon
        self.current_playlist = [s['filepath'] for s in
                                 self.library_manager.get_all_songs()]  # Or update based on the source list

    def _setup_side_navigation(self):
        self.side_nav_layout = QVBoxLayout(self.side_nav)
        self.main_button = QPushButton("Main Page")
        self.playlists_button = QPushButton("Playlists")
        self.albums_button = QPushButton("Albums")
        self.favorites_button = QPushButton("Favorites")

        # Make the text bigger and bold (programmatically)
        font = self.main_button.font()
        font.setPointSize(16)  # Increased font size
        font.setBold(True)
        self.main_button.setFont(font)
        self.playlists_button.setFont(font)
        self.albums_button.setFont(font)
        self.favorites_button.setFont(font)

        self.main_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.playlists_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.albums_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.favorites_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        self.side_nav_layout.addWidget(self.main_button)
        self.side_nav_layout.addWidget(self.playlists_button)
        self.side_nav_layout.addWidget(self.albums_button)
        self.side_nav_layout.addWidget(self.favorites_button)
        self.side_nav.setFixedWidth(250) # Increased width further for better spacing

    def _setup_main_page(self):
        self.main_page_widget = QWidget()
        self.main_page_layout = QVBoxLayout(self.main_page_widget)

        self.app_name_label = QLabel("VoxTune")
        self.app_name_label.setAlignment(Qt.AlignCenter)
        self.app_name_label.setStyleSheet("font-size: 24px; color: #00FF00;")
        self.main_page_layout.addWidget(self.app_name_label)
        self.app_name_timer = QTimer(self)
        self.app_name_timer.timeout.connect(self._hide_app_name)
        self.app_name_timer.start(5000)
        self.initial_display = True

        self.virtual_playlist_widget = QListWidget()
        self._populate_virtual_playlist()
        self.main_page_layout.addWidget(self.virtual_playlist_widget)
        self.virtual_playlist_widget.itemDoubleClicked.connect(self._play_selected_song)

    def _hide_app_name(self):
        self.app_name_label.hide()
        self.app_name_timer.stop()
        self.initial_display = False

    def _populate_virtual_playlist(self):
        self.virtual_playlist_widget.clear()
        songs = self.library_manager.scan_library()
        for song in songs:
            item = SongListItem(song)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())
            self.virtual_playlist_widget.addItem(list_item)
            self.virtual_playlist_widget.setItemWidget(list_item, item)

    def refresh_virtual_playlist(self):
        self._populate_virtual_playlist()

    def sort_virtual_playlist(self, sort_by, ascending):
        songs = self.library_manager.get_all_songs()
        sorted_songs = self.library_manager.sort_songs(songs, sort_by, ascending)
        self._populate_virtual_playlist_with_list(sorted_songs)

    def _populate_virtual_playlist_with_list(self, song_list):
        self.virtual_playlist_widget.clear()
        for song in song_list:
            item = SongListItem(song)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())
            self.virtual_playlist_widget.addItem(list_item)
            self.virtual_playlist_widget.setItemWidget(list_item, item)

    def _setup_playback_controls(self):
        self.playback_controls_widget = QWidget()
        controls_layout = QHBoxLayout(self.playback_controls_widget)

        self.current_album_art = QLabel()
        pixmap = QPixmap(60, 60)
        pixmap.fill(Qt.gray)
        self.current_album_art.setPixmap(pixmap)
        controls_layout.addWidget(self.current_album_art)

        self.current_song_info = QLabel("No song playing")
        controls_layout.addWidget(self.current_song_info)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        controls_layout.addItem(spacer)

        icon_path = "ui/"  # Path to your neon icon directory

        self.prev_button = QPushButton(QIcon(icon_path + "neon_prev.png"), "")
        self.skip_backward_button = QPushButton(QIcon(icon_path + "neon_rewind.png"), "<<5")
        self.play_pause_button = QPushButton(QIcon(icon_path + "neon_play.png"), "")
        self.skip_forward_button = QPushButton(QIcon(icon_path + "neon_fast_forward.png"), ">>5")
        self.next_button = QPushButton(QIcon(icon_path + "neon_next.png"), "")

        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.skip_backward_button)
        controls_layout.addWidget(self.play_pause_button)
        controls_layout.addWidget(self.skip_forward_button)
        controls_layout.addWidget(self.next_button)

        self.play_pause_button.clicked.connect(self._toggle_play_pause)
        self.next_button.clicked.connect(self._play_next)
        self.prev_button.clicked.connect(self._play_previous)
        self.skip_forward_button.clicked.connect(self._skip_forward)
        self.skip_backward_button.clicked.connect(self._skip_backward)

    def _play_selected_song(self, item):
        widget = self.virtual_playlist_widget.itemWidget(item)
        if widget and widget.song_info:
            song = widget.song_info
            self.audio_player.load(song['filepath'])
            self.audio_player.play()
            self._update_current_song_info(song)
            self.play_pause_button.setIcon(QIcon("ui/neon_pause.png")) # Assuming you have a neon pause icon
            self.current_playlist = [s['filepath'] for s in self.library_manager.get_all_songs()] # Update current playlist

    def _toggle_play_pause(self):
        if self.audio_player.current_track:
            if self.audio_player.paused:
                self.audio_player.unpause()
                self.play_pause_button.setIcon(QIcon("ui/neon_pause.png"))
            else:
                self.audio_player.pause()
                self.play_pause_button.setIcon(QIcon("ui/neon_play.png"))
        elif self.library_manager.songs:
            first_song = list(self.library_manager.songs.values())[0]
            self.audio_player.load(first_song['filepath'])
            self.audio_player.play()
            self._update_current_song_info(first_song)
            self.play_pause_button.setIcon(QIcon("ui/neon_pause.png"))
            self.current_playlist = [s['filepath'] for s in self.library_manager.get_all_songs()]

    def _play_next(self):
        if self.current_playlist:
            next_track = self.audio_player.next(self.current_playlist)
            if next_track:
                song_info = self.library_manager.songs.get(next_track)
                if song_info:
                    self._update_current_song_info(song_info)
                    self.play_pause_button.setIcon(QIcon("ui/neon_pause.png"))

    def _play_previous(self):
        if self.current_playlist:
            prev_track = self.audio_player.prev(self.current_playlist)
            if prev_track:
                song_info = self.library_manager.songs.get(prev_track)
                if song_info:
                    self._update_current_song_info(song_info)
                    self.play_pause_button.setIcon(QIcon("ui/neon_pause.png"))

    def _skip_forward(self):
        self.audio_player.skip_forward()

    def _skip_backward(self):
        self.audio_player.skip_backward()

    def _update_current_song_info(self, song_info):
        title = song_info.get('title', 'Unknown Title')
        artist = song_info.get('artist', 'Unknown Artist')
        self.current_song_info.setText(f"{title} - {artist}")
        # Load album art here if you have that functionality

    def show_notification(self, message):
        QMessageBox.information(self, "tunes", message)

    def refresh_playlists_view(self):
        if hasattr(self, 'playlists_page'):
            self.playlists_page._populate_playlists()

    def play_virtual_playlist(self, playlist_filepaths):
        if playlist_filepaths:
            self.current_playlist = playlist_filepaths
            first_track = playlist_filepaths[0]
            song_info = self.library_manager.songs.get(first_track)
            if song_info:
                self.audio_player.load(first_track)
                self.audio_player.play()
                self._update_current_song_info(song_info)
                self.play_pause_button.setIcon(QIcon("ui/neon_pause.png"))

    def _apply_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(50, 0, 70)) # Dark Purple
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Button, QColor(50, 0, 70))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(0, 255, 0)) # Neon Green
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        self.side_nav.setStyleSheet(f"background-color: #320046; color: white;") # Removed font-size from here, set programmatically
        buttons = self.side_nav.findChildren(QPushButton)
        for button in buttons:
            button.setStyleSheet("QPushButton { color: white; background-color: #320046; border: none; padding: 12px; text-align: left; }" # Increased padding
                                 "QPushButton:hover { background-color: #460060; }"
                                 "QPushButton:pressed { background-color: #00FF00; color: black; }")
        self.playback_controls_widget.setStyleSheet("background-color: #320046; color: white; padding: 10px;")
        playback_buttons = self.playback_controls_widget.findChildren(QPushButton)
        for button in playback_buttons:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: 1px solid #00FF00; /* Neon Green Border */
                    color: #00FF00; /* Neon Green Text */
                    padding: 5px;
                    border-radius: 3px;
                    min-width: 60px; /* Increased min-width to accommodate text */
                    text-align: center; /* Center the text and icon */
                }}
                QPushButton:hover {{
                    background-color: #460060; /* Darker purple on hover */
                    color: #00CC00; /* Slightly darker neon green on hover */
                    border-color: #00CC00;
                }}
                QPushButton:pressed {{
                    background-color: #00FF00;
                    color: black;
                    border-color: black;
                }}
            """)
        if hasattr(self, 'virtual_playlist_widget'):
            self.virtual_playlist_widget.setStyleSheet("QListWidget { background-color: #1E0028; color: white; border: none; font-size: 12px; }"
                                                       "QListWidget::item:selected { background-color: #460060; }")
        self.content_widget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #320046, stop:1 #000000);") # Gradient