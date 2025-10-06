import pytest
import sqlite3
from db import Database

class TestDatabase:
    def test_database_connection(self, test_database):
        assert test_database.conn is not None
        assert test_database.cursor is not None

    def test_tables_created(self, test_database):
        test_database.cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND (name='students' OR name='courses')
        """)
        tables = test_database.cursor.fetchall()
        table_names = [table[0] for table in tables]
        assert 'students' in table_names
        assert 'courses' in table_names

    def test_foreign_key_constraints(self, test_database):
        test_database.cursor.execute("PRAGMA foreign_keys")
        result = test_database.cursor.fetchone()
        assert result[0] == 1

    def test_execute_query(self, test_database):
        test_database.execute("INSERT INTO courses (course_code, course_name, lecturer, credits) VALUES (?, ?, ?, ?)", 
                            ('CS101', 'Computer Science', 'Dr. Smith', 3))
        
        rows = test_database.fetchall("SELECT * FROM courses WHERE course_code = ?", ('CS101',))
        assert len(rows) == 1
        assert rows[0]['course_name'] == 'Computer Science'

    def test_fetchone_method(self, test_database):
        test_database.execute("INSERT INTO courses (course_code, course_name, lecturer, credits) VALUES (?, ?, ?, ?)", 
                            ('MATH101', 'Mathematics', 'Dr. Johnson', 4))
        
        row = test_database.fetchone("SELECT * FROM courses WHERE course_code = ?", ('MATH101',))
        assert row is not None
        assert row['lecturer'] == 'Dr. Johnson'

    def test_database_close(self, test_database):
        test_database.close()
        with pytest.raises(sqlite3.ProgrammingError):
            test_database.cursor.execute("SELECT 1")
