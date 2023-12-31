import bcrypt

def hash_password(password):
        # Băm mật khẩu
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

password1 = "thanh1"
print(hash_password(password1))