from ml.MatlabClient import MatlabClient
import exoskeletonengine
import time

from collections import namedtuple

from arduino.ArduinoClient import ArduinoClient, parse_port_data, validate_port_data

if __name__ == '__main__':
    arduino_client = ArduinoClient()

    # As we need to ensure we have all 3 encoders data before we call the MATLAB function,
    # we will keep calling read_serial_port until we have data for all 3 encoders. This
    # dictionary lets us keep track of each encoder's reading.
    encoder_data = {
        ArduinoClient.ENCODER_0: None,
        ArduinoClient.ENCODER_1: None,
        ArduinoClient.ENCODER_2: None,
    }

    # Current issue: the logic to store encoders is not correct- we're just holding values and stalling while the
    # device moves.

    while True:
        port_data = arduino_client.read_serial_port()

        if port_data and validate_port_data(port_data):
            encoder_name, encoder_value = parse_port_data(port_data)
            encoder_data[encoder_name] = encoder_value

        if None not in encoder_data.values():
            print("Calling MATLAB file", encoder_data)
            # call matlab file

            # Reset encoder_data
            for k in encoder_data:
                encoder_data[k] = None
        else:
            print("Still waiting: ", encoder_data)

        quit = input("enter Q to quit loop")
        if quit == 'q':
            break

    arduino_client.close()
