# Secure Bluetooth Device Manager System

A command-line Python tool to securely manage and simulate Bluetooth Classic and BLE devices. This system performs real BLE scanning, maintains a device whitelist, encrypts data using AES, and optionally communicates via secure sockets.

---

## 🔧 Features

- **Real BLE Scanning** using `bleak` (no hardware required for simulation)
- **Device Identification**: Name, MAC address, and classification (`Classic` / `BLE`)
- **Whitelisting System**: Add/remove MACs from trusted devices
- **AES Encryption**: CBC-mode encryption with shared key/IV and simulated handshake
- **Secure Communication**: Encrypted message exchange with whitelisted devices
- **Socket Communication (Bonus)**: Simulated encrypted messaging over TCP
- **Fully CLI-Based**: No GUI or third-party frameworks

---

## 📸 Sample Output

```text
🔍 Scanning for real nearby BLE devices...

[1] Name: OPPO Enco Buds 2 | Type: BLE | MAC: A1:B2:C3:D4:E5:F6

✅ A1:B2:C3:D4:E5:F6 whitelisted.

🔗 Secure session with OPPO Enco Buds 2...
✅ Secure channel established.
🔒 Sent: 8A72FC...
🔒 Received: D02E93...
🟢 Decrypted: Ack from OPPO Enco Buds 2

[Encrypted socket simulation]
🔓 [Client] Decrypted response: Server ACK: Got 'Hello Server'
````

---

## 🚀 Getting Started

### Requirements

* Python 3.8 or higher
* `bleak` for BLE scanning
* `pycryptodome` for AES encryption

### Installation

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

---

## 📂 Project Structure

```
bluetooth-manager/
├── main.py                 # Entry point
├── cli.py                  # CLI control logic
├── device.py               # BluetoothDevice class
├── whitelist.py            # WhitelistManager class
├── encryption.py           # SecureChannel (AES)
├── socket_comm.py          # Encrypted socket client/server
└── README.md               # Project documentation
```

---

## 🔐 Encryption Details

* **Algorithm**: AES-128 CBC
* **Padding**: PKCS7
* **Handshake**: Simulated (pre-shared key and IV)
* Keys and IVs are randomly generated per session and shared between communicating endpoints.

---

## 🧠 Device Discovery

* **BLE Scanning** is done using `bleak`.
* Devices are identified by:

  * `name` (if available)
  * `MAC address`
  * `type`: statically labeled as `BLE` or simulated `Classic`

---

## ⚙️ Whitelisting

Only whitelisted devices (by MAC) are allowed to initiate or receive secure communication.

```text
> Add MAC to whitelist: A1:B2:C3:D4:E5:F6
> ✅ Whitelisted.
```

---

## 🧪Encrypted Socket Communication

Simulated client-server communication over localhost using AES-encrypted TCP messages.

* Server listens for encrypted messages.
* Client encrypts message and receives secure response.

---

## 🛡️ Disclaimer

This project is built for **educational and authorized use only**.
Do **not** use it to scan or interact with unauthorized Bluetooth devices.
Always ensure you have consent for any device scanning or connection.
---
