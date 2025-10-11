import pytest
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestSQLInjection:
    def test_sql_injection_in_student_search(self, test_database):
        course_model = CourseModel(test_database)
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        student_model = StudentModel(test_database)
        
        malicious_input = "'; DROP TABLE students; --"
        results = student_model.search_students(malicious_input)
        
        assert isinstance(results, list)
        
        tables = test_database.fetchall("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        assert len(tables) == 1

    def test_sql_injection_in_course_search(self, test_database):
        course_model = CourseModel(test_database)
        
        malicious_input = "'; DELETE FROM courses; --"
        results = course_model.search_courses(malicious_input)
        
        assert isinstance(results, list)
        
        courses = course_model.get_all_courses()
        assert len(courses) == 0

    def test_parameterized_queries_working(self, test_database):
        course_model = CourseModel(test_database)
        course_model.add_course('TEST101', 'Test Course', 'Dr. Test', 3)
        student_model = StudentModel(test_database)
        student_model.add_student('S1234567', 'John', 'Doe', 'john@test.edu', 1)
        
        special_chars = "test' OR '1'='1"
        student_results = student_model.search_students(special_chars)
        course_results = course_model.search_courses(special_chars)
        
        assert len(student_results) == 0
        assert len(course_results) == 0
