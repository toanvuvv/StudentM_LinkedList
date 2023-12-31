#NOTE: Exception handling
import re
import datetime

def validate_idnum(id_num):
    if re.match(r"^\d{6}$", id_num):
        return id_num
    else:
        print("Invalid ID number. Please enter a valid 6-digit integer.")
        return None

def validate_phone(phone):
    if re.match(r"^\+?\d{1,3}[\s-]?\d{6,10}$", phone):
        return phone
    else:
        print("Invalid phone number. Please enter a valid phone number.")
        return None

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
