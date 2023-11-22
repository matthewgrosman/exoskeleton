import serial
import serial.tools.list_ports


def validate_port_data(port_data: str):
    if not any(encoder in port_data for encoder in [ArduinoClient.ENCODER_0, ArduinoClient.ENCODER_1, ArduinoClient.ENCODER_2]):
        return False

    return True


def parse_port_data(port_data: str) -> (str, str):
    port_data_split = port_data.split(":")
    encoder_name = port_data_split[0]
    encoder_value = port_data_split[1]

    return encoder_name, encoder_value


def _find_comport():
    for port in serial.tools.list_ports.comports():
        if "Arduino" in port.description:
            return port.name

    raise Exception("Arduino not detected.")


class ArduinoClient:
    ENCODER_0 = "Encoder0"
    ENCODER_1 = "Encoder1"
    ENCODER_2 = "Encoder2"

    def __init__(self) -> None:
        self.serial = serial.Serial(
            port=_find_comport(),
            baudrate=115200,
            timeout=0.01  # sets read frequency
        )

    def read_serial_port(self) -> str:
        return self.serial.readline().decode().strip()

    def flush_input(self):
        self.serial.flushInput()

    def close(self):
        self.serial.close()

    def __exit__(self):
        self.serial.close()
