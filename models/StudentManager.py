from models.student import Student
from models.linked_list import DoubleLinkedList
from utils.data_loader import load_data, write_data
class StudentManager:
    def __init__(self):
        self.students = DoubleLinkedList()
    def load_students(self, file_path):
            students_data = load_data(file_path)
            for student_info in students_data:
                student = Student(
                    student_info["Full Name"],
                    student_info["Student ID"],
                    student_info["Date of Birth"],
                    student_info["Hometown"],
                    student_info["Phone Number"],
                    student_info["Major"],
                    student_info.get("Completed Courses", []),
                    student_info.get("Current Courses", [])
                )
                self.students.append(student)
    def add_student(self, full_name, student_id, dob, hometown, phone, major):
        """Create a new student object."""
        new_student = Student(full_name, student_id, dob, hometown, phone, major)
        self.students.append(new_student)
        return new_student

    def find_student(self, student_id):
        """Find a student by student_id."""
        current = self.students.head
        while current:
            if current.data.student_id == student_id:
                return current.data
            current = current.next
        return None

    def update_student(self, student_id, full_name=None, dob=None, hometown=None, phone=None, major=None):
        """Update the student's information."""
        student = self.find_student(student_id)
        if not student:
            return None
        if full_name:
            student.full_name = full_name
        if dob:
            student.dob = dob
        if hometown:
            student.hometown = hometown
        if phone:
            student.phone = phone
        if major:
            student.major = major
        return student

    def delete_student(self, student_id):
        """Delete the student from the list."""
        student = self.find_student(student_id)
        if not student:
            return None
        self.students.remove(student)
        return student

    def enroll_course(self, student_id, course_id, course_name):
        """Enroll the student in a new course."""
        student = self.find_student(student_id)
        if not student:
            return None
        student.enroll_course(course_id, course_name)
        return student

    def complete_course(self, student_id, course_id, grade):
        """Mark a course as completed."""
        student = self.find_student(student_id)
        if not student:
            return None
        student.complete_course(course_id, grade)
        return student

    def get_student_info(self, student_id):
        """Return a summary of the student's information."""
        student = self.find_student(student_id)
        if not student:
            return None
        return student.get_student_info()

    def get_all_students(self):
        """Return a list of all students."""
        students = []
        current = self.students.head
        while current:
            students.append(current.data)
            current = current.next
        return students
    def write_students(self, file_path):
            students_data = []
            current = self.students.head
            while current:
                student = current.data
                student_info = {
                    "Full Name": student.full_name,
                    "Student ID": student.student_id,
                    "Date of Birth": student.dob,
                    "Hometown": student.hometown,
                    "Phone Number": student.phone,
                    "Major": student.major,
                    "Completed Courses": student.completed_courses,
                    "Current Courses": student.current_courses
                }
                students_data.append(student_info)
                current = current.next

            write_data(file_path, students_data)