from .checkerConstants import *
import string

def printError(person, course, message):
    print("ERR: %s, %s. %s" % (person.name, course.cse, message))


def validateComputerSkill(person, course):
    # if course is not a lab then return true cuz comp skills notneeded
    if course.cse[-1:] == 'L':
        # If insufficient computer skill
        if (int(person.computerSkills) < 3):
            printError(person, course, 
                "Instructor has computer skill: %s. Course requires computer skill: 3" % person.computerSkills)
            return False
        else:
            return True
    else:
        return True


def validateQualifyingExam(person, course):
    # if no qualifying exams return true
    if course.cse not in qualifyingExams:
        return True
        # If qualifying exam not fulfilled
    if qualifyingExams[course.cse] not in person.qualifyingExams:
        printError(person, course, "Instructor is missing required qualifying exam: %s" % qualifyingExams[course.cse])
        return False
    else:
        return True


def checkIfClassIsPrefferedClass(person, course):
    if not any(course.cse in val for val in person.teachPrefs.values()):
        printError(person, course, "Instructor did not list course as one of their preferences")
        return False
    else:
        return True


def validate(person, course):
    # Ensure sufficient computer skills
    # Ensure sufficient qualification exams passed
    # Ensure course is one of person's preferences
    return validateComputerSkill(person, course) and validateQualifyingExam(person, course) and checkIfClassIsPrefferedClass(person, course)
    # NEED TO IMPLEMENT
    # 600-level courses must have passed appropriate COMP
    # if int(course.cse.strip(string.ascii_letters)) >= 600:
    # Have to be on T/Th or M/W/F schedule, no in-between


def check(courses, people):
    # Make set of courseNames that will be used to ensure every course is assigned
    courseNames = set([course.cse for course in courses])
    print("START: " + str(courseNames))

    for person in people:
        for course in courses:
            # Found a course that person is teaching
            if person.name == course.instructor:
                # if course is valid remove it from the coursenameList
                if validate(person, course):
                    # We need course list to be empty at end, so if course is assigned correctly, remove it from list
                    try:
                        courseNames.remove(course.cse)
                    except KeyError:
                        continue

    print("Invalid courses are: " + str(courseNames))