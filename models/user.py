import base64
from utils.data_loader import load_data
from utils.data_writer import write_data
from utils.encryption_util import encrypt_data , decrypt_data
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = encrypt_data(password)  # Mã hóa mật khẩu
        self.role = role

    def check_password(self, password):
        # So sánh mật khẩu đã mã hóa
        return self.password == encrypt_data(password)

    def is_admin(self):
        return self.role == "administrator"
class UserManager:
    def __init__(self):
        self.users = []
        self.load_users_from_json("data/users.json")
    def load_users_from_json(self, file_path):
            users_data = load_data(file_path)
            for user_info in users_data:
                # Decode from Base64 and then decrypt
                password_encoded = user_info["Password"].encode('utf-8')
                password_decoded = base64.b64decode(password_encoded)
                password_decrypted = decrypt_data(password_decoded)

                user = User(user_info["Username"], password_decrypted, user_info["Role"])
                self.users.append(user)

    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    def add_user(self, username, password, role):
        encrypted_password = encrypt_data(password)  # Mã hóa mật khẩu
        user = User(username, encrypted_password, role)
        self.users.append(user)
        return user
    def change_password(self, username, old_password, new_password):
        user = self.find_user(username)
        if not user:
            return None
        if not user.check_password(old_password):  # Kiểm tra mật khẩu cũ
            return None
        encrypted_new_password = encrypt_data(new_password)  # Mã hóa mật khẩu mới
        user.password = encrypted_new_password
        return user
    def update_user(self, username, password=None, role=None):
        user = self.find_user(username)
        if not user:
            return None
        if password:
            encrypted_password = encrypt_data(password)  # Mã hóa mật khẩu mới
            user.password = encrypted_password
        if role:
            user.role = role
        return user
    def update_user(self, username, password=None, role=None):
        user = self.find_user(username)
        if not user:
            return None
        if password:
            encrypted_password = encrypt_data(password)  # Mã hóa mật khẩu mới
            user.password = encrypted_password
        if role:
            user.role = role
        return user
    def delete_user(self, username):
        user = self.find_user(username)
        if not user:
            return None
        self.users.remove(user)
        return user

    def save_users_to_json(self, file_path):
        existing_users = load_data(file_path)  # Load existing data
        updated_users = {user['Username']: user for user in existing_users}  # Convert to dict for easy lookup

        for user in self.users:
            # Encrypt and encode to Base64
            password_encrypted = encrypt_data(user.password)
            password_encoded = base64.b64encode(password_encrypted).decode('utf-8')

            # Update or add new user
            updated_users[user.username] = {
                "Username": user.username,
                "Password": password_encoded,
                "Role": user.role
            }

        # Convert back to list and write to file
        users_data = list(updated_users.values())
        write_data(file_path, users_data)
