# cli.py

import asyncio
import random
import re
import threading
import time
from Crypto.Random import get_random_bytes

from device import BluetoothDevice
from whitelist import WhitelistManager
from encryption import SecureChannel
from bleak import BleakScanner  # Ensure bleak is installed


class BluetoothManagerCLI:
    """
    Command-line interface to manage BLE scanning, whitelisting,
    secure AES communication, and optional encrypted socket exchange.
    """

    def __init__(self):
        self.devices = []
        self.whitelist = WhitelistManager()
        self.secure_channels = {}

    async def _scan_ble(self, timeout=5.0):
        """
        Perform real BLE scan using bleak. Returns a list of found devices.
        """
        print(f"\n🔍 Scanning for real nearby BLE devices (timeout={timeout}s)...\n")
        found = await BleakScanner.discover(timeout=timeout)
        self.devices = [
            BluetoothDevice(d.name or "Unknown", d.address, "BLE")
            for d in found
        ]
        for idx, d in enumerate(self.devices, 1):
            print(f"[{idx}] {d}")

    def _is_valid_mac(self, mac):
        """
        Validate MAC address format.
        """
        return re.fullmatch(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac) is not None

    def _get_device_by_mac(self, mac):
        """
        Return a device object matching the given MAC.
        """
        return next((d for d in self.devices if d.mac == mac), None)

    def show_menu(self):
        """
        Display CLI menu options.
        """
        print("""
=============================
🔧 Bluetooth Device Manager
=============================
1. Scan real BLE devices
2. Show scanned devices
3. Add device to whitelist
4. Remove device from whitelist
5. Show whitelisted devices
6. Secure communicate with whitelisted
7. Start encrypted socket communication
8. Exit
=============================
        """)

    def start(self):
        """
        Main CLI loop to interact with the user.
        """
        loop = asyncio.get_event_loop()

        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if choice == '1':
                loop.run_until_complete(self._scan_ble())

            elif choice == '2':
                print("\n📡 Scanned Devices:")
                for d in self.devices:
                    print(f"  - {d}")

            elif choice == '3':
                mac = input("MAC to whitelist: ").strip().upper()
                if not self._is_valid_mac(mac):
                    print("❌ Invalid MAC format.")
                elif self._get_device_by_mac(mac):
                    self.whitelist.add(mac)
                    print(f"✅ {mac} whitelisted.")
                else:
                    print("❌ Device not found in last scan.")

            elif choice == '4':
                mac = input("MAC to remove: ").strip().upper()
                self.whitelist.remove(mac)
                print(f"🗑️ {mac} removed.")

            elif choice == '5':
                print("\n📝 Whitelisted Devices:")
                for mac in self.whitelist.list():
                    dev = self._get_device_by_mac(mac)
                    print(f"  - {dev.name if dev else 'Unknown'} ({mac})")

            elif choice == '6':
                mac = input("MAC to communicate: ").strip().upper()
                if not self._is_valid_mac(mac):
                    print("❌ Invalid MAC.")
                    continue
                if not self.whitelist.is_whitelisted(mac):
                    print("⚠️ Device is not whitelisted.")
                    continue

                dev = self._get_device_by_mac(mac)
                if not dev:
                    print("❌ Device not found in last scan.")
                    continue

                print(f"\n🔗 Establishing secure session with {dev.name}...")
                channel = SecureChannel()
                self.secure_channels[mac] = channel
                channel.handshake()

                msg = f"Hello {dev.name}"
                enc = channel.encrypt(msg)
                print(f"🔒 Sent: {enc.hex()}")

                ack = f"Ack from {dev.name}"
                enc_ack = channel.encrypt(ack)
                print(f"🔒 Received: {enc_ack.hex()}")
                print(f"🟢 Decrypted: {channel.decrypt(enc_ack)}")

            elif choice == '7':
                # Bonus: Encrypted Socket Communication
                from socket_comm import EncryptedSocketServer, EncryptedSocketClient

                # Shared AES key and IV
                key = get_random_bytes(16)
                iv = get_random_bytes(16)

                # Start the server in a background thread
                def run_server():
                    server = EncryptedSocketServer(key=key, iv=iv)
                    server.start()

                server_thread = threading.Thread(target=run_server, daemon=True)
                server_thread.start()

                time.sleep(1)  # Give the server a moment to start

                input_msg = input("Enter message to send to server: ")
                client = EncryptedSocketClient(key=key, iv=iv)
                client.start(input_msg)

            elif choice == '8':
                print("👋 Exiting Bluetooth Manager. Goodbye.")
                break

            else:
                print("❗ Invalid input. Please choose a valid option.")
