# The first data handler 😱😱😱😱😱
# Created by Levin Boehler of course!
# 10:06 - 14.11.2026
# It works 😱😱😱
import serial
import time

class ESP32:
    def __init__(self, port, baudrate=115200):
        # ESP32 connection configs like com port, baudrate etc.
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def connect(self):
        # Connect to the esp32

        self.connection = serial.Serial(
            self.port,
            self.baudrate,
            timeout=1
        )

        time.sleep(2)
        print("Log: ESP32 connected")

    def read_data(self):
        # Read and parse data, aka sort data
        if self.connection is None:
            #raise ConnectionError("ESP32 is not connected")
            self.no_connection()
            return None
        else:
            line = self.connection.readline().decode(
                "utf-8"
            ).strip()

            if not line:
                return None

        try:
            data = {}

            for item in line.split(","): # trennt noo komma
                key, value = item.split(":") # key z.b temperature a value z.b 20 grad also temperature:20C
                data[key] = float(value)

            return data

        except ValueError:
            return None

    def no_connection(self):
        pass

    def disconnect(self):
        # disconnect
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Log: Disconnected from ESP32")