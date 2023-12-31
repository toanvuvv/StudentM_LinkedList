# app.py
import re # Regular expression library
from models.StudentManager import StudentManager
from models.User import User, UserManager

from prettytable import PrettyTable
from termcolor import colored

from datetime import datetime
from models.CourseManager import Course, CourseManager

from utils.calculate import calculate_student_year, calculate_gpa, calculate_tuition_fee
from utils.exception import validate_idnum, validate_phone, validate_dob, validate_choice

# Khởi tạo và tải dữ liệu sinh viên
student_manager = StudentManager()
student_manager.load_students("data/students.json")

# Khoi tao va tai du lieu khoa hoc
course_manager = CourseManager()
course_manager.load_courses("data/courses.json")

# Tải dữ liệu người dùng
users = UserManager()
users.load_users_from_json("data/users.json")

#NOTEUtility functions


#FUNC Login
def login(users):
    username = input("Enter username: ")
    password = input("Enter password: ")  # Trong thực tế, mật khẩu nên được nhập một cách an toàn hơn

    user = users.find_user(username)
    get_user_info = users.get_user_info(username)
    print(get_user_info)
    if user and user.check_password(password):
        return user
    else:
        print("Invalid username or password")
        return None
#menu logic chuong trinh
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
    print("4. Show student list and general infomation")
    print("5. Find and show student detail infomation")
    print("6. Logout")
    choice = input("Enter your choice: ")
    return choice
def show_student_menu():
    print("Welcome to Student Panel")
    print("1. Show student info")
    print("2. Update student info")
    print("3. Enroll course")
    print("4. Complete course")
    print("5. Change user password")
    print("6. Logout")
    choice = input("Enter your choice: ")
    return choice

# Functions for admin (include: add, update, delete, show list, show general infomation, find and show detail infomation)
def add_student(student_manager, users):
    print(colored("Add New Student", "green"))
    full_name = input("Enter full name: ")
    student_id = validate_idnum(input("Enter student ID: "))
    if student_id is None:
        return
    dob = validate_dob(input("Enter date of birth (YYYY/MM/DD): "))
    if dob is None:
        return
    hometown = input("Enter hometown: ")
    phone = validate_phone(input("Enter phone number: "))
    if phone is None:
        return
    major = input("Enter major: ")

    # Thêm student mới
    # student_manager: chua thong tin danh sach tat ca sinh vien

    student_manager.add_student(full_name, student_id, dob, hometown, phone, major)
    print(colored("Student added successfully!", "blue"))

    # Tạo user mới cho student
    username = student_id
    password = student_id + "A"  # Tạo password
    role = "student"  # Đặt role là 'student'
    users.add_user(username, password, role)  # Thêm user mới
    print(colored(f"User for student {student_id} created with password {password}", "blue"))

def update_student(student_manager):
    print(colored("Update Student Information", "yellow"))
    student_id = validate_idnum(input("Enter student ID: "))
    if student_id is None:
        return

    # Check if the student exists
    student = student_manager.find_student(student_id)
    if not student:
        print(colored("Student not found!", "red"))
        return

    # Collect new details (leave blank if no change)
    print("Enter new information (leave blank if no change):")
    full_name = input("Enter full name: ") or student.full_name
    dob = validate_dob(input("Enter date of birth (DD/MM/YYYY): ")) or student.dob
    hometown = input("Enter hometown: ") or student.hometown
    phone = validate_phone(input("Enter phone number: ")) or student.phone
    major = input("Enter major: ") or student.major

    # Update the student
    student_manager.update_student(student_id, full_name, dob, hometown, phone, major)
    print(colored("Student updated successfully!", "blue"))
def delete_student(student_manager, users):
    print(colored("Delete Student", "red"))
    student_id = validate_idnum(input("Enter student ID to delete: "))
    if student_id is None:
        return

    # Kiểm tra xem student có tồn tại không
    student = student_manager.find_student(student_id)
    if not student:
        print(colored("Student not found!", "red"))
        return

    # Xác nhận trước khi xoá
    confirm = input("Are you sure you want to delete this student? (y/n): ")
    if confirm.lower() == 'y':
        student_manager.delete_student(student_id)
        print(colored("Student deleted successfully!", "blue"))

        # Xoá user tương ứng
        if users.delete_user(student_id):
            print(colored(f"User for student {student_id} also deleted.", "blue"))
        else:
            print(colored(f"No user found for student {student_id}.", "yellow"))
    else:
        print(colored("Student deletion cancelled.", "yellow"))

def show_student_list(student_manager):
    students = student_manager.get_all_students()  # Assuming this method exists
    table = PrettyTable()
    table.field_names = ["Name","Student ID", "DOB", "Phone", "Year", "Major", "GPA"]

    for student in students:
        year = calculate_student_year(student.student_id)
        gpa = calculate_gpa(student.completed_courses,course_manager)  # Assuming completed_courses is a list of dictionaries
        table.add_row([student.full_name,student.student_id, student.dob, student.phone, year, student.major, gpa])

    print(table)

def find_and_show_detailed_information(student_manager, user):
    if user.role == "administrator":
        student_id = input("Enter student ID: ")
    else:
        student_id = user.username  # For students, use the username as the student ID

    student = student_manager.find_student(student_id)

    if student is None:
        print(colored("Student not found.", "red"))
        return

    year = calculate_student_year(student.student_id)
    gpa = calculate_gpa(student.completed_courses, course_manager)  # Assuming completed_courses is a list of dictionaries
    tuition_fee = calculate_tuition_fee(student, course_manager)
    # Student Basic Information Table
    info_table = PrettyTable()
    info_table.field_names = [colored("Field", "blue"), colored("Information", "blue")]
    info_table.add_row(["Name", student.full_name])
    info_table.add_row(["Student ID", student.student_id])
    info_table.add_row(["Date of Birth", student.dob])
    info_table.add_row(["Hometown", student.hometown])
    info_table.add_row(["Phone Number", student.phone])
    info_table.add_row(["Major", student.major])
    info_table.add_row(["Year in University", year])
    info_table.add_row(["GPA", gpa])
    info_table.add_row(["Tuition Fee", tuition_fee])
    print("\n" + colored("Detailed Student Information", "green"))
    print(info_table)

    # Completed Courses Table
    courses_table = PrettyTable()
    courses_table.field_names = [colored("Course Name", "blue"), colored("Grade", "blue")]

    for course in student.completed_courses:
        courses_table.add_row([course['Course Name'], course['Grade']])

    if student.completed_courses:
        print(colored("\nCompleted Courses:", "green"))
        print(courses_table)
    else:
        print(colored("\nNo completed courses available.", "yellow"))
    # Current Courses Table
    courses_table = PrettyTable()
    courses_table.field_names = [colored("Course Name", "blue"), colored("Course ID", "blue")]
    print(colored("\nCurrent Courses:", "green"))
    print(courses_table)
# Functions for user (include: show infomation, update infomation, enroll course, complete course)
def enroll_course(student_manager, course_manager, logged_in_user):
    # Assuming logged_in_user is an instance of the User class
    student_id = logged_in_user.username  # Using the username as the student ID
    student = student_manager.find_student(student_id)

    if student is None:
        print("Student not found.")
        return

    course_id = input("Enter course ID: ")
    course = course_manager.get_course_info(course_id)

    if course is None:
        print("Course not found.")
        return

    # Check if the course is part of the student's major
    if course['Major ID'] != student.major:
        print("This course is not part of your major.")
        return

    student_manager.enroll_course(student_id, course_id, course['Course Name'])
    print(f"Student enrolled in course: {course['Course Name']}")
def complete_course(student_manager, logged_in_user):
    student_id = logged_in_user.username  # Assuming username is the student ID
    student = student_manager.find_student(student_id)

    if student is None:
        print("Student not found.")
        return

    course_id = input("Enter course ID: ")
    # Check if the course is in the student's current courses
    if not any(course['Course ID'] == course_id for course in student.current_courses):
        print("Course not found in your current courses.")
        return

    try:
        grade = float(input("Enter your grade for the course: "))
    except ValueError:
        print("Invalid grade. Please enter a numeric value.")
        return

    # Mark the course as completed
    student_manager.complete_course(student_id, course_id, grade)
    print("Course marked as completed.")
def change_password(users, logged_in_user):
    old_password = input("Enter old password: ")
    new_password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")

    if new_password != confirm_password:
        print("New password and confirm password do not match.")
        return

    user = users.change_password(logged_in_user.username, old_password, new_password)

    if user:
        print("Password changed successfully.")
    else:
        print("Invalid old password.")
# Main program logic
def main():
    while True:
        choice = show_menu()
        if choice == "1":
            user = login(users)
            if user:
                print(colored("Login successfully!", "blue"))
                if user.role == "administrator":
                    while True:
                        choice = show_admin_menu()
                        if choice == "1":
                            add_student(student_manager, users)
                        elif choice == "2":
                            update_student(student_manager)
                        elif choice == "3":
                            delete_student(student_manager, users)
                        elif choice == "4":
                            show_student_list(student_manager)
                        elif choice == "5":
                            find_and_show_detailed_information(student_manager, user)
                        elif choice == "6":
                            break
                        else:
                            print(colored("Invalid choice!", "red"))
                elif user.role == "student":
                    while True:
                        choice = show_student_menu()
                        if choice == "1":
                            find_and_show_detailed_information(student_manager, user)
                        elif choice == "2":
                            update_student(student_manager)
                        elif choice == "3":
                            enroll_course(student_manager, course_manager, user)
                        elif choice == "4":
                            complete_course(student_manager, user)
                        elif choice == "5":
                            change_password(users, user)
                        elif choice == "6":
                            break
                        else:
                            print(colored("Invalid choice!", "red"))
        elif choice == "2":
            # Save data
            student_manager.write_students("data/students.json")
            course_manager.save_courses("data/courses.json")
            users.save_users_to_json("data/users.json")
            break
        else:
            print(colored("Invalid choice!", "red"))
    print(colored("Goodbye!", "green"))
if __name__ == "__main__":
    main()
