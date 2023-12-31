# app.py
import re # Regular expression library
from models.StudentManager import StudentManager
from models.User import User, UserManager
import stdiomask


from prettytable import PrettyTable
from termcolor import colored

from datetime import datetime
from models.CourseManager import Course, CourseManager

import getpass
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

#NOTE Utility functions


#FUNC Login
def login(users):
    username = input("Enter username: ")
    password = stdiomask.getpass("Enter your password: ", mask='*')
    # print(password)
    user = users.find_user(username)
    # get_user_info = users.get_user_info(username)
    # print(get_user_info)
    if user and user.check_password(password):
        return user
    else:
        print("Invalid username or password")
        return None
    
    
def print_with_border(text, color_code):
    border_length = len(text) + 4  # Adjust border length based on text length
    border_top = color_code + '+' + '-' * (border_length - 2) + '+\033[0m'  # Top border
    border_middle = color_code + '| ' + text + ' |\033[0m'  # Middle part with text
    border_bottom = color_code + '+' + '-' * (border_length - 2) + '+\033[0m'  # Bottom border

    print(border_top)
    print(border_middle)
    print(border_bottom)
#menu logic chuong trinh
def show_menu():
    welcome_text = "Welcome to Student Management System"
    color_code = '\033[94m'  # Blue color
    print_with_border(welcome_text, color_code)
    print("1. Login")
    print("2. Exit")
    choice = input("Enter your choice: ")
    return choice
def show_admin_menu():
    welcome_text = "Welcome to Admin Panel"
    color_code = '\033[92m'  # Green color
    print_with_border(welcome_text, color_code)
    print("1. Add student")
    print("2. Update student info")
    print("3. Delete student")
    print("4. Show student list and general infomation")
    print("5. Find and show student detail infomation")
    print("6. Complete student course")
    print("7. Logout")
    choice = input("Enter your choice: ")
    return choice
def show_student_menu():
    welcome_text = "Welcome to Student Panel"
    color_code = '\033[92m'  # Green color
    print_with_border(welcome_text, color_code)
    print("1. Show student info")
    print("2. Update student info")
    print("3. Enroll course")
    print("4. Change user password")
    print("5. Logout")
    choice = input("Enter your choice: ")
    return choice

# Functions for admin (include: add, update, delete, show list, show general infomation, find and show detail infomation)


def add_student(student_manager, users):
    print(colored("Add New Student", "green"))
    full_name = input("Enter full name: ")
    
    # Generate a new student ID
    existing_students = student_manager.get_all_students()
    highest_id = max([int(student.student_id) for student in existing_students], default=0)
    student_id = str(highest_id + 1)

    dob = None
    while dob is None:
        dob = validate_dob(input("Enter date of birth (YYYY/MM/DD): "))
    
    hometown = input("Enter hometown: ")
    phone = validate_phone(input("Enter phone number: "), student_manager)
    if phone is None:
        return
    major = input("Enter major: ")

    # Add the new student
    student_manager.add_student(full_name, student_id, dob, hometown, phone, major)
    print(colored("Student added successfully with ID: " + student_id, "blue"))

    # Create a new user for the student
    username = student_id
    password = student_id + "A"  # Create a password
    role = "student"  # Set role as 'student'
    users.add_user(username, password, role)  # Add new user
    print(colored(f"User for student {student_id} created with password {password}", "blue"))


def update_student(student_manager, logged_in_user=None):
    if logged_in_user and logged_in_user.role == "student":
        student_id = logged_in_user.username
    else:
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
    
    dob = None
    while dob is None:
        dob_input = input("Enter date of birth (YYYY/MM/DD): ")
        dob = validate_dob(dob_input)

        
    hometown = input("Enter hometown: ") or student.hometown
    # phone = validate_phone(input("Enter phone number: ")) or student.phone --- sửa lại
    phone = validate_phone(input("Enter phone number: "), student_manager) or student.phone
    major = student.major

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
    current_courses_table = PrettyTable()
    current_courses_table.field_names = [colored("Course Name", "blue"), colored("Course ID", "blue")]

    for course in student.current_courses:
        current_courses_table.add_row([course['Course Name'], course['Course ID']])

    if student.current_courses:
        print(colored("\nCurrent Courses:", "green"))
        print(current_courses_table)
    else:
        print(colored("\nNo current courses available.", "yellow"))
# Functions for user (include: show infomation, update infomation, enroll course, complete course)


def enroll_course(student_manager, course_manager, logged_in_user):
    student_id = logged_in_user.username  # Using the username as the student ID
    student = student_manager.find_student(student_id)

    if student is None:
        print(colored("Student not found.", "red"))
        return

    enrolled_courses = {course['Course ID'] for course in student.current_courses}
    all_courses = course_manager.courses
    major_courses = [course for course in all_courses if course.major_id == student.major]

    # Create a PrettyTable instance
    courses_table = PrettyTable()
    courses_table.field_names = [colored("Course ID", "blue"), colored("Course Name", "blue"), colored("Status", "blue")]

    for course in major_courses:
        status = colored("Enrolled", "green") if course.course_id in enrolled_courses else colored("Not Enrolled", "red")
        courses_table.add_row([course.course_id, course.course_name, status])


    print("\nCourses in your major:")
    print(courses_table)

    course_id_to_enroll = input("\nEnter Course ID to enroll (or press Enter to skip): ")
    if course_id_to_enroll:
        if course_id_to_enroll in enrolled_courses:
            print(colored("You are already enrolled in this course.", "yellow"))
        elif course_id_to_enroll not in [course.course_id for course in major_courses]:
            print(colored("Invalid Course ID or the course is not in your major.", "red"))
        else:
            course_to_enroll = next((course for course in major_courses if course.course_id == course_id_to_enroll), None)
            if course_to_enroll:
                print(colored("\nCourse Information:", "cyan"))
                print(f"Course ID: {course_to_enroll.course_id}")
                print(f"Course Name: {course_to_enroll.course_name}")
                print(f"Tuition Fee per credit: {course_to_enroll.tuition_fee}")
                print(f"Description: {course_to_enroll.description}")
                print(f"Major ID: {course_to_enroll.major_id}")
                print(f"Credit: {course_to_enroll.credit}")

                confirm = input(colored("Do you want to enroll in this course? (yes/no): ", "green")).lower()
                if confirm == 'yes':
                    student_manager.enroll_course(student_id, course_id_to_enroll, course_to_enroll.course_name)
                    print(colored(f"Enrolled in course: {course_to_enroll.course_name}", "green"))
                else:
                    print(colored("Enrollment canceled.", "yellow"))
            else:
                print(colored("Course not found.", "red"))


    
def complete_course(student_manager):
    student_id = input("Enter student ID: ")
    student = student_manager.find_student(student_id)

    if student is None:
        print(colored("Student not found.", "red"))
        return

    # Display current courses using PrettyTable
    current_courses_table = PrettyTable()
    current_courses_table.field_names = [colored("Course ID", "blue"), colored("Course Name", "blue")]

    for course in student.current_courses:
        current_courses_table.add_row([course['Course ID'], course['Course Name']])

    if student.current_courses:
        print(colored("\nCurrent Courses:", "green"))
        print(current_courses_table)
    else:
        print(colored("\nNo current courses available.", "yellow"))
        return

    course_id = input("Enter course ID to complete: ")
    if course_id not in [course['Course ID'] for course in student.current_courses]:
        print(colored("Course not found in your current courses.", "red"))
        return

    try:
        grade = float(input("Enter your grade for the course: "))
    except ValueError:
        print(colored("Invalid grade. Please enter a numeric value.", "red"))
        return

    student_manager.complete_course(student_id, course_id, grade)
    print(colored("Course marked as completed.", "green"))


def change_password(users, logged_in_user):
    old_password = stdiomask.getpass("Enter old password: ", mask='*')
    new_password = stdiomask.getpass("Enter new password: ", mask='*')
    confirm_password = stdiomask.getpass("Confirm new password: ", mask='*')

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
                            complete_course(student_manager)
                        elif choice == "7":
                            break
                        else:
                            print(colored("Invalid choice!", "red"))
                elif user.role == "student":
                    while True:
                        choice = show_student_menu()
                        if choice == "1":
                            find_and_show_detailed_information(student_manager, user)
                        elif choice == "2":
                            update_student(student_manager, user)
                        elif choice == "3":
                            enroll_course(student_manager, course_manager, user)
                        elif choice == "4":
                            change_password(users, user)
                        elif choice == "5":
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
