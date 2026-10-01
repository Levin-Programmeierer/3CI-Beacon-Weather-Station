# Written by Levin Boehler, started on 29.09.2026 at 18:36

#
# Imports
#

# Graphical User Interface Library
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt

import pyqtgraph as pg

import sys

#
# Classes
#

class mainwindow(QMainWindow): # <-- QMainWindow for GUI elements
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        # Window settings (title, size, etc.)
        self.setWindowTitle("Weather Station")
        self.setFixedSize(1000, 700)

        self.load_stylesheet()

        # Setup of the layouts

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

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

        title = QLabel("Weather Station 🌦️ - 3CI")
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
        """)

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