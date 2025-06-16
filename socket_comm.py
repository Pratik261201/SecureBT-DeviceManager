# socket_comm.py

import socket
from encryption import SecureChannel


class EncryptedSocketServer:
    """
    TCP socket server that communicates using AES-CBC encryption.

    Requires a pre-shared AES key and IV to maintain encrypted messaging
    between the server and client.
    """

    def __init__(self, host='127.0.0.1', port=9090, key=None, iv=None):
        self.host = host
        self.port = port
        self.channel = SecureChannel(key=key, iv=iv)

    def start(self):
        """
        Start the server, accept one client connection, and handle
        a single message exchange over an encrypted channel.
        """
        print("🔐 [Server] Performing AES Handshake...")
        self.channel.handshake()
        print("✅ [Server] AES secure channel established.\n")

        # Create and bind the TCP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(1)
        print(f"📡 [Server] Listening on {self.host}:{self.port}...")

        conn, addr = server.accept()
        print(f"📥 [Server] Connection from {addr}")

        data = conn.recv(1024)
        if not data:
            print("⚠️ [Server] No data received.")
            conn.close()
            server.close()
            return

        # Decrypt and handle the message
        try:
            decrypted = self.channel.decrypt(data)
            print(f"🔓 [Server] Decrypted message: {decrypted}")
        except Exception as e:
            print(f"❌ [Server] Decryption failed: {e}")
            conn.close()
            server.close()
            return

        # Respond to the client with encrypted message
        response = f"Server ACK: Got '{decrypted}'"
        encrypted_response = self.channel.encrypt(response)
        conn.sendall(encrypted_response)

        conn.close()
        server.close()


class EncryptedSocketClient:
    """
    TCP socket client that sends an AES-CBC encrypted message
    and receives an encrypted response from the server.
    """

    def __init__(self, host='127.0.0.1', port=9090, key=None, iv=None):
        self.host = host
        self.port = port
        self.channel = SecureChannel(key=key, iv=iv)

    def start(self, message):
        """
        Connect to the server, send an encrypted message,
        and print the decrypted response.
        """
        print("🔐 [Client] Performing AES Handshake...")
        self.channel.handshake()
        print("✅ [Client] AES secure channel established.\n")

        # Create and connect socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        # Encrypt and send message
        encrypted_msg = self.channel.encrypt(message)
        client.sendall(encrypted_msg)

        # Receive and decrypt response
        encrypted_response = client.recv(1024)
        if not encrypted_response:
            print("❌ [Client] No response received.")
            client.close()
            return

        try:
            decrypted_response = self.channel.decrypt(encrypted_response)
            print(f"🔓 [Client] Decrypted response: {decrypted_response}")
        except Exception as e:
            print(f"❌ [Client] Decryption failed: {e}")

        client.close()
