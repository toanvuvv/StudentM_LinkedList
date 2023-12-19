from utils.data_loader import load_data

class Course:
    def __init__(self, course_id, course_name, tuition_fee, description, major_id, credit):
        self.course_id = course_id
        self.course_name = course_name
        self.tuition_fee = tuition_fee
        self.description = description
        self.major_id = major_id
        self.credit = credit

    def get_course_info(self):
        return {
            "Course ID": self.course_id,
            "Course Name": self.course_name,
            "Tuition Fee": self.tuition_fee,
            "Description": self.description,
            "Major ID": self.major_id,
            "Credit": self.credit
        }

class CourseManager:
    def __init__(self):
        self.courses = []

    def load_courses(self, file_path):
        courses_data = load_data(file_path)
        for course_info in courses_data:
            course = Course(
                course_info["Course ID"],
                course_info["Course Name"],
                course_info["Tuition Fee"],
                course_info["Description"],
                course_info["Major ID"],
                course_info["Credit"]
            )
            self.courses.append(course)

    def get_course_info(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course.get_course_info()
        return None
    def get_course_credit(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course.credit
        return None  # or raise an exception if course not found