import pytest
from model.course_model import CourseModel

class TestCourseWorkflow:
    def test_complete_course_lifecycle(self, test_database):
        course_model = CourseModel(test_database)
        
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        courses = course_model.get_all_courses()
        assert len(courses) == 1
        assert courses[0]['course_code'] == 'CS101'
        
        course_model.update_course(1, 'CS201', 'Advanced CS', 'Dr. Johnson', 4)
        
        updated_courses = course_model.get_all_courses()
        assert updated_courses[0]['course_name'] == 'Advanced CS'
        assert updated_courses[0]['credits'] == 4
        
        course_model.delete_course(1)
        final_courses = course_model.get_all_courses()
        assert len(final_courses) == 0

    def test_course_search_integration(self, test_database):
        course_model = CourseModel(test_database)
        
        course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        course_model.add_course('MATH101', 'Mathematics', 'Dr. Johnson', 4)
        course_model.add_course('PHY101', 'Physics', 'Dr. Brown', 3)
        
        science_courses = course_model.search_courses('Science')
        assert len(science_courses) == 1
        
        all_courses = course_model.search_courses('101')
        assert len(all_courses) == 3
