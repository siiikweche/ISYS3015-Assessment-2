import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model.student_model import StudentModel
from model.course_model import CourseModel

def demonstrate_sql_injection():
    print(" DEMONSTRATING SQL INJECTION VULNERABILITIES")
    print("=" * 60)
    
    # Import our test database
    from tests.conftest import test_database
    
    # Setup
    db = test_database()
    student_model = StudentModel(db)
    course_model = CourseModel(db)
    
    print("\n TEST 1: SQL Injection in Student Search")
    print("-" * 40)
    
    # Test malicious inputs
    malicious_inputs = [
        "' OR '1'='1' --",
        "'; DROP TABLE students; --", 
        "test' OR 'x'='x",
        "xxx' UNION SELECT * FROM students --"
    ]
    
    for i, malicious_input in enumerate(malicious_inputs, 1):
        print(f"\n Attempt {i}: {malicious_input}")
        try:
            results = student_model.search_students(malicious_input)
            print(f"    Results returned: {len(results)} records")
            if len(results) > 0:
                print("   ❌ VULNERABILITY CONFIRMED: System returned data with malicious input!")
            else:
                print("    No data returned (safe)")
        except Exception as e:
            print(f"     System error: {e}")
    
    print("\n TEST 2: SQL Injection in Course Search") 
    print("-" * 40)
    
    for i, malicious_input in enumerate(malicious_inputs, 1):
        print(f"\n Attempt {i}: {malicious_input}")
        try:
            results = course_model.search_courses(malicious_input)
            print(f"    Results returned: {len(results)} courses") 
            if len(results) > 0:
                print("    VULNERABILITY CONFIRMED: System returned data with malicious input!")
            else:
                print("    No data returned (safe)")
        except Exception as e:
            print(f"    System error: {e}")
    
    print("\n" + "=" * 60)
    print("SQL Injection Testing Complete")

if __name__ == "__main__":
    demonstrate_sql_injection()