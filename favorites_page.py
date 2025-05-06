from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class FavoritesPage(QWidget):
    def __init__(self, favorites_manager, library_manager, audio_player, main_window, parent=None):
        super().__init__(parent)
        self.favorites_manager = favorites_manager
        self.library_manager = library_manager
        self.audio_player = audio_player
        self.main_window = main_window

        self.layout = QVBoxLayout(self)

        # Title Label
        self.title_label = QLabel("Favorites")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Favorites List Widget
        self.favorites_list_widget = QListWidget()
        self.layout.addWidget(self.favorites_list_widget)

        # Buttons
        self.refresh_button = QPushButton("Refresh")
        self.clear_button = QPushButton("Clear Favorites")
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.clear_button)

        self._apply_button_style()

        # Populate the favorites list on page load
        self._populate_favorites()

    def _apply_button_style(self):
        """
        Apply consistent styling to action buttons.
        """
        button_style = """
        QPushButton {
            background-color: #320046;
            color: white;
            border: 1px solid #00FF00;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #460060;
        }
        QPushButton:pressed {
            background-color: #00FF00;
            color: black;
        }
        """
        self.refresh_button.setStyleSheet(button_style)
        self.clear_button.setStyleSheet(button_style)

    def _populate_favorites(self):
        """
        Populate favorites list widget with data.
        """
        self.favorites_list_widget.clear()
        # Use the correct method name from the FavoritesManager
        favorites = self.favorites_manager.get_favorites()
        for favorite in favorites:
            self.favorites_list_widget.addItem(favorite)

    def apply_theme(self):
        """
        Apply consistent theming to the FavoritesPage.
        """
        # Set the main background color
        self.setStyleSheet("background-color: #28003C; color: white;")

        # Style title label
        self.title_label.setStyleSheet("color: white;")

        # Style favorites list widget
        self.favorites_list_widget.setStyleSheet(
            """
            QListWidget {
                background-color: #320046;
                color: white;
                border: none;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #460060;
            }
            QListWidget::item:hover {
                background-color: #28003C;
            }
            """
        )

        # Restyle buttons using the helper function
        self._apply_button_style()
