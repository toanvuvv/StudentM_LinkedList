import base64
from utils.data_loader import load_data
from utils.data_writer import write_data
from utils.encryption_util import encrypt_data
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
            # Chuyển đổi chuỗi base64 trở lại thành byte
            password_decoded = base64.b64decode(user_info["password"].encode('utf-8'))
            user = User(user_info["username"], password_decoded, user_info["role"])
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
        users_data = []
        for user in self.users:
            # Chuyển đổi mật khẩu mã hóa thành chuỗi base64
            password_encoded = base64.b64encode(user.password).decode('utf-8')
            users_data.append({
                "Username": user.username,
                "Password": password_encoded,
                "Role": user.role
            })
        write_data(file_path, users_data)
