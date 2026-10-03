# Written by Levin Boehler, started on 29.09.2026 at 18:36

#
# Imports
#

# Graphical User Interface Library
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
    QPushButton
)
from PyQt5.QtCore import Qt

# Graph GUI
import pyqtgraph as pg

# Important for application
import sys

#
# Variables
#

app_version = 0.2

#
# Classes
#

class mainwindow(QMainWindow): # <-- QMainWindow for GUI elements
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        # Window settings (title, size, etc.)
        self.setWindowTitle("Beacon - Weather Station")
        self.setFixedSize(1000, 700)

        self.load_stylesheet()

        # Setup of the main layout

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        settings_bar = self.create_settings_bar()
        main_layout.addLayout(settings_bar)

        header = self.create_header()
        main_layout.addLayout(header)
        
        sensors = self.create_sensor_cards()
        main_layout.addLayout(sensors)
        graph = self.create_graph_placeholder()
        main_layout.addWidget(graph, stretch=1)
        """
        bottom = self.create_bottom_section()
        main_layout.addLayout(bottom)

        history = self.create_history()
        main_layout.addLayout(history)
        """

    def create_header(self):
        layout = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setObjectName("title")

        time = QLabel("0:00 | 30.09") # Time and date are to be filled up later
        time.setAlignment(Qt.AlignRight)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(time)

        return layout

    def create_sensor_cards(self):
        layout = QGridLayout()

        cards = [
            ("🌡️", "Temperature", "NaN"),
            ("💧", "Humidity", "NaN"),
            ("🌀", "Pressure", "NaN"),
            ("🌧️", "Rain", "NaN")
        ]

        for i, (icon, name, value) in enumerate(cards):

            card = QFrame()
            card.setObjectName("card")

            card_layout = QVBoxLayout(card)

            title = QLabel(f"{icon} {name}")
            value_label = QLabel(value)

            value_label.setObjectName("sensorValue")

            card_layout.addWidget(title)
            card_layout.addWidget(value_label)

            layout.addWidget(card, 0, i)

        return layout

    def create_graph_placeholder(self):
        graph = pg.PlotWidget()

        graph.setBackground("white")
        graph.setTitle(
            "Temperatue / Humidity -- 25h",
            color="black",
            size="14pt"
        )

        graph.setLabel("left", "Temperature (°C)")
        graph.setLabel("bottom", "Time (h)")

        # Example values
        times = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        temperatures = [
            14.2, 13, 12, 10, 31.2,
            17.2, 18.4, 19.1, 18.9, 18.7
        ]

        graph.plot(
            times,
            temperatures,
            pen=pg.mkPen(width=2)
        )

        return graph

    def create_settings_bar(self):
        layout = QHBoxLayout()

        settings = QPushButton("⚙️ Settings")
        dashboard = QPushButton("🌦️ Dashboard")
        about = QPushButton("ℹ️ About")

        connected_status = QLabel("Connected: 🔴")
        connected_status.setObjectName("connectionStatus") # Names are needed to get the correct stylesheet

        # Connect buttons

        settings.clicked.connect(self.open_settings)
        about.clicked.connect(self.open_about)

        layout.addWidget(dashboard)
        layout.addWidget(settings)
        layout.addWidget(about)
        layout.addStretch()
        layout.addWidget(connected_status, alignment=Qt.AlignRight)

        return layout

    def open_settings(self):
        self.settings_page = settingspage()
        self.settings_page.show()

    def open_about(self):
        self.about_page = aboutpage()
        self.about_page.show()
       
# ChatGPT generated function
    def load_stylesheet(self):

        self.setStyleSheet("""
        QMainWindow {
            background-color: #f5f7fa;
        }

        QLabel#title {
            font-size: 26px;
            font-weight: bold;
            color: #1f2937;
        }

        QLabel#connectionStatus {
            background-color: #fef2f2;
            color: #dc2626;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: bold;
        
        }

        QFrame#card {
            background-color: white;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            padding: 12px;
        }

        QLabel#sensorName {
            font-size: 14px;
            color: #6b7280;
        }

        QLabel#sensorValue {
            font-size: 28px;
            font-weight: bold;
            color: #111827;
        }

        QTableWidget {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            gridline-color: #eeeeee;
        }

        QHeaderView::section {
            background-color: white;
            border: none;
            padding: 8px;
            font-weight: bold;
        }

        QPushButton {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 8px 14px;
            color: #374151;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #f3f4f6;
        }

        QPushButton:pressed {
            background-color: #e5e7eb;
        }
        """)

class settingspage(QWidget):
    def __init__(self):
        super().__init__()

        # General window settings

        self.setWindowTitle("Settings")
        self.setFixedSize(500, 400)

        # Layout setup

        layout = QVBoxLayout()

        layout2 = QHBoxLayout()

        title = QLabel("⚙️ Settings")
        #ChatGPT StyleSheet
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        # Settings buttons

        temperature = QLabel("Temperature unit:")
        layout2.addWidget(temperature)

        celsius = QPushButton("°C")
        fahrenheit = QPushButton("°F")

        layout2.addWidget(celsius)
        layout2.addWidget(fahrenheit)

        layout2.addStretch()

        layout.addLayout(layout2)

        self.setLayout(layout)

class aboutpage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        title = QLabel("About this program")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        version = QLabel(f"Current version: {app_version}")
        creators = QLabel(f"Created by: Levin Boehler, Dany Da Silva Marques")

        layout.addWidget(version)
        layout.addWidget(creators)

        self.setLayout(layout)

#
# Functions
#

def main():
    app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())

#
# Execution
#

# Check if the name is main or else it won't run
if __name__ == "__main__":
    main()