import pytest
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestStudentModel:
    def test_add_student_success(self, test_database, sample_student_data):
        course_model = CourseModel(test_database)
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        
        student_model = StudentModel(test_database)
        student_model.add_student(
            sample_student_data['student_no'],
            sample_student_data['first_name'],
            sample_student_data['last_name'],
            sample_student_data['email'],
            course_id=1
        )
        
        students = student_model.get_all_students()
        assert len(students) == 1
        assert students[0]['student_no'] == 'S1234567'

    def test_add_duplicate_student_fails(self, test_database):
        course_model = CourseModel(test_database)
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model = StudentModel(test_database)
        
        student_model.add_student('S1234567', 'John', 'Doe', 'john@test.edu', 1)
        
        with pytest.raises(Exception):
            student_model.add_student('S1234567', 'Jane', 'Smith', 'jane@test.edu', 1)

    def test_search_students(self, test_database):
        course_model = CourseModel(test_database)
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model = StudentModel(test_database)
        
        student_model.add_student('S1234567', 'John', 'Doe', 'john@test.edu', 1)
        
        results = student_model.search_students('John')
        assert len(results) == 1
        assert results[0]['student_no'] == 'S1234567'

    def test_delete_student(self, test_database):
        course_model = CourseModel(test_database)
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model = StudentModel(test_database)
        
        student_model.add_student('S1234567', 'John', 'Doe', 'john@test.edu', 1)
        student_model.delete_student(1)
        
        students = student_model.get_all_students()
        assert len(students) == 0

    def test_update_student(self, test_database):
        course_model = CourseModel(test_database)
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model = StudentModel(test_database)
        
        student_model.add_student('S1234567', 'John', 'Doe', 'john@test.edu', 1)
        student_model.update_student(1, 'S1234567', 'John', 'Smith', 'john.smith@test.edu', 1)
        
        students = student_model.get_all_students()
        assert students[0]['name'] == 'John Smith'
