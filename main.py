import time
import tkinter as tk
import arduino.constants as constants

from arduino.ArduinoClient import ArduinoClient, parse_port_data, validate_port_data
from frontend.TkinterClient import TkinterClient
from calculation.get_end_effector import get_end_effector

# Time interval in seconds between each time we read data from the sensors.
DATA_REFRESH_TIME = 0.20

if __name__ == '__main__':
    root = tk.Tk()
    app = TkinterClient(root)
    arduino_client = ArduinoClient()

    # As we need to ensure we have all 3 encoders data before we call the MATLAB function,
    # we will keep calling read_serial_port until we have data for all 3 encoders. This
    # dictionary lets us keep track of each encoder's reading.
    encoder_data = {
        constants.ENCODER_0_NAME: None,
        constants.ENCODER_1_NAME: None,
        constants.ENCODER_2_NAME: None
    }

    while True:
        port_data = arduino_client.read_serial_port()

        if port_data and validate_port_data(port_data):
            encoder_name, encoder_value = parse_port_data(port_data)

            # We need to ensure the first value we pull is encoder #0 as the Arduino
            # will send all three encoder data at once, and we read each encoder's
            # data line-by-line starting with #0. If we were to grab encoder #1 first,
            # for example, by the time we pick up an encoder #0 reading, that reading
            # is coming from a different position since it belongs to a new data reading
            # altogether.
            if encoder_data[constants.ENCODER_0_NAME] is None:
                if encoder_name == constants.ENCODER_0_NAME:
                    encoder_data[encoder_name] = encoder_value
                else:
                    continue

            encoder_data[encoder_name] = encoder_value

        if None not in encoder_data.values():
            theta1, theta2 = get_end_effector(
                float(encoder_data[constants.ENCODER_0_NAME]),
                float(encoder_data[constants.ENCODER_1_NAME]),
                float(encoder_data[constants.ENCODER_2_NAME])
            )

            app.update_display(theta1, theta2)
            root.update()

            # Reset encoder_data
            for encoder in encoder_data:
                encoder_data[encoder] = None

            # Brief pause so we aren't refreshing values too quickly
            time.sleep(DATA_REFRESH_TIME)

    arduino_client.close()
