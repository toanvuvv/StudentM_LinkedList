class Student:
    def __init__(self, full_name, student_id, dob, hometown, phone, major):
        self.full_name = full_name
        self.student_id = student_id
        self.dob = dob
        self.hometown = hometown
        self.phone = phone
        self.major = major
        self.completed_courses = []  # Danh sách các khóa học đã hoàn thành
        self.current_courses = []    # Danh sách các khóa học hiện tại
    def update_phone(self, new_phone):
        self.phone = new_phone

    def update_major(self, new_major):
        self.major = new_major

    # Các phương thức khác để cập nhật thông tin cá nhân
    def enroll_course(self, course_id, course_name):
        self.current_courses.append({"Course ID": course_id, "Course Name": course_name})

    def complete_course(self, course_id, grade):
        course = next((c for c in self.current_courses if c["Course ID"] == course_id), None)
        if course:
            course["Grade"] = grade
            self.completed_courses.append(course)
            self.current_courses.remove(course)
    def get_student_info(self):
        return {
            "Full Name": self.full_name,
            "Student ID": self.student_id,
            "Date of Birth": self.dob,
            "Hometown": self.hometown,
            "Phone Number": self.phone,
            "Major": self.major,
            "Completed Courses": self.completed_courses,
            "Current Courses": self.current_courses
        }
