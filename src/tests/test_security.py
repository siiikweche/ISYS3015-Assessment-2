import pytest
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestSecurity:
    """Testing the security vulnerabilities identified in Code Review"""
    
    def test_sql_injection_student_search(self, test_database):
        """
        TEST: SQL Injection in Student Search
        Code Review Finding: student_model.py - String interpolation in SQL queries
        This test proves the vulnerability you documented in your Code Review!
        """
        print("Testing SQL Injection in Student Search...")
        
        student_model = StudentModel(test_database)
        
        # MALICIOUS INPUTS that exploit the vulnerability
        sql_injection_attempts = [
            "' OR '1'='1' --",           # Basic SQL injection - should return ALL students
            "'; DROP TABLE students; --", # Destructive SQL injection
            "test' OR 'x'='x",           # Boolean-based injection
            "xxx' UNION SELECT * FROM students --", # Union-based injection
        ]
        
        for malicious_input in sql_injection_attempts:
            print(f"   Testing: {malicious_input}")
            try:
                # This calls YOUR actual search_students method
                results = student_model.search_students(malicious_input)
                
                # If we get results with malicious input, it's a VULNERABILITY
                if results and len(results) > 0:
                    print(f"   VULNERABILITY CONFIRMED: Returned {len(results)} records")
                    print(f"   This proves the SQL injection vulnerability from your Code Review!")
                else:
                    print(f"   No results returned (safe)")
                    
            except Exception as e:
                print(f"     System error: {e}")

    def test_sql_injection_course_search(self, test_database):
        """
        TEST: SQL Injection in Course Search  
        Code Review Finding: course_model.py - Same vulnerability pattern
        """
        print(" Testing SQL Injection in Course Search...")
        
        course_model = CourseModel(test_database)
        
        malicious_inputs = [
            "' OR '1'='1' --",
            "'; DELETE FROM courses; --",
            "xxx' UNION SELECT * FROM courses --"
        ]
        
        for malicious_input in malicious_inputs:
            print(f"   Testing: {malicious_input}")
            try:
                results = course_model.search_courses(malicious_input)
                
                if results and len(results) > 0:
                    print(f"   VULNERABILITY CONFIRMED: Returned {len(results)} courses")
                    print(f"   This proves the SQL injection vulnerability from your Code Review!")
                else:
                    print(f"   No results returned (safe)")
                    
            except Exception as e:
                print(f"     Course search error: {e}")

    def test_input_validation_gaps(self, test_database):
        """
        TEST: Missing Input Validation
        Code Review Finding: Views lack comprehensive server-side validation
        """
        print(" Testing Input Validation Gaps...")
        
        student_model = StudentModel(test_database)
        
        # Test inputs that should be validated but might not be
        problematic_inputs = [
            "",  # Empty input
            "   ",  # Whitespace only
            "<script>alert('xss')</script>",  # XSS attempt
            "very_long_input_" * 100,  # Buffer overflow attempt
        ]
        
        for bad_input in problematic_inputs:
            try:
                results = student_model.search_students(bad_input)
                if results is not None:
                    print(f"  No validation for: '{bad_input[:20]}...'")
                else:
                    print(f"Handled input safely: '{bad_input[:20]}...'")
            except Exception as e:
                print(f"System rejected invalid input: {e}")