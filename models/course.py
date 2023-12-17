from utils.data_loader import load_data
class Course:
    def __init__(self, course_id, course_name, tuition_fee, description, major_id):
        self.course_id = course_id
        self.course_name = course_name
        self.tuition_fee = tuition_fee
        self.description = description
        self.major_id = major_id

    def get_course_info(self):
        return {
            "Course ID": self.course_id,
            "Course Name": self.course_name,
            "Tuition Fee": self.tuition_fee,
            "Description": self.description,
            "Major ID": self.major_id
        }
    
    
    # load data from json file
def load_courses_from_json(file_path):
    courses_data = load_data(file_path)
    courses = []
    for course_info in courses_data:
        course = Course(course_info["Course ID"], course_info["Course Name"], course_info["Description"], course_info["Tuition Fee"])
        courses.append(course)
    return courses