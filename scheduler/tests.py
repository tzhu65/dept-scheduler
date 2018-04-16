from django.test import TestCase
from .person import *
from .course import *
from .checker import *
from .parser import *
# Create your tests here.
class AnalysisCompQualification(TestCase):
    "Test to see if individuals analysis comp constraint is functioning"
    FACULTY_HOURS = "scheduler/static/data/faculty_hours/faculty_hours_April8.csv"
    PREFERENCES =  "scheduler/static/data/preferences/Test/analysis_comp_test_pref.cvs"
    SCHEDULE = "scheduler/static/data/schedule/Test/analysis_comp_test_schedule.csv"

    schedule = parseCoursesFromPath(SCHEDULE)
    preferences = parsePeopleFromPath(PREFERENCES)
    facultyHours = parseFacultyHoursFromPath(FACULTY_HOURS)

    check(courses, people, facultyHours[0])
