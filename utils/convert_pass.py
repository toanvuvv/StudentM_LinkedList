from encryption_util import encrypt_data, decrypt_data
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
original_password = "admin"

# Mã hóa và mã hóa Base64
encoded_password = encrypt_and_encode(original_password)
print(f"Mật khẩu đã mã hóa và mã hóa Base64: {encoded_password}")

# Giải mã Base64 và giải mã
decrypted_password = decode_and_decrypt(encoded_password)
print(f"Mật khẩu sau khi giải mã: {decrypted_password}")
