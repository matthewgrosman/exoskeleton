import serial
import serial.tools.list_ports


def find_comport():
    ports = list(serial.tools.list_ports.comports())

    for p in ports:
        print("name: ", p.name)
        print("description: ", p.description)
        print("pid: ", p.pid)
        print("serial number: ", p.serial_number)
        print("product: ", p.product)
        print("vid: ", p.vid)
        print("device: ", p.device)
        print("location: ", p.location)
        print("interface: ", p.interface)


if __name__ == '__main__':
    find_comport()
