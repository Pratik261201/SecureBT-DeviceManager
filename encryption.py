# encryption.py

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class SecureChannel:
    """
    SecureChannel handles AES-CBC encryption and decryption.
    
    This class supports initialization with an optional pre-shared
    key and IV (Initialization Vector), which is crucial for secure
    communication over sockets or between trusted devices.
    """

    def __init__(self, key: bytes = None, iv: bytes = None):
        """
        Initialize the AES channel with a 128-bit key and IV.
        If not provided, both are randomly generated.
        """
        self.key = key or get_random_bytes(16)  # 128-bit AES key
        self.iv = iv or get_random_bytes(16)    # 128-bit IV
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv=self.iv)

    def handshake(self):
        """
        Simulates a cryptographic handshake.
        For this use-case, the key/IV are assumed to be pre-shared,
        so nothing is exchanged. This method just logs the step.
        """
        print("✅ Secure channel established.")

    def encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt a UTF-8 string into AES-encrypted ciphertext.
        Padding is applied to match AES block size.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv=self.iv)
        padded = pad(plaintext.encode(), AES.block_size)
        return cipher.encrypt(padded)

    def decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt AES-encrypted bytes and return the original string.
        Unpadding is applied after decryption.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv=self.iv)
        decrypted = cipher.decrypt(ciphertext)
        return unpad(decrypted, AES.block_size).decode()
