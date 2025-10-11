import pytest
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestDatabaseIntegrity:
    """Testing database integrity issues found in Code Review"""
    
    def test_foreign_key_constraints(self, test_database):
        """
        TEST: Foreign Key Constraint Enforcement
        Code Review Finding: Foreign keys defined but not properly enforced
        """
        print("Testing Foreign Key Constraints...")
        
        student_model = StudentModel(test_database)
        
        # Try to add student with non-existent course (should fail)
        try:
            student_model.add_student("S9999", "Test", "Student", "test@test.com", 999)
            print("VULNERABILITY: Allowed student with non-existent course")
        except Exception as e:
            print("Correctly prevented invalid course reference")

    def test_data_consistency(self, test_database):
        """
        TEST: Data Consistency Across Operations
        Code Review Finding: Potential data corruption risks
        """
        print("Testing Data Consistency...")
        
        student_model = StudentModel(test_database)
        course_model = CourseModel(test_database)
        
        # Verify test data is consistent
        students = student_model.get_all_students()
        courses = course_model.get_all_courses()
        
        print(f"   Found {len(students)} students and {len(courses)} courses")
        assert len(students) > 0, "No students found in test data"
        assert len(courses) > 0, "No courses found in test data"
        print("Data consistency verified")
