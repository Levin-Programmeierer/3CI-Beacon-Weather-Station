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
    QGraphicsDropShadowEffect,
    QGraphicsBlurEffect,
    QStyle,
    QStyleOptionButton
)
from PySide6.QtCore import (
    QSize,
    Qt,
    QTime,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    Property
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
    QColor,
    QPen,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QIcon
    )
# For image paths
from pathlib import Path

# Other system libaries
import os

# Constants

PROGRAM_VERSION = 0.5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Reusable functions / Icon loading, background loading, styles, etc.

def apply_glass_button_style(button, radius=18):

    button.setStyleSheet(f"""
        QPushButton {{
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1,

                stop: 0 rgba(255, 255, 255, 230),
                stop: 0.25 rgba(220, 248, 255, 195),
                stop: 1 rgba(130, 210, 240, 175)
            );

            border: 1px solid rgba(255, 255, 255, 230);
            border-bottom: 1px solid rgba(75, 155, 190, 110);

            border-radius: {radius}px;
        }}

        QPushButton:hover {{
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1,
                stop: 0 rgba(255, 255, 255, 250),
                stop: 1 rgba(190, 235, 250, 220)
            );

            border: 1px solid white;
        }}

        QPushButton:pressed {{
            background-color: rgba(100, 190, 225, 210);
            border: 1px solid rgba(255, 255, 255, 180);
        }}
    """)

def check_icon_availability(icon):
        BASE_DIR = Path(__file__).resolve().parent
        icon_path = BASE_DIR / "assets" / "icons" / icon
        return icon_path    
#
# Other classes
#

#These classes arereplacement for QFrames, QPushbuttons, etc. automatically adding all styles
# AKA less code Levin happy :D -> Levin faul

class GlassFrame(QFrame):
    def __init__(
        self,
        parent=None,
        radius=20,
        shadow=True,
        hover_effect=False
    ):
        super().__init__(parent)

        self.radius = radius
        self.hover_effect = hover_effect
        self._hovered = False
        self._glow = 0.0

        self.animation = QPropertyAnimation(self, b"glow")
        self.animation.setDuration(180)
        self.animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        # Space between the glass edge and its contents
        self.setContentsMargins(14, 12, 14, 12)

        # Soft blue-tinted shadow
        if shadow:
            shadow_effect = QGraphicsDropShadowEffect(self)
            shadow_effect.setBlurRadius(28)
            shadow_effect.setOffset(0, 6)
            shadow_effect.setColor(QColor(20, 90, 125, 65))
            self.setGraphicsEffect(shadow_effect)

    def getGlow(self):
        return self._glow

    def setGlow(self, value):
        self._glow = value
        self.update()

    glow = Property(float, getGlow, setGlow)

    def enterEvent(self, event):
        if self.hover_effect:
            self.animation.stop()
            self.animation.setStartValue(self._glow)
            self.animation.setEndValue(1.0)
            self.animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.hover_effect:
            self.animation.stop()
            self.animation.setStartValue(self._glow)
            self.animation.setEndValue(0.0)
            self.animation.start()

        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        glow = self._glow

        gradient = QLinearGradient(
            rect.topLeft(),
            rect.bottomLeft()
        )

        # Normal glass colors
        normal_top = QColor(225, 250, 255, 205)
        normal_middle = QColor(125, 205, 225, 175)
        normal_bottom = QColor(55, 150, 190, 160)

        # Hover glass colors
        hover_top = QColor(245, 255, 255, 235)
        hover_middle = QColor(160, 230, 245, 205)
        hover_bottom = QColor(85, 185, 215, 190)

        def blend_color(normal, hover):
            return QColor(*(
                round(a + (b - a) * glow)
                for a, b in zip(normal.getRgb(), hover.getRgb())
            ))

        gradient.setColorAt(
            0.0, blend_color(normal_top, hover_top)
        )
        gradient.setColorAt(
            0.5, blend_color(normal_middle, hover_middle)
        )
        gradient.setColorAt(
            1.0, blend_color(normal_bottom, hover_bottom)
        )

        # Rounded glass shape
        glass_path = QPainterPath()
        glass_path.addRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        # Draw glass background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(glass_path)

        # Outer glass border
        border_pen = QPen(QColor(255, 255, 255, 175))
        border_pen.setWidthF(1.2)

        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(glass_path)

        # Top reflective highlight
        highlight_pen = QPen(QColor(255, 255, 255, 115))
        highlight_pen.setWidthF(2)

        painter.setPen(highlight_pen)
        painter.drawLine(
           rect.left() + self.radius,
           rect.top() + 2,
           rect.right() - self.radius,
           rect.top() + 2
        )

        # Darker bottom edge
        bottom_pen = QPen(QColor(25, 100, 135, 65))
        bottom_pen.setWidthF(1)

        painter.setPen(bottom_pen)
        painter.drawLine(
            rect.left() + self.radius,
            rect.bottom() - 1,
            rect.right() - self.radius,
            rect.bottom() - 1
        )

        painter.end()

class AeroButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self._glow = 0.0
        self._pressed = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(38)

        # Smooth hover animation
        self.animation = QPropertyAnimation(self, b"glow")
        self.animation.setDuration(160)
        self.animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        # Remove default button appearance
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
            }
        """)

    def getGlow(self):
        return self._glow

    def setGlow(self, value):
        self._glow = value
        self.update()

    glow = Property(float, getGlow, setGlow)

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self._glow)
        self.animation.setEndValue(1.0)
        self.animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self._glow)
        self.animation.setEndValue(0.0)
        self.animation.start()

        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.update()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(2, 2, -2, -2)

        # Button gradient
        gradient = QLinearGradient(
            rect.topLeft(),
            rect.bottomLeft()
        )

        if self._pressed:
            gradient.setColorAt(0.0, QColor(35, 125, 165, 230))
            gradient.setColorAt(1.0, QColor(20, 85, 125, 245))
        else:
            gradient.setColorAt(
                0.0,
                QColor(
                    100 + int(70 * self._glow),
                    210 + int(35 * self._glow),
                    235 + int(20 * self._glow),
                    225
                )
            )
            gradient.setColorAt(
                1.0,
                QColor(
                    35 + int(35 * self._glow),
                    145 + int(40 * self._glow),
                    190 + int(30 * self._glow),
                    235
                )
            )

        painter.setPen(QPen(QColor(255, 255, 255, 180), 1))
        painter.setBrush(gradient)
        painter.drawRoundedRect(rect, 12, 12)

        # Reflective top highlight
        if not self._pressed:
            highlight = QLinearGradient(
                rect.topLeft(),
                rect.center()
            )
            highlight.setColorAt(0.0, QColor(255, 255, 255, 95))
            highlight.setColorAt(1.0, QColor(255, 255, 255, 0))

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(highlight)
            painter.drawRoundedRect(
                rect.adjusted(2, 2, -2, -rect.height() // 2),
                10,
                10
            )

        # Draw button text
        painter.end()

        option = QStyleOptionButton()
        self.initStyleOption(option)
        option.rect = self.rect()

        style_painter = QPainter(self)
        self.style().drawControl(
            QStyle.ControlElement.CE_PushButtonLabel,
            option,
            style_painter,
            self
        )

        style_painter.end()

        return

class StatusIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.connected = False
        self.setFixedSize(32, 32)

        self.icon_connected = QIcon(os.path.join(
                    BASE_DIR, "assets", "icons", "Net046.ico"
        ))
        self.icon_disconnected = QIcon(os.path.join(
                    BASE_DIR, "assets", "icons", "Net052.ico"
        ))

        self.setConnected(False)

    def setConnected(self, connected):
        self.connected = connected

        self.icon = (
            self.icon_connected if connected
            else self.icon_disconnected
        )

        print("Icon loaded:", not self.icon.isNull())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.icon.paint(
            painter,
            self.rect(),
            Qt.AlignmentFlag.AlignCenter
        )

#
# WINDOWS
#

# Create app instance
app =  QApplication([])
# Mainwindow
class main_window(QWidget):
    def __init__(self, settings, about):
        super().__init__()
        # Application settings
        self.setWindowTitle("Beacon - Weather Station V0.5")
        self.resize(800, 500)
        self.setWindowOpacity(1.00)

        self.settingswindow = settings
        self.aboutwindow = about

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

        self.status_bar = GlassFrame(radius=22, shadow=True)
        self.status_bar.setFixedSize(620, 100)

        self.status_bar_layout = QHBoxLayout(self.status_bar)

        self.connected_label = StatusIndicator()

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

        self.sidebar = GlassFrame(radius=18, shadow=True, hover_effect=True)
        self.sidebar.setFixedSize(100, 450)

        self.sidebarlayout = QVBoxLayout(self.sidebar) # <- Fir dass buttons erankommen

        # Buttons

        # ESP32 Connection Settings Button

        self.connection_button = AeroButton()

        # Icon available check
        icon_path = self.check_icon_availability("Net028.ico")

        self.connection_button.setIcon(QIcon(str(icon_path)))
        self.connection_button.setIconSize(QSize(48, 48))
        self.connection_button.setFixedSize(60, 60)

        apply_glass_button_style(self.connection_button)

        self.sidebarlayout.addWidget(self.connection_button, alignment=Qt.AlignCenter)

        # Settings Button

        self.settings_button = AeroButton()
        icon_path = self.check_icon_availability("Settings.png")

        self.settings_button.setIcon(QIcon(str(icon_path)))
        self.settings_button.setIconSize(QSize(48, 48))
        self.settings_button.setFixedSize(60, 60)

        apply_glass_button_style(self.settings_button)
        
        self.sidebarlayout.addWidget(self.settings_button, alignment=Qt.AlignCenter)

        # About button

        self.about_button = AeroButton()
        icon_path = self.check_icon_availability("Alert002.ico")

        self.about_button.setIcon(QIcon(str(icon_path)))
        self.about_button.setIconSize(QSize(48, 48))
        self.about_button.setFixedSize(60, 60)

        apply_glass_button_style(self.about_button)

        self.sidebarlayout.addWidget(self.about_button, alignment=Qt.AlignCenter)

        self.settings_button.clicked.connect(self.settingswindow.show)
        self.about_button.clicked.connect(self.aboutwindow.show)

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

class settings_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(600, 400)
        self.load_fonts()

        self.create_background()
        self.create_settings_buttons()

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.main_layout.addLayout(self.settings_layout)
        self.setLayout(self.main_layout)


    def create_background(self):
        BASE_DIR = Path(__file__).resolve().parent
        image_path = BASE_DIR / "assets" / "backgrounds" / "b2.jpg"

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)

        self.background.lower()
        self.background.setGeometry(0, 0, 600, 400)

        if self.background_image.isNull():
            print(f"ERROR: Could not load background: {image_path}")

    def create_settings_buttons(self):
        self.top_layout = QHBoxLayout()
        self.settings_layout = QVBoxLayout()

        icon_path = self.check_icon_availability("Sign026.ico")

        self.exit_button = AeroButton()
        self.exit_button.setIcon(QIcon(str(icon_path)))
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setIconSize(QSize(30, 30))
        self.settings_label = QLabel()
        self.settings_label.setFont(QFont(self.custom_font, 30))
        self.settings_label.setStyleSheet("color: #000000;")
        self.settings_label.setText("Settings")

        apply_glass_button_style(self.exit_button)

        self.exit_button.clicked.connect(self.hide)

        self.top_layout.addWidget(self.exit_button, alignment=Qt.AlignLeft)
        self.top_layout.addWidget(self.settings_label)
        self.top_layout.addStretch()    
        self.settings_layout.addLayout(self.top_layout)

        self.settings_frame = GlassFrame(radius=20, shadow=True)
        self.settings_frame.setFixedSize(500, 250)

        self.settings_layout.addWidget(self.settings_frame, alignment=Qt.AlignRight)

    def check_icon_availability(self, icon):
        BASE_DIR = Path(__file__).resolve().parent
        icon_path = BASE_DIR / "assets" / "icons" / icon
        return icon_path

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

class about_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(600, 400)
        self.load_fonts()
        self.create_background()
        self.create_about_page()
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.about_layout)
        self.setLayout(self.main_layout)

    def create_background(self):
        BASE_DIR = Path(__file__).resolve().parent
        image_path = BASE_DIR / "assets" / "backgrounds" / "b3.jpg"

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)

        self.background.lower()
        self.background.setGeometry(0, 0, 600, 400)

    def create_about_page(self):
        self.top_layout = QHBoxLayout()
        self.about_layout = QVBoxLayout()
        
        icon_path = self.check_icon_availability("Sign026.ico")
        
        self.exit_button = AeroButton()
        self.exit_button.setIcon(QIcon(str(icon_path)))
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setIconSize(QSize(30, 30))
        apply_glass_button_style(self.exit_button)

        self.about_title = QLabel()
        self.about_title.setText("About this program")
        self.about_title.setFont(QFont(self.custom_font, 25))
        self.about_title.setStyleSheet("color: #000000")

        self.about_img = QLabel()
        self.about_img.setPixmap(QPixmap((self.check_icon_availability("Alert002.ico"))))
        self.about_img.setScaledContents(True)
        self.about_img.setFixedSize(25, 25)

        self.top_layout.addWidget(self.exit_button)
        self.top_layout.addWidget(self.about_title)
        self.top_layout.addWidget(self.about_img)
        self.top_layout.addStretch()  

        self.about_layout.addLayout(self.top_layout)
        self.about_layout.addStretch()

        self.about_frame = GlassFrame(radius=20, shadow=True)
        self.about_frame.setFixedSize(550, 250)

        self.about_layout.addWidget(self.about_frame, Qt.AlignRight)

        self.about_frame_layout = QVBoxLayout(self.about_frame)

        self.program_version_label = QLabel()
        self.program_version_label.setText(f"Program version: {PROGRAM_VERSION}")
        self.program_version_label.setFont(QFont(self.custom_font, 15))
        self.program_version_label.setStyleSheet("color: #000000; border-radius: 5px; background-color: rgba(128, 231, 105, 0.8)")
        self.program_version_label.setFixedSize(190, 25)

        self.creators_label = QLabel()
        self.creators_label.setText("Created by: Levin Boehler & Dany Da Silva Marques")
        self.creators_label.setFont(QFont(self.custom_font, 15))
        self.creators_label.setStyleSheet("color: #000000; border-radius: 5px; background-color: rgba(128, 231, 105, 0.8)")
        self.creators_label.setFixedSize(460, 25)

        self.about_frame_layout.addWidget(self.program_version_label, Qt.AlignLeft)
        self.about_frame_layout.addWidget(self.creators_label, Qt.AlignLeft)

        self.exit_button.clicked.connect(self.hide)

    def check_icon_availability(self, icon):
        BASE_DIR = Path(__file__).resolve().parent
        icon_path = BASE_DIR / "assets" / "icons" / icon
        return icon_path

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
    
s_window = settings_window()
abt_window = about_window()
m_window = main_window(s_window, abt_window)


if __name__ == "__main__":
    sys.exit(app.exec())