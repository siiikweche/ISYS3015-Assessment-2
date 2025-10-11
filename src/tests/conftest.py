import pytest
import sqlite3
import os
import sys

# Adding project path to import application modules
print("Setting up Python path for module imports...")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDatabase:
    """Creating test database class that mimics our main Database class"""
    
    def __init__(self, db_path=":memory:"):
        # Using in-memory database for isolated testing
        print("Initializing in-memory test database...")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        print("Test database connection established successfully")
        
    def execute(self, query, params=()):
        """Executing SQL queries with parameter binding"""
        self.cursor.execute(query, params)
        self.conn.commit()
        
    def fetchall(self, query, params=()):
        """Fetching all results from database query"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
        
    def fetchone(self, query, params=()):
        """Fetching single result from database query"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
        
    def close(self):
        """Closing database connection"""
        print("Closing test database connection...")
        self.conn.close()

@pytest.fixture
def test_database():
    """
    FIXTURE: Creating isolated test database for each test
    Using in-memory database to avoid file system issues
    """
    print("Setting up test database fixture...")
    
    # Creating test database instance with in-memory storage
    db = TestDatabase()
    
    # Setting up test data structure matching our application
    setup_test_database(db)
    
    print("Test database fixture ready for testing")
    yield db  # Providing database to tests
    
    # Cleaning up after tests complete
    print("Cleaning up test database resources...")
    db.close()

def setup_test_database(db):
    """
    Setting up test data that matches our actual application structure
    This ensures our tests validate real application behavior
    """
    print("Creating test tables matching our application schema...")
    
    # Creating courses table matching our actual schema from db.py
    db.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE,
            course_name TEXT,
            lecturer TEXT,
            credits INTEGER
        )
    """)
    
    # Creating students table matching our actual schema from db.py
    db.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_no TEXT UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            course_id INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)
    
       # Inserting test course data for realistic testing scenarios
    print("Inserting test course data...")
    test_courses = [
        ("TEST101", "Test Programming", "Dr. Test", 3),  
        ("TEST201", "Test Mathematics", "Prof. Test", 4),
        ("TEST301", "Test Physics", "Dr. Test", 3)       
    ]
    
    for course_code, course_name, lecturer, credits in test_courses:
        db.execute(
            "INSERT OR IGNORE INTO courses (course_code, course_name, lecturer, credits) VALUES (?, ?, ?, ?)",
            (course_code, course_name, lecturer, credits)
        )
    
    # Inserting test student data for comprehensive testing
    print("Inserting test student data...")
    test_students = [
        ("S1001", "John", "Doe", "john.doe@email.com", 1),
        ("S1002", "Jane", "Smith", "jane.smith@email.com", 2),
        ("S1003", "Bob", "Johnson", "bob.johnson@email.com", 1)
    ]
    
    for student_no, first_name, last_name, email, course_id in test_students:
        db.execute(
            "INSERT OR IGNORE INTO students (student_no, first_name, last_name, email, course_id) VALUES (?, ?, ?, ?, ?)",
            (student_no, first_name, last_name, email, course_id)
        )
    
    print("Test database setup completed with sample data")

@pytest.fixture
def sample_course_data():
    """Creating sample course data for testing"""
    return {
        'course_code': 'TEST101',
        'course_name': 'Test Course',
        'lecturer': 'Dr. Test', 
        'credits': 3
    }

@pytest.fixture  
def sample_student_data():
    """Creating sample student data for testing"""
    return {
        'student_no': 'S1234567',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@student.edu'
    }