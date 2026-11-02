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
    Property,
    QRectF
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

PROGRAM_VERSION = 0.6
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

def load_fonts():
    fonts_dir = os.path.join(BASE_DIR, "assets", "fonts")

    regular_id = QFontDatabase.addApplicationFont(
        os.path.join(fonts_dir, "FrutigerAero.ttf")
    )

    bold_id = QFontDatabase.addApplicationFont(
        os.path.join(fonts_dir, "Frutiger_bold.ttf")
    )

    regular_font = (
        QFontDatabase.applicationFontFamilies(regular_id)[0]
        if regular_id != -1 else QFont().defaultFamily()
    )

    bold_font = (
        QFontDatabase.applicationFontFamilies(bold_id)[0]
        if bold_id != -1 else regular_font
    )

    return regular_font, bold_font

#
# Other classes
#

#These classes arereplacement for QFrames, QPushbuttons, etc. automatically adding all styles
# AKA less code Levin happy :D -> Levin faul



class GlassFrame(QFrame):
    def __init__(
        self,
        parent=None,
        radius=16,
        shadow=True,
        hover_effect=True,
        theme="blue"
    ):
        super().__init__(parent)

        self.radius = radius
        self.hover_enabled = hover_effect
        self._glow = 0.0

        # Theme selection
        self.theme = theme.lower()

        if self.theme not in ("blue", "green"):
            self.theme = "blue"

        # Theme colors
        if self.theme == "green":
            self.shadow_color = QColor(30, 160, 90, 90)
            self.glow_color = QColor(120, 255, 165)

            self.glass_colors = [
                QColor(235, 255, 240, 135),
                QColor(160, 235, 185, 100),
                QColor(90, 200, 135, 95),
                QColor(35, 145, 95, 120)
            ]

            self.bottom_color = QColor(0, 120, 65, 50)

        else:
            self.shadow_color = QColor(25, 130, 190, 85)
            self.glow_color = QColor(100, 220, 255)

            self.glass_colors = [
                QColor(220, 250, 255, 125),
                QColor(135, 215, 245, 85),
                QColor(75, 175, 220, 80),
                QColor(30, 130, 195, 115)
            ]

            self.bottom_color = QColor(0, 100, 170, 45)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFrameShape(QFrame.Shape.NoFrame)

        self.setContentsMargins(14, 12, 14, 12)

        # Glass shadow
        if shadow:
            self.shadow_effect = QGraphicsDropShadowEffect(self)

            self.shadow_effect.setBlurRadius(22)
            self.shadow_effect.setOffset(0, 4)
            self.shadow_effect.setColor(self.shadow_color)

            self.setGraphicsEffect(self.shadow_effect)

        # Hover glow animation
        self.glow_animation = QPropertyAnimation(
            self, b"glow", self
        )

        self.glow_animation.setDuration(180)

        self.glow_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

    # Animated glow property
    def getGlow(self):
        return self._glow

    def setGlow(self, value):
        self._glow = value
        self.update()

    glow = Property(float, getGlow, setGlow)

    # Hover effects
    def enterEvent(self, event):
        if self.hover_enabled:
            self.glow_animation.stop()

            self.glow_animation.setStartValue(self._glow)
            self.glow_animation.setEndValue(1.0)

            self.glow_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.hover_enabled:
            self.glow_animation.stop()

            self.glow_animation.setStartValue(self._glow)
            self.glow_animation.setEndValue(0.0)

            self.glow_animation.start()

        super().leaveEvent(event)

    # Glass painting
    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform
        )

        rect = QRectF(self.rect()).adjusted(
            1, 1, -1, -1
        )

        # Main rounded glass shape
        path = QPainterPath()

        path.addRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        # Main glass gradient
        glass = QLinearGradient(
            rect.topLeft(),
            rect.bottomLeft()
        )

        glass.setColorAt(0.0, self.glass_colors[0])
        glass.setColorAt(0.30, self.glass_colors[1])
        glass.setColorAt(0.65, self.glass_colors[2])
        glass.setColorAt(1.0, self.glass_colors[3])

        painter.fillPath(path, glass)

        # Top reflective shine
        reflection = QLinearGradient(
            rect.topLeft(),
            rect.topLeft() + rect.bottomLeft() * 0.48
        )

        reflection.setColorAt(
            0.0, QColor(255, 255, 255, 115)
        )

        reflection.setColorAt(
            0.45, QColor(255, 255, 255, 35)
        )

        reflection.setColorAt(
            1.0, QColor(255, 255, 255, 0)
        )

        painter.fillPath(path, reflection)

        # Bottom glass depth
        bottom = QLinearGradient(
            rect.center().x(),
            rect.center().y(),
            rect.center().x(),
            rect.bottom()
        )

        bottom.setColorAt(
            0.0, QColor(0, 0, 0, 0)
        )

        bottom.setColorAt(
            1.0, self.bottom_color
        )

        painter.fillPath(path, bottom)

        # Outer reflective border
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.setPen(
            QPen(
                QColor(230, 252, 255, 190),
                1.4
            )
        )

        painter.drawPath(path)

        # Inner glass border
        inner_rect = rect.adjusted(
            2, 2, -2, -2
        )

        inner_path = QPainterPath()

        inner_path.addRoundedRect(
            inner_rect,
            max(1, self.radius - 2),
            max(1, self.radius - 2)
        )

        painter.setPen(
            QPen(
                QColor(255, 255, 255, 75),
                1
            )
        )

        painter.drawPath(inner_path)

        # Animated theme-colored hover glow
        if self._glow > 0:
            glow_color = QColor(self.glow_color)

            glow_color.setAlpha(
                int(110 * self._glow)
            )

            painter.setPen(
                QPen(glow_color, 2.5)
            )

            painter.drawPath(path)

            # Subtle inner hover highlight
            painter.setPen(
                QPen(
                    QColor(
                        255, 255, 255,
                        int(65 * self._glow)
                    ),
                    1.5
                )
            )

            painter.drawPath(inner_path)

        painter.end()

class AeroButton(QPushButton):
    def __init__(
        self,
        text="",
        parent=None,
        radius=10,
        shadow=True,
        hover=True,
        hover_effect=None
    ):
        super().__init__(text, parent)

        if hover_effect is not None:
            hover = hover_effect

        self.radius = radius
        self.hover_enabled = hover
        self._glow = 0.0

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

        self.setMinimumHeight(34)

        # Smooth hover animation
        self.glow_animation = QPropertyAnimation(
            self, b"glow", self
        )
        self.glow_animation.setDuration(200)
        self.glow_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        # Soft blue shadow
        if shadow:
            self.shadow_effect = QGraphicsDropShadowEffect(self)
            self.shadow_effect.setBlurRadius(15)
            self.shadow_effect.setOffset(0, 3)
            self.shadow_effect.setColor(
                QColor(25, 125, 190, 90)
            )
            self.setGraphicsEffect(self.shadow_effect)

    # Animated glow property
    def getGlow(self):
        return self._glow

    def setGlow(self, value):
        self._glow = value
        self.update()

    glow = Property(float, getGlow, setGlow)

    # Hover animation
    def enterEvent(self, event):
        if self.hover_enabled and self.isEnabled():
            self.glow_animation.stop()
            self.glow_animation.setStartValue(self._glow)
            self.glow_animation.setEndValue(1.0)
            self.glow_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.hover_enabled:
            self.glow_animation.stop()
            self.glow_animation.setStartValue(self._glow)
            self.glow_animation.setEndValue(0.0)
            self.glow_animation.start()

        super().leaveEvent(event)

    # Custom Aero painting
    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform
        )

        rect = QRectF(self.rect()).adjusted(
            1, 1, -1, -1
        )

        path = QPainterPath()
        path.addRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        # Button state
        pressed = self.isDown()
        enabled = self.isEnabled()
        checked = self.isCheckable() and self.isChecked()

        # Main glass gradient
        gradient = QLinearGradient(
            rect.topLeft(),
            rect.bottomLeft()
        )

        if not enabled:
            gradient.setColorAt(
                0.0, QColor(185, 205, 215, 130)
            )
            gradient.setColorAt(
                1.0, QColor(115, 150, 170, 110)
            )

        elif pressed or checked:
            gradient.setColorAt(
                0.0, QColor(45, 145, 195, 220)
            )
            gradient.setColorAt(
                0.5, QColor(35, 125, 185, 225)
            )
            gradient.setColorAt(
                1.0, QColor(20, 95, 155, 235)
            )

        else:
            gradient.setColorAt(
                0.0, QColor(235, 252, 255, 220)
            )
            gradient.setColorAt(
                0.35, QColor(145, 220, 250, 190)
            )
            gradient.setColorAt(
                0.7, QColor(80, 180, 225, 185)
            )
            gradient.setColorAt(
                1.0, QColor(40, 135, 195, 210)
            )

        painter.fillPath(path, gradient)

        # Top glossy reflection
        if not pressed:
            reflection = QLinearGradient(
                rect.topLeft(),
                rect.topLeft() + rect.bottomLeft() * 0.55
            )

            reflection.setColorAt(
                0.0, QColor(255, 255, 255, 145)
            )
            reflection.setColorAt(
                0.45, QColor(255, 255, 255, 45)
            )
            reflection.setColorAt(
                1.0, QColor(255, 255, 255, 0)
            )

            painter.fillPath(path, reflection)

        # Outer glass border
        painter.setBrush(Qt.BrushStyle.NoBrush)

        border_color = (
            QColor(255, 255, 255, 115)
            if not enabled
            else QColor(235, 252, 255, 220)
        )

        painter.setPen(
            QPen(border_color, 1.2)
        )

        painter.drawPath(path)

        # Inner border
        inner_rect = rect.adjusted(2, 2, -2, -2)

        inner_path = QPainterPath()
        inner_path.addRoundedRect(
            inner_rect,
            max(1, self.radius - 2),
            max(1, self.radius - 2)
        )

        painter.setPen(
            QPen(
                QColor(255, 255, 255, 85),
                1
            )
        )

        painter.drawPath(inner_path)

        # Animated hover glow
        if self._glow > 0 and enabled:
            glow_color = QColor(
                100,
                225,
                255,
                int(150 * self._glow)
            )

            painter.setPen(
                QPen(glow_color, 2.2)
            )

            painter.drawPath(path)

        # Preserve native button text and icons
        option = QStyleOptionButton()
        self.initStyleOption(option)

        painter.setPen(Qt.PenStyle.NoPen)

        self.style().drawControl(
            QStyle.ControlElement.CE_PushButtonLabel,
            option,
            painter,
            self
        )

        painter.end()

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
    def __init__(self, settings, about, connection, custom_font, custom_font_bold):
        super().__init__()
        # Application settings
        self.setWindowTitle("Beacon - Weather Station V0.5")
        self.resize(800, 500)
        self.setWindowOpacity(1.00)
        self.custom_font = custom_font
        self.custom_font_bold = custom_font_bold

        self.settingswindow = settings
        self.aboutwindow = about
        self.connectionwindow = connection

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

        glow = QGraphicsDropShadowEffect(self.title)
        glow.setBlurRadius(22)
        glow.setColor(QColor(80, 190, 255, 170))
        glow.setOffset(0, 0)

        self.title.setGraphicsEffect(glow)

        icon_path = check_icon_availability("LM004.ico")

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
        self.time_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background: transparent;
                padding: 6px;
            }
        """)

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
        icon_path = check_icon_availability("Net028.ico")

        self.connection_button.setIcon(QIcon(str(icon_path)))
        self.connection_button.setIconSize(QSize(48, 48))
        self.connection_button.setFixedSize(60, 60)

        apply_glass_button_style(self.connection_button)

        self.sidebarlayout.addWidget(self.connection_button, alignment=Qt.AlignCenter)

        # Settings Button

        self.settings_button = AeroButton()
        icon_path = check_icon_availability("Settings.png")

        self.settings_button.setIcon(QIcon(str(icon_path)))
        self.settings_button.setIconSize(QSize(48, 48))
        self.settings_button.setFixedSize(60, 60)

        apply_glass_button_style(self.settings_button)
        
        self.sidebarlayout.addWidget(self.settings_button, alignment=Qt.AlignCenter)

        # About button

        self.about_button = AeroButton()
        icon_path = check_icon_availability("Alert002.ico")

        self.about_button.setIcon(QIcon(str(icon_path)))
        self.about_button.setIconSize(QSize(48, 48))
        self.about_button.setFixedSize(60, 60)

        apply_glass_button_style(self.about_button)

        self.sidebarlayout.addWidget(self.about_button, alignment=Qt.AlignCenter)

        self.settings_button.clicked.connect(self.settingswindow.show)
        self.about_button.clicked.connect(self.aboutwindow.show)
        self.connection_button.clicked.connect(self.connectionwindow.show)   

    def create_background(self):


        BASE_DIR = Path(__file__).resolve().parent
        image_path = BASE_DIR / "assets" / "backgrounds" / "b1.jpg"

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)

        self.background.lower()
        self.background.setGeometry(0, 0, 800, 500)

    def load_settings(self):
        pass

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)

class settings_window(QWidget):
    def __init__(self, custom_font, custom_font_bold):
        super().__init__()

        self.setWindowTitle("Beacon - Settings")
        self.setFixedSize(600, 400)

        self.custom_font = custom_font
        self.custom_font_bold = custom_font_bold

        self.create_background()

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.create_settings_page()

    def create_background(self):
        image_path = (
            Path(BASE_DIR) / "assets" / "backgrounds" / "b2.jpg"
        )

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.lower()

        if self.background_image.isNull():
            print(f"ERROR: Could not load background: {image_path}")

    def create_settings_page(self):

        # Main vertical layout
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setSpacing(15)

        # -------------------------
        # HEADER
        # -------------------------

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(12)

        # Exit button
        icon_path = check_icon_availability("Sign026.ico")

        self.exit_button = AeroButton(
            radius=10,
            shadow=True,
            hover=True
        )

        self.exit_button.setIcon(QIcon(str(icon_path)))
        self.exit_button.setIconSize(QSize(26, 26))
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setToolTip("Close settings")
        self.exit_button.clicked.connect(self.hide)

        # Header title
        self.settings_label = QLabel("Settings")
        self.settings_label.setFont(
            QFont(self.custom_font, 27)
        )

        self.settings_label.setStyleSheet("""
            QLabel {
                color: #164D35;
                background: transparent;
            }
        """)

        self.top_layout.addWidget(
            self.exit_button,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.top_layout.addWidget(self.settings_label)

        self.top_layout.addStretch()

        self.settings_layout.addLayout(self.top_layout)

        # -------------------------
        # SETTINGS GLASS FRAME
        # -------------------------

        self.settings_frame = GlassFrame(
            radius=20,
            shadow=True,
            hover_effect=True,
            theme="green"
        )

        self.settings_frame.setFixedSize(540, 275)

        self.settings_frame_layout = QVBoxLayout(
            self.settings_frame
        )

        self.settings_frame_layout.setContentsMargins(
            20, 18, 20, 18
        )

        self.settings_frame_layout.setSpacing(12)

        # Section heading
        self.preferences_title = QLabel("Application preferences")

        self.preferences_title.setFont(
            QFont(self.custom_font, 17)
        )

        self.preferences_title.setStyleSheet("""
            QLabel {
                color: #17623C;
                background: transparent;
            }
        """)

        self.settings_frame_layout.addWidget(
            self.preferences_title
        )

        # Placeholder for future settings
        self.preferences_description = QLabel(
            "Beacon settings and preferences will appear here."
        )

        self.preferences_description.setFont(
            QFont(self.custom_font, 11)
        )

        self.preferences_description.setWordWrap(True)

        self.preferences_description.setStyleSheet("""
            QLabel {
                color: #286C49;
                background: transparent;
            }
        """)

        self.settings_frame_layout.addWidget(
            self.preferences_description
        )

        self.settings_frame_layout.addStretch()

        self.settings_layout.addWidget(
            self.settings_frame,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.main_layout.addLayout(self.settings_layout)

class about_window(QWidget):
    def __init__(self, custom_font, custom_font_bold):
        super().__init__()

        self.setWindowTitle("Beacon - About")
        self.setFixedSize(600, 400)

        self.custom_font = custom_font
        self.custom_font_bold = custom_font_bold

        self.create_background()

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.create_about_page()

    def create_background(self):
        image_path = (
            Path(BASE_DIR) / "assets" / "backgrounds" / "b3.jpg"
        )

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.lower()

        if self.background_image.isNull():
            print(f"ERROR: Could not load background: {image_path}")

    def create_about_page(self):

        # Main vertical layout
        self.about_layout = QVBoxLayout()
        self.about_layout.setSpacing(15)

        # -------------------------
        # HEADER
        # -------------------------

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(12)

        # Exit button
        icon_path = check_icon_availability("Sign026.ico")

        self.exit_button = AeroButton(
            radius=10,
            shadow=True,
            hover=True
        )

        self.exit_button.setIcon(QIcon(str(icon_path)))
        self.exit_button.setIconSize(QSize(26, 26))
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setToolTip("Close About")
        self.exit_button.clicked.connect(self.hide)

        # About title
        self.about_title = QLabel("About this program")

        self.about_title.setFont(
            QFont(CUSTOM_FONT2, 25)
        )

        self.about_title.setStyleSheet("""
            QLabel {
                color: #164D35;
                background: transparent;
            }
        """)

        # About icon
        icon_path = check_icon_availability("Alert002.ico")

        self.about_img = QLabel()

        self.about_img.setPixmap(
            QPixmap(str(icon_path))
        )

        self.about_img.setScaledContents(True)
        self.about_img.setFixedSize(30, 30)

        self.top_layout.addWidget(
            self.exit_button,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.top_layout.addWidget(self.about_title)

        self.top_layout.addWidget(
            self.about_img,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.top_layout.addStretch()

        self.about_layout.addLayout(self.top_layout)

        # -------------------------
        # ABOUT GLASS FRAME
        # -------------------------

        self.about_frame = GlassFrame(
            radius=20,
            shadow=True,
            hover_effect=True,
            theme="green"
        )

        self.about_frame.setFixedSize(550, 250)

        self.about_frame_layout = QVBoxLayout(
            self.about_frame
        )

        self.about_frame_layout.setContentsMargins(
            22, 20, 22, 20
        )

        self.about_frame_layout.setSpacing(15)

        # Beacon application name
        self.program_name_label = QLabel(
            "Beacon - Weather Station"
        )

        self.program_name_label.setFont(
            QFont(self.custom_font, 20)
        )

        self.program_name_label.setStyleSheet("""
            QLabel {
                color: #155C38;
                background: transparent;
            }
        """)

        self.about_frame_layout.addWidget(
            self.program_name_label
        )

        # Green information label style
        info_style = """
            QLabel {
                color: #164D35;
                border: 1px solid rgba(255, 255, 255, 210);
                border-radius: 8px;
                padding: 5px 9px;
                background-color: rgba(190, 255, 210, 155);
            }
        """

        # Program version
        self.program_version_label = QLabel(
            f"Program version: {PROGRAM_VERSION}"
        )

        self.program_version_label.setFont(
            QFont(self.custom_font, 12)
        )

        self.program_version_label.setStyleSheet(
            info_style
        )

        self.program_version_label.setFixedHeight(34)

        # Creator information
        self.creators_label = QLabel(
            "Created by: Levin Boehler & Dany Da Silva Marques"
        )

        self.creators_label.setFont(
            QFont(self.custom_font, 12)
        )

        self.creators_label.setStyleSheet(
            info_style
        )

        self.creators_label.setFixedHeight(34)

        # Add information
        self.about_frame_layout.addWidget(
            self.program_version_label
        )

        self.about_frame_layout.addWidget(
            self.creators_label
        )

        self.about_frame_layout.addStretch()

        # Add frame to page
        self.about_layout.addWidget(
            self.about_frame,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.about_layout.addStretch()

        self.main_layout.addLayout(self.about_layout)

        font_path = (
            Path(BASE_DIR) / "assets" / "fonts" / "FrutigerAero.ttf"
        )

        font_id = QFontDatabase.addApplicationFont(
            str(font_path)
        )

        if font_id == -1:
            print("Font loading failed")
            self.custom_font = "Segoe UI"
            return

        font_families = QFontDatabase.applicationFontFamilies(
            font_id
        )

        self.custom_font = font_families[0]

        print("About font loaded:", self.custom_font)

class connection_window(QWidget):
    def __init__(self, custom_font, custom_font_bold):
        super().__init__()

        self.setWindowTitle("Device connection")
        self.setFixedSize(600, 400)

        self.custom_font = custom_font
        self.custom_font_bold = custom_font_bold

        self.create_background()

        self.create_connection_page()

        self.setLayout(self.connection_layout)

    def create_connection_page(self):

        # Main vertical layout
        self.connection_layout = QVBoxLayout()
        self.connection_layout.setSpacing(15)

        # -------------------------
        # HEADER
        # -------------------------

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(12)

        # Exit button
        icon_path = check_icon_availability("Sign026.ico")

        self.exit_button = AeroButton(
            radius=10,
            shadow=True,
            hover=True
        )

        self.exit_button.setIcon(QIcon(str(icon_path)))
        self.exit_button.setIconSize(QSize(26, 26))
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setToolTip("Close Connection")
        self.exit_button.clicked.connect(self.hide)

        self.title = QLabel("Connection settings")

        self.title.setFont(
            QFont(CUSTOM_FONT2, 25)
        )

        self.title.setStyleSheet("""
            QLabel {
                color: #000000;
                background: transparent;
            }
        """)

        self.connection_frame = GlassFrame(radius=20, shadow=True, hover_effect=True, theme="blue")
        self.connection_frame.setFixedSize(540, 275)

        self.top_layout.addWidget(self.exit_button, Qt.AlignLeft)
        self.top_layout.addWidget(self.title, Qt.AlignLeft)
        self.connection_layout.addLayout(self.top_layout)
        self.connection_layout.addStretch()
        self.connection_layout.addWidget(self.connection_frame)

    def create_background(self):
        image_path = (
            Path(BASE_DIR) / "assets" / "backgrounds" / "b4.jpg"
        )

        self.background_image = QPixmap(str(image_path))

        self.background = QLabel(self)
        self.background.setPixmap(self.background_image)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.lower()

        if self.background_image.isNull():
            print(f"ERROR: Could not load background: {image_path}")
    
if __name__ == "__main__":
    CUSTOM_FONT1, CUSTOM_FONT2 = load_fonts()
    s_window = settings_window(CUSTOM_FONT1, CUSTOM_FONT2)
    abt_window = about_window(CUSTOM_FONT1, CUSTOM_FONT2)
    con_window = connection_window(CUSTOM_FONT1, CUSTOM_FONT2)
    m_window = main_window(s_window, abt_window, con_window, CUSTOM_FONT1, CUSTOM_FONT2)
    sys.exit(app.exec())