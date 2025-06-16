# device.py

class BluetoothDevice:
    """
    Represents a Bluetooth device with identifying information.

    Attributes:
        name (str): Human-readable device name (e.g., "OPPO Enco Buds 2").
        mac (str): MAC address in standard format (e.g., "E4:5F:01:9C:A3:FF").
        device_type (str): Either 'Classic' or 'BLE' to denote protocol.
    """

    def __init__(self, name: str, mac: str, device_type: str):
        self.name = name
        self.mac = mac
        self.device_type = device_type

    def __str__(self) -> str:
        """
        Returns a string representation of the device.
        """
        return f"Name: {self.name} | Type: {self.device_type} | MAC: {self.mac}"
