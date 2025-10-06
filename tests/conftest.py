import pytest
import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from db import Database

@pytest.fixture
def test_database():
    test_db = Database()
    test_db.conn = sqlite3.connect(':memory:')
    test_db.cursor = test_db.conn.cursor()
    test_db.conn.row_factory = sqlite3.Row
    test_db.setup()
    yield test_db
    test_db.close()

@pytest.fixture
def sample_course_data():
    return {
        'course_code': 'TEST101',
        'course_name': 'Test Course',
        'lecturer': 'Dr. Test',
        'credits': 3
    }

@pytest.fixture
def sample_student_data():
    return {
        'student_no': 'S1234567',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@student.edu'
    }

@pytest.fixture
def sample_enrollment_data():
    return {
        'student_no': 'S7654321',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@student.edu',
        'course_code': 'CS402',
        'course_name': 'Advanced Database Systems'
    }
