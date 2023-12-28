import bcrypt

def hash_password(password):
    """
    Hàm này nhận vào một mật khẩu dưới dạng chuỗi và trả về mật khẩu đã được băm.
    """
    # Chuyển đổi mật khẩu sang dạng bytes, sau đó băm nó sử dụng bcrypt
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Trả về mật khẩu đã băm dưới dạng chuỗi để dễ dàng lưu trữ
    return hashed_password.decode('utf-8')

