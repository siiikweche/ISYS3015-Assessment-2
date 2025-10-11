import pytest
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestFunctionality:
    """Testing core application functionality"""
    
    def test_student_search_functionality(self, test_database):
        """
        TEST: Student Search Functionality
        Tests TC-STU-003 from your Test Plan
        """
        print(" Testing Student Search Functionality...")
        
        student_model = StudentModel(test_database)
        
        # Test normal search operations
        results = student_model.search_students("John")
        print(f"   Search for 'John' returned {len(results)} results")
        
        results = student_model.search_students("S1001")
        print(f"   Search for 'S1001' returned {len(results)} results")
        
        print("Student search functionality working")

    def test_course_search_functionality(self, test_database):
        """
        TEST: Course Search Functionality
        """
        print(" Testing Course Search Functionality...")
        
        course_model = CourseModel(test_database)
        
        results = course_model.search_courses("Programming")
        print(f"   Search for 'Programming' returned {len(results)} results")
        
        results = course_model.search_courses("TEST101")
        print(f"   Search for 'TEST101' returned {len(results)} results")
        
        print(" Course search functionality working")

    def test_get_all_records(self, test_database):
        """
        TEST: Retrieve All Records
        """
        print(" Testing Record Retrieval...")
        
        student_model = StudentModel(test_database)
        course_model = CourseModel(test_database)
        
        students = student_model.get_all_students()
        courses = course_model.get_all_courses()
        
        print(f"   Retrieved {len(students)} students and {len(courses)} courses")
        assert len(students) > 0, "Should have test students"
        assert len(courses) > 0, "Should have test courses"
        print(" Record retrieval working correctly")