import datetime

#FUNC Calculate student year
def calculate_student_year(student_id):
    # Assuming the student ID is a string and the first two digits represent the year of enrollment
    enrollment_year = int(str(student_id)[:2])

    current_year = datetime.now().year % 100  # Get the last two digits of the current year

    # Calculate the academic year
    academic_year = current_year - enrollment_year + 1

    # Check if the academic year is valid
    if 1 <= academic_year <= 4:
        return academic_year
    else:
        return "Invalid or graduated"
#FUNC Calculate the GPA
def calculate_gpa(completed_courses, course_manager):
    if not completed_courses:
        return 0

    total_credits = 0
    total_score = 0

    for completed_course in completed_courses:
        course_id = completed_course["Course ID"]
        course_credit = course_manager.get_course_credit(course_id)
        course_score = completed_course["Grade"]

        total_credits += course_credit
        total_score += course_credit * course_score

    if total_credits == 0:
        return 0

    return round(total_score / total_credits, 2)


#FUNC Calculate tuition fee
def calculate_tuition_fee(student, course_manager):
    total_fee = 0

    # Iterate through the student's current courses
    for enrolled_course in student.current_courses:
        course_id = enrolled_course["Course ID"]
        course = course_manager.get_course_info(course_id)

        if course:
            # Calculate the fee for this course
            total_fee += course['Credit'] * course['Tuition Fee']
        else:
            print(f"Course with ID {course_id} not found in course database.")

    return total_fee

