#NOTE: Exception handling
import re
from datetime import datetime

def validate_idnum(id_num):
    if re.match(r"^\d{6}$", id_num):
        return id_num
    else:
        print("Invalid ID number. Please enter a valid 6-digit integer.")
        return None

def validate_phone(phone, student_manager):
    if not re.match(r"^\+?\d{1,3}[\s-]?\d{6,10}$", phone):
        print("Invalid phone number. Please enter a valid phone number.")
        return None

    # Retrieve all existing phone numbers
    existing_phones = [student.phone for student in student_manager.get_all_students()]

    # Check for duplicate phone number
    if phone in existing_phones:
        print("This phone number is already in use. Please enter a different phone number.")
        return None

    return phone


def validate_dob(dob):
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        return dob
    except ValueError:
        print("Invalid date of birth. Please enter a valid date in YYYY-MM-DD format.")
        return None

def validate_choice(choice):
    try:
        return int(choice)
    except ValueError:
        print("Invalid choice. Please enter a valid integer.")
        return None
