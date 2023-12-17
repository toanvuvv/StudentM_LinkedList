from models.user import User
from utils.data_loader import load_data
from utils.data_writer import write_data
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # Lưu ý: Mật khẩu nên được mã hóa
        self.role = role  # "admin" hoặc "user"

    def check_password(self, password):
        # Kiểm tra mật khẩu, trả về True nếu khớp
        return self.password == password

    def is_admin(self):
        return self.role == "admin"
class UserManager:
    def __init__(self):
        self.users = []
        self.load_users_from_json("data/users.json")
    def load_users_from_json(self, file_path):
        users_data = load_data(file_path)
        for user_info in users_data:
            user = User(user_info["Username"], user_info["Password"], user_info["Role"])
            self.users.append(user)
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    def add_user(self, username, password, role):
        user = User(username, password, role)
        self.users.append(user)
        return user
    def update_user(self, username, password=None, role=None):
        user = self.find_user(username)
        if not user:
            return None
        if password:
            user.password = password
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
            users_data.append({
                "Username": user.username,
                "Password": user.password,
                "Role": user.role
            })
        write_data(file_path, users_data)