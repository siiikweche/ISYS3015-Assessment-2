import pytest
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestStudentWorkflow:
    def test_complete_student_lifecycle(self, test_database):
        course_model = CourseModel(test_database)
        student_model = StudentModel(test_database)
        
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model.add_student('S1234567', 'John', 'Doe', 'john.doe@student.edu', 1)
        
        students = student_model.get_all_students()
        assert len(students) == 1
        assert students[0]['name'] == 'John Doe'
        
        student_model.update_student(1, 'S1234567', 'John', 'Smith', 'john.smith@student.edu', 1)
        
        updated_students = student_model.get_all_students()
        assert updated_students[0]['name'] == 'John Smith'
        
        student_model.delete_student(1)
        final_students = student_model.get_all_students()
        assert len(final_students) == 0

    def test_student_search_integration(self, test_database):
        course_model = CourseModel(test_database)
        student_model = StudentModel(test_database)
        
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model.add_student('S1234567', 'John', 'Doe', 'john.doe@student.edu', 1)
        student_model.add_student('S7654321', 'Jane', 'Smith', 'jane.smith@student.edu', 1)
        
        search_results = student_model.search_students('John')
        assert len(search_results) == 1
        assert search_results[0]['student_no'] == 'S1234567'
        
        search_results = student_model.search_students('Smith')
        assert len(search_results) == 2
