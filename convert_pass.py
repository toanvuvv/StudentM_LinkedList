from utils.encryption_util import encrypt_data, decrypt_data
import base64

sample_password = "phuongthanh"
encrypted_password = encrypt_data(sample_password)
password_encoded = base64.b64encode(encrypted_password).decode('utf-8')
print(password_encoded)
password_decoded = base64.b64decode(password_encoded)
password_decrypted = decrypt_data(password_decoded)
print(password_decrypted)