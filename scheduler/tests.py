from django.test import TestCase
from .person import *
from .course import *
from .checker import *
from .parser import *
# Create your tests here.
class AnalysisCompQualification(TestCase):
    temp = {}
    people = {}
    temp["aaron zhang"] = 12
    course = Course(521,  # Course number
                    1,  # Section
                    "MWF",
                    None,
                    "9:00AM",
                    "10:15AM",
                    "aaron zhang",
                    12,
                    temp,
                    None,
                    )
    courses = []
    courses.append(course)
    name = "aaron zhang"
    fullySupported = "no"
    supportingProfessor = None
    yearInSchool = 3
    pureOrApplied = "Pure"
    qualifyingExams = ["scientific comp"]
    teachingPrefs = ""
    labPrefs
    assistingPrefs
    person = Person(name, fullySupported, supportingProfessor, yearInSchool, pureOrApplied, qualifyingExams,
                    teachingPrefs, labPrefs, assistingPrefs, recitationPrefs, categoryPrefs, conflicts,
                    computerSkills, hoursCompleted, hoursBoughtOut)
    people.append(person)
