from struct import unpack
import binascii
from bluepy import btle


class RecvDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.handleDataBufffer = {}

    def handleNotification(self, cHandle, data):
        if self.handleDataBufffer.get(cHandle):
            self.handleDataBufffer[cHandle] += data
        else:
            self.handleDataBufffer[cHandle] = data

    def notifyClear(self):
        self.handleDataBufffer = {}


class Characteristic(btle.Characteristic):
    def __init__(self, ch):
        super(Characteristic, self).__init__(
            ch.peripheral, ch.uuid,
            ch.handle, ch.properties, ch.valHandle
        )

    def enable_notify(self):
        setup_data = b"\x01\x00"
        client_char_config = self.getDescriptors(forUUID=0x2902)
        if client_char_config:
            client_char_config = client_char_config[0]
            client_char_config.write(setup_data, withResponse=True)
        else:
            notify_handle = self.getHandle() + 1
            self.peripheral.writeCharacteristic(notify_handle, setup_data, withResponse=True)

    def read_string(self):
        return self.read().decode()

    def read_byte(self):
        return unpack('B', self.read())[0]

    def read_hex(self):
        return binascii.hexlify(self.read())

    def read_uint16(self):
        return unpack('H', self.read())[0]


class Driver:
    def __init__(self, dev, uuid):
        super(Driver, self).__init__()
        self.dev = dev
        self.name = None
        self.svc = self.dev.getServiceByUUID(uuid)

    def getCharacteristic(self, uuid):
        c = self.dev.getCharacteristics(uuid=uuid)[0]
        return Characteristic(c)

    def __str__(self):
        output = [self.name]
        for x in dir(self):
            if x.startswith('get_'):
                # Modify 'get_method_name' -> 'Method Name'
                method_name = ' '.join(map(lambda s: s.title(), x[len('get_'):].split('_')))
                method_value = getattr(self, x)()
                output.append('[+] %s: %s' % (method_name, method_value))
        return '\n'.join(output)


class DeviceInformationDriver(Driver):
    def __init__(self, dev):
        super(DeviceInformationDriver, self).__init__(dev=dev, uuid='180a')
        self.name = 'Device Information'

    def get_manufacturer_name(self):
        return self.getCharacteristic('2a29').read_string()

    def get_model_number(self):
        return self.getCharacteristic('2a24').read_string()

    def get_serial_number(self):
        return self.getCharacteristic('2a25').read_string()

    def get_hardware_revision(self):
        return self.getCharacteristic('2a27').read_string()

    def get_firmware_revision(self):
        return self.getCharacteristic('2a26').read_string()

    def get_system_id(self):
        return self.getCharacteristic('2a23').read_hex()


class GenericAccessDriver(Driver):
    appearances = {
        0: "Unknown",
        1024: "Generic Glucose Meter",
        1088: "Generic: Running Walking Sensor",
        1089: "Running Walking Sensor: In-Shoe",
        1090: "Running Walking Sensor: On-Shoe",
        1091: "Running Walking Sensor: On-Hip",
        1152: "Generic: Cycling",
        1153: "Cycling: Cycling Computer",
        1154: "Cycling: Speed Sensor",
        1155: "Cycling: Cadence Sensor",
        1156: "Cycling: Power Sensor",
        1157: "Cycling: Speed and Cadence Sensor",
        128: "Generic Computer",
        192: "Generic Watch",
        193: "Watch: Sports Watch",
        256: "Generic Clock",
        3136: "Generic: Pulse Oximeter",
        3137: "Fingertip Pulse",
        3138: "Wrist Worn",
        320: "Generic Display",
        3200: "Generic: Weight Scale",
        384: "Generic Remote Control",
        448: "Generic Eye-glasses",
        512: "Generic Tag",
        5184: "Generic: Outdoor Sports Activity",
        5185: "Location Display Device",
        5186: "Location and Navigation Display Device",
        5187: "Location Pod",
        5188: "Location and Navigation Pod",
        576: "Generic Keyring",
        64: "Generic Phone",
        640: "Generic Media Player",
        704: "Generic Barcode Scanner",
        768: "Generic Thermometer",
        769: "Thermometer: Ear",
        832: "Generic Heart rate Sensor",
        833: "Heart Rate Sensor: Heart Rate Belt",
        896: "Generic Blood Pressure",
        897: "Blood Pressure: Arm Blood",
        898: "Blood Pressure: Wrist Blood",
        960: "Human Interface Device (HID)",
        961: "Keyboard",
        962: "Mouse",
        963: "Joystick",
        964: "Gamepad",
        965: "Digitizer Tablet",
        966: "Card Reader",
        967: "Digital Pen",
        968: "Barcode Scanner",
    }

    def __init__(self, dev):
        super(GenericAccessDriver, self).__init__(dev=dev, uuid='1800')
        self.name = 'Generic Access'

    def get_device_name(self):
        return self.getCharacteristic('2a00').read_string()

    def get_appearance(self):
        b = self.getCharacteristic('2a01').read_uint16()
        return self.appearances.get(b)

    def get_peripheral_preferred_connection_parameters(self):
        return self.getCharacteristic('2a04').read_hex()


class NordicUARTDriver(Driver):
    def __init__(self, dev):
        super(NordicUARTDriver, self).__init__(dev=dev, uuid='6e400001-b5a3-f393-e0a9-e50e24dcca9e')
        self.name = 'Nordic UART'
        self.rx = self.getCharacteristic('6e400003-b5a3-f393-e0a9-e50e24dcca9e')
        self.tx = self.getCharacteristic('6e400002-b5a3-f393-e0a9-e50e24dcca9e')
        self.rx.enable_notify()

    def send(self, pkg, withResponse=False):
        self.tx.write(pkg)
        self.dev.waitForNotifications(1.0)
        if withResponse:
            handle = self.rx.getHandle()
            response = self.dev.delegate.handleDataBufffer.get(handle)
            if response:
                self.dev.delegate.notifyClear()
                return response
        return None


class BattaryDriver(Driver):
    def __init__(self, dev):
        super(BattaryDriver, self).__init__(dev=dev, uuid='180f')
        self.name = 'Battery Service'

    def get_battery_level(self):
        return self.getCharacteristic('2a19').read_byte()


def connect(mac, atype=btle.ADDR_TYPE_PUBLIC, c=0):
    if c == 5:
        return None
    try:
        dev = btle.Peripheral(mac, atype)
    except btle.BTLEDisconnectError:
        c += 1
        atype = 'public' if atype == 'random' else 'random'
        return connect(mac, atype, c)
    return dev
