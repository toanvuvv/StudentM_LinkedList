# app.py
from models.StudentManager import StudentManager
from models.user import User, UserManager
from utils.data_loader import load_data 

from utils.encryption_util import encrypt_data, decrypt_data

# Khởi tạo và tải dữ liệu sinh viên
student_manager = StudentManager()
student_manager.load_students("data/students.json")

# Tải dữ liệu người dùng
users = UserManager()
users.load_users_from_json("data/users.json")


#menu logic chuong trinh
def login(users):
    username = input("Enter username: ")
    password = input("Enter password: ")  # Trong thực tế, mật khẩu nên được nhập một cách an toàn hơn

    user = users.find_user(username)
    if user and user.check_password(password):
        return user
    else:
        print("Invalid username or password")
        return None
    

def show_menu():
    print("Welcome to Student Management System")
    print("1. Login")
    print("2. Exit")
    choice = input("Enter your choice: ")
    return choice
def show_admin_menu():
    print("Welcome to Admin Panel")
    print("1. Add student")
    print("2. Update student")
    print("3. Delete student")
    print("4. Show student list")
    print("5. Logout")
    choice = input("Enter your choice: ")
    return choice
def show_student_menu():
    print("Welcome to Student Panel")
    print("1. Show student info")
    print("2. Update student info")
    print("3. Enroll course")
    print("4. Complete course")
    print("5. Logout")
    choice = input("Enter your choice: ")
    return choice
def add_student():
    print("Add student")
    full_name = input("Enter full name: ")
    student_id = input("Enter student ID: ")
    dob = input("Enter date of birth: ")
    hometown = input("Enter hometown: ")
    phone = input("Enter phone number: ")
    major = input("Enter major: ")
    student_manager.add_student(full_name, student_id, dob, hometown, phone, major)
    print("Add student successfully")
def update_student():
    print("Update student")
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)
    if not student:
        print("Student not found")
        return
    print("Student found:")
    print(student.get_student_info())
    print("Enter new information (leave blank if no change)")
    full_name = input("Enter full name: ")
    dob = input("Enter date of birth: ")
    hometown = input("Enter hometown: ")
    phone = input("Enter phone number: ")
    major = input("Enter major: ")
    student_manager.update_student(student_id, full_name, dob, hometown, phone, major)
    print("Update student successfully")
def delete_student():
    print("Delete student")
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)
    if not student:
        print("Student not found")
        return
    print("Student found:")
    print(student.get_student_info())
    confirm = input("Are you sure you want to delete this student? (y/n) ")
    if confirm == "y":
        student_manager.delete_student(student_id)
        print("Delete student successfully")
def show_student_list():
    print("Student list")
    student_manager.show_students()
def show_student_info():
    print("Student info")
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)
    if not student:
        print("Student not found")
        return
    print("Student found:")
    print(student.get_student_info())
def update_student_info():
    print("Update student info")
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)
    if not student:
        print("Student not found")
        return
    print("Student found:")
    print(student.get_student_info())
    print("Enter new information (leave blank if no change)")
    full_name = input("Enter full name: ")
    dob = input("Enter date of birth: ")
    hometown = input("Enter hometown: ")
    phone = input("Enter phone number: ")
    student_manager.update_student(student_id, full_name, dob, hometown, phone)
    print("Update student info successfully")
def enroll_course():
    print("Enroll course")
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)
    if not student:
        print("Student not found")
        return
    print("Student found:")
    print(student.get_student_info())
    course_id = input("Enter course ID: ")
    course_name = input("Enter course name: ")
    student_manager.enroll_course(student_id, course_id, course_name)
    print("Enroll course successfully")
def complete_course():
    print("Complete course")
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)
    if not student:
        print("Student not found")
        return
    print("Student found:")
    print(student.get_student_info())
    course_id = input("Enter course ID: ")
    grade = input("Enter grade: ")
    student_manager.complete_course(student_id, course_id, grade)
    print("Complete course successfully")
def main():
    while True:
        choice = show_menu()
        if choice == "1":
            user = login(users)
            if user:
                if user.is_admin():
                    while True:
                        choice = show_admin_menu()
                        if choice == "1":
                            add_student()
                        elif choice == "2":
                            update_student()
                        elif choice == "3":
                            delete_student()
                        elif choice == "4":
                            show_student_list()
                        elif choice == "5":
                            break
                        else:
                            print("Invalid choice")
                else:
                    while True:
                        choice = show_student_menu()
                        if choice == "1":
                            show_student_info()
                        elif choice == "2":
                            update_student_info()
                        elif choice == "3":
                            enroll_course()
                        elif choice == "4":
                            complete_course()
                        elif choice == "5":
                            break
                        else:
                            print("Invalid choice")
        elif choice == "2":
            break
        else:
            print("Invalid choice")
    student_manager.write_students("data/students.json")
    print("Goodbye!")
if __name__ == "__main__":
    main()