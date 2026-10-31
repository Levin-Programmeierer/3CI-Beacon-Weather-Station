# Written by Levin Boehler, started on 29.09.2026 at 18:36
# Recoded in PySide6 by Levin at 31.10.2026 at 10:51

#
# Imports
#

# Graphical User Interface Library
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import (
    QSize,
    Qt,
    QTime,
    QTimer
)
# System libraries
import sys
# For image loading
# Vum Grafik Design Kuer
# -> Icons fir buttons an esou
# -> PNG fir backgrounds
from PySide6.QtGui import (
    QPixmap, 
    QIcon,
    QFontDatabase,
    QFont,
    QColor
    )
# For image paths
from pathlib import Path

# Create app instance
app =  QApplication([])
# Mainwindow
class main_window(QWidget):
    def __init__(self):
        super().__init__()
        # Application settings
        self.setWindowTitle("Beacon - Weather Station V0.5")
        self.resize(800, 500)
        self.setWindowOpacity(0.95)

        # Load fonts
        self.load_fonts()
        self.create_background()

        # Main Window Layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Widget creation etc.
        self.create_sidebar()
        self.create_dashboard()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addLayout(self.dashboard_layout)

        # After setup
        self.show()

    def create_dashboard(self):
        self.dashboard_layout = QVBoxLayout()
        self.dashboard_top = QHBoxLayout()

        self.title = QLabel()
        self.title.setText("Beacon - Weather Station")
        self.title.setFont(QFont(self.custom_font, 30))
        self.title.setStyleSheet("color: #000000;")

        icon_path = self.check_icon_availability("LM004.ico")

        self.titleimg = QLabel()
        self.titleimg.setPixmap(QPixmap(str(icon_path)))
        self.titleimg.setFixedSize(60,60)

        self.dashboard_top.addWidget(self.title)
        self.dashboard_top.addWidget(self.titleimg)
        self.dashboard_top.addStretch()    

        self.status_bar = QFrame()
        self.status_bar.setFixedSize(620, 100)
        self.status_bar.setStyleSheet("""
                    QFrame {
                        background-color: rgba(184, 234, 247, 180);
                        border: 1px solid white;
                        border-radius: 20px;
                    }            
                """)

        self.status_bar_layout = QHBoxLayout(self.status_bar)

        self.connected_label = QLabel()
        connected = True

        if connected:
            icon_path = self.check_icon_availability("Net046.ico")
        else:
            icon_path = self.check_icon_availability("Net052.ico")

        self.connected_label.setPixmap(QPixmap(str(icon_path)))
        self.connected_label.setFixedSize(60,60)
        self.connected_label.setStyleSheet("""
            QLabel {
                background-color: rgba(210, 245, 255, 100);
                border: 1px solid rgba(255, 255, 255, 190);
                border-radius: 20px;
            }""")

        self.status_bar_layout.addWidget(self.connected_label, alignment=Qt.AlignLeft)

        self.time_label = QLabel()
        self.time_label.setFont(QFont(self.custom_font, 20))
        self.time_label.setStyleSheet("color: #000000;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # For updating the time

        self.update_time()

        self.status_bar_layout.addWidget(self.time_label, alignment=Qt.AlignRight)

        self.dashboard_layout.addLayout(self.dashboard_top)
        self.dashboard_layout.addStretch()
        self.dashboard_layout.addWidget(self.status_bar, alignment=Qt.AlignRight)

    def create_sidebar(self):

        self.sidebar = QFrame()
        self.sidebar.setFixedSize(100, 450)

        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: rgba(184, 234, 247, 180);
                border: 1px solid white;
                border-radius: 20px;
            }            
        """)
        
        self.sidebarlayout = QVBoxLayout(self.sidebar) # <- Fir dass buttons erankommen

        # Buttons

        # ESP32 Connection Settings Button

        self.connection_button = QPushButton()

        # Icon available check
        icon_path = self.check_icon_availability("Net028.ico")

        self.connection_button.setIcon(QIcon(str(icon_path)))
        self.connection_button.setIconSize(QSize(48, 48))
        self.connection_button.setFixedSize(60, 60)

        self.connection_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(210, 245, 255, 100);
                border: 1px solid rgba(255, 255, 255, 190);
                border-radius: 20px;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 200);
            }
        """)

        shadow = QGraphicsDropShadowEffect(self.sidebar)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 100, 150, 70))

        self.sidebar.setGraphicsEffect(shadow)

        self.sidebarlayout.addWidget(self.connection_button, alignment=Qt.AlignCenter)

        # Settings Button

        self.settings_button = QPushButton()
        icon_path = self.check_icon_availability("Settings.png")

        self.settings_button.setIcon(QIcon(str(icon_path)))
        self.settings_button.setIconSize(QSize(48, 48))
        self.settings_button.setFixedSize(60, 60)

        self.settings_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(184, 234, 247, 180);
                    border: 1px solid white;
                    border-radius: 20px;
                }
        
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 200);
                }
            """)
        
        self.sidebarlayout.addWidget(self.settings_button, alignment=Qt.AlignCenter)

        # About button

        self.about_button = QPushButton()
        icon_path = self.check_icon_availability("Alert002.ico")

        self.about_button.setIcon(QIcon(str(icon_path)))
        self.about_button.setIconSize(QSize(48, 48))
        self.about_button.setFixedSize(60, 60)

        self.about_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(184, 234, 247, 180);
                    border: 1px solid white;
                    border-radius: 20px;
                }
                
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 200);
                }
        """)

        self.sidebarlayout.addWidget(self.about_button, alignment=Qt.AlignCenter)

    def check_icon_availability(self, icon):
        BASE_DIR = Path(__file__).resolve().parent
        icon_path = BASE_DIR / "assets" / "icons" / icon
        return icon_path     

    def create_background(self):


        BASE_DIR = Path(__file__).resolve().parent
        image_path = BASE_DIR / "assets" / "backgrounds" / "b1.jpg"

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)

        self.background.lower()
        self.background.setGeometry(0, 0, 800, 500)

    def load_fonts(self):

        BASE_DIR = Path(__file__).resolve().parent
        font_path = BASE_DIR / "assets" / "fonts" / "FrutigerAero.ttf"

        font_id = QFontDatabase.addApplicationFont(str(font_path))

        if font_id == -1:
            print("Font loading failed")
            self.custom_font = "Segoe UI"
            return

        font_families = QFontDatabase.applicationFontFamilies(font_id)

        self.custom_font = font_families[0]

        print("Loaded font:", self.custom_font)

    def load_settings(self):
        pass

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)
m_window = main_window()

if __name__ == "__main__":
    sys.exit(app.exec())