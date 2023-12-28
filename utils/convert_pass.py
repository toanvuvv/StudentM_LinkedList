from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def load_key():
    """Load the encryption key from the .env file."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("No ENCRYPTION_KEY found in .env file")
    return key

# Generate a key and instantiate a Fernet object
key = load_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    """Encrypt data."""
    if isinstance(data, str):
        data = data.encode()
    encrypted_data = cipher_suite.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data):
    """Decrypt data."""
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()

import base64

def encrypt_and_encode(password):
    # Mã hóa mật khẩu
    encrypted_password = encrypt_data(password)
    # Mã hóa Base64
    encoded_password = base64.b64encode(encrypted_password).decode('utf-8')
    return encoded_password

def decode_and_decrypt(encoded_password):
    # Giải mã Base64
    decoded_password = base64.b64decode(encoded_password)
    # Giải mã mật khẩu
    decrypted_password = decrypt_data(decoded_password)
    return decrypted_password

# Mật khẩu ban đầu
original_password = "phuongthanh"

# Mã hóa và mã hóa Base64
encoded_password = encrypt_and_encode(original_password)
print(f"Mật khẩu đã mã hóa và mã hóa Base64: {encoded_password}")

# Giải mã Base64 và giải mã
decrypted_password = decode_and_decrypt(encoded_password)
print(f"Mật khẩu sau khi giải mã: {decrypted_password}")
