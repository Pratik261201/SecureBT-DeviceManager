# whitelist.py

class WhitelistManager:
    """
    Handles storage and management of whitelisted Bluetooth device MAC addresses.
    """

    def __init__(self):
        self._whitelist = set()

    def add(self, mac: str) -> bool:
        self._whitelist.add(mac)
        return True

    def remove(self, mac: str) -> bool:
        self._whitelist.discard(mac)
        return True

    def is_whitelisted(self, mac: str) -> bool:
        return mac in self._whitelist

    def list(self):
        return list(self._whitelist)
