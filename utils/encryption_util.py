from cryptography.fernet import Fernet

# Generate a key and instantiate a Fernet object
key = Fernet.generate_key()
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
