from boresightWindow import BoresightWindow
from radarData import RadarData
from serialPortReader import SerialPortReader
import time

MAX_POINTS_ON_RADAR = 20
MAX_RADAR_DISTANCE = 200
MAX_RADAR_ANGLE = 90
MAX_RADAR_LINE_LIFETIME_IN_SECONDS = 1

SERIAL_PORT = "COM6"
SERIAL_BAUD_RATE = 9600
SERIAL_PORT_TIMEOUT = 200

UI_UPDATE_INTERVAL_IN_SECODNS = .01

def main():
    serial_reader = SerialPortReader(SERIAL_PORT, SERIAL_BAUD_RATE, SERIAL_PORT_TIMEOUT, MAX_POINTS_ON_RADAR)
    radar_data = RadarData(max_points=MAX_POINTS_ON_RADAR)
    boresight = BoresightWindow(MAX_RADAR_DISTANCE, MAX_RADAR_ANGLE, MAX_RADAR_LINE_LIFETIME_IN_SECONDS)

    serial_reader.start()

    while serial_reader.is_connected():
        line_of_bytes = serial_reader.get_last_line_of_bytes()

        if line_of_bytes is not None:
            radar_data.append(line_of_bytes)
            boresight.update(radar_data)
        
        try:
            time.sleep(UI_UPDATE_INTERVAL_IN_SECODNS)
        except KeyboardInterrupt:
            pass
        
    serial_reader.stop()

if __name__ == "__main__":
    main()
