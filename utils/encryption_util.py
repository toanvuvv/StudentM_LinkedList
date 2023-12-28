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
