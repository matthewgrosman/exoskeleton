import time

from arduino.ArduinoClient import ArduinoClient, parse_port_data, validate_port_data
from matlab.get_end_effector import get_end_effector

if __name__ == '__main__':
    arduino_client = ArduinoClient()

    # As we need to ensure we have all 3 encoders data before we call the MATLAB function,
    # we will keep calling read_serial_port until we have data for all 3 encoders. This
    # dictionary lets us keep track of each encoder's reading.
    encoder_data = {
        ArduinoClient.ENCODER_0: None,
        ArduinoClient.ENCODER_1: None,
        ArduinoClient.ENCODER_2: None
    }

    while True:
        port_data = arduino_client.read_serial_port()

        if port_data and validate_port_data(port_data):
            encoder_name, encoder_value = parse_port_data(port_data)
            encoder_data[encoder_name] = encoder_value

        if None not in encoder_data.values():
            theta1, theta2 = get_end_effector(
                encoder_data[ArduinoClient.ENCODER_0],
                encoder_data[ArduinoClient.ENCODER_1],
                encoder_data[ArduinoClient.ENCODER_2]
            )

            # Reset encoder_data
            for encoder in encoder_data:
                encoder_data[encoder] = None

            # Brief pause so we aren't refreshing values too quickly
            time.sleep(0.20)

    arduino_client.close()
