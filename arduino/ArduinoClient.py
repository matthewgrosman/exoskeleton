import re
import serial
import serial.tools.list_ports

import arduino.constants as constants


def validate_port_data(port_data: str) -> bool:
    """
    Function that validates incoming Arduino input is valid. Valid data comes in the format:
    <ENCODER_NAME>:<ENCODER_VALUE>. ENCODER_NAME must be either "Encoder1", "Encoder2", or
    "Encoder3", and ENCODER_VALUE must be number (can be a floating point).

    :param port_data:   String containing a line of Arduino input.
    :return:            Bool denoting if this is valid input.
    """
    pattern = re.compile(constants.VALID_INPUT_REGEX)
    return bool(pattern.match(port_data))


def parse_port_data(port_data: str) -> (str, str):
    """
    Function that takes in a string containing a line of Arduino input and extracts/returns
    encoder name and the value of the encoder data.

    Arduino input comes in the following format: <ENCODER_NAME>:<ENCODER_VALUE>

    :param port_data:   String containing a line of Arduino input in the format described
                        above.
    :return:            Tuple containing encoder name and encoder value.
    """
    port_data_split = port_data.split(":")
    encoder_name = port_data_split[0]
    encoder_value = port_data_split[1]

    return encoder_name, encoder_value


def _find_comport() -> str:
    """
    Finds the COMPORT number that the Arduino is connected to. If the Arduino is not
    connected/detected, we will throw an Exception.

    We can determine which COMPORT number the Arduino is connected to by looking at
    the port.description attribute value. The Arduino has a port description of
    "Arduino Uno", so I just grab the port that contains the string "Arduino".

    :return:    String containing the COMPORT number the Arduino is connected to.
    """
    for port in serial.tools.list_ports.comports():
        if constants.PORT_DESCRIPTION_IDENTIFIER in port.description:
            return port.name

    raise Exception("Arduino not detected.")


class ArduinoClient:
    def __init__(self) -> None:
        self.serial = serial.Serial(
            port=_find_comport(),
            baudrate=115200,
            timeout=0.01  # Sets read frequency
        )

    def read_serial_port(self) -> str:
        return self.serial.readline().decode().strip()

    def close(self) -> None:
        self.serial.close()

    def __exit__(self) -> None:
        self.serial.close()
