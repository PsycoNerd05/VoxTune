import sys

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication

from core import library_manager, playlist_manager, audio_player, favorites_manager
from ui.mainwindow import MainWindow


class Theme:
    @staticmethod
    def darkPurpleNeon():
        palette = QPalette()

        # Window
        palette.setColor(QPalette.Window, QColor(50, 0, 70))  # Dark Purple
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # White

        # Base and Alternate (for lists, etc.)
        palette.setColor(QPalette.Base, QColor(30, 0, 40))
        palette.setColor(QPalette.AlternateBase, QColor(40, 0, 55))

        # Text
        palette.setColor(QPalette.Text, QColor(255, 255, 255))

        # Buttons (base colors, stylesheets will override for neon)
        palette.setColor(QPalette.Button, QColor(50, 0, 70))
        palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))  # Default to neon text

        # Highlight
        palette.setColor(QPalette.Highlight, QColor(0, 255, 0))  # Neon Green
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))  # Black

        # Disabled
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 128, 128))

        return palette

    @staticmethod
    def gradientDarkPurpleNeon():
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #320046, stop:1 #1E0028); /* Dark Purple Gradient */
                color: white;
            }
            QWidget {
                background: transparent; /* Make other widgets transparent to see the main window's gradient */
                color: white;
            }
            QListView {
                background-color: #28003C;
                color: white;
                border: none;
            }
            QListView::item:selected {
                background-color: #460060;
            }
            QPushButton {
                background-color: #320046;
                color: #00FF00; /* Neon Green Text */
                border: 1px solid #00FF00; /* Neon Green Border */
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #460060;
            }
            QPushButton:pressed {
                background-color: #00FF00;
                color: black;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #28003C;
                color: white;
                border: 1px solid #460060;
                padding: 3px;
                border-radius: 2px;
            }
            QScrollBar:vertical {
                border: none;
                background: #28003C;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #460060;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """

    @staticmethod
    def applyTheme(widget, theme_name="darkPurpleNeon"):
        if theme_name == "darkPurpleNeon":
            widget.setPalette(Theme.darkPurpleNeon())
        elif theme_name == "gradientDarkPurpleNeon":
            widget.setStyleSheet(Theme.gradientDarkPurpleNeon())
        # Add other themes here as elif conditions
        elif theme_name == "anotherTheme":
            palette = QPalette()
            # Define colors for another theme
            palette.setColor(...)
            widget.setPalette(palette)
            widget.setStyleSheet(...) # If needed for stylesheet-based themes

# Example of applying the gradient theme in main_window.py:
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ... (rest of your initialization)
    main_window = MainWindow(library_manager, playlist_manager, audio_player, favorites_manager)
    Theme.applyTheme(main_window, "gradientDarkPurpleNeon") # Apply the gradient theme
    main_window.show()
    sys.exit(app.exec_())
