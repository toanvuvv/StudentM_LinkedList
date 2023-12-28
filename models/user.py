import bcrypt
from utils.data_loader import load_data
from utils.data_writer import write_data
class User:
    def __init__(self, username, password, role, hashed=False):
        self.username = username
        if hashed:
            self.password = password  # Sử dụng mật khẩu đã băm
        else:
            self.password = self.hash_password(password)  # Băm mật khẩu
        self.role = role

    def hash_password(self, password):
        # Băm mật khẩu
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # So sánh mật khẩu đã băm
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def is_admin(self):
        return self.role == "administrator"

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users_from_json("data/users.json")
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    def get_user_info(self, username):
        user = self.find_user(username)
        if not user:
            return None
        return {
            "Username": user.username,
            "Password": user.password,  # Lưu ý: đây là mật khẩu đã băm
            "Role": user.role
        }
    def load_users_from_json(self, file_path):
        users_data = load_data(file_path)
        self.users = []  # Làm trống danh sách trước khi thêm người dùng mới
        for user_info in users_data:
            user = User(user_info["username"], user_info["password"], user_info["role"], hashed=True)
            self.users.append(user)


    def save_users_to_json(self, file_path):
        # Tạo một danh sách chứa dữ liệu người dùng để lưu vào JSON
        users_data = []
        for user in self.users:
            user_data = {
                "username": user.username,
                "password": user.password,  # Lưu ý: đây là mật khẩu đã băm
                "role": user.role
            }
            users_data.append(user_data)
        # print ra tat ca user trong users_data
        

        # Ghi đè dữ liệu người dùng vào file JSON
        write_data(file_path, users_data)


    def add_user(self, username, password, role):
        if any(user.username == username for user in self.users):
            return None  # Người dùng đã tồn tại, không thêm vào danh sách
        user = User(username, password, role)
        self.users.append(user)
        return user

    def change_password(self, username, old_password, new_password):
        user = self.find_user(username)
        if not user or not user.check_password(old_password):
            return None
        user.password = user.hash_password(new_password)  # Băm mật khẩu mới
        return user
    def update_user(self, username, password=None, role=None):
        user = self.find_user(username)
        if not user:
            return None
        if password:
            user.password = user.hash_password(password)  # Băm mật khẩu mới
        if role:
            user.role = role
        return user
    def delete_user(self, username):
        user = self.find_user(username)
        if not user:
            return None
        self.users.remove(user)
        return user