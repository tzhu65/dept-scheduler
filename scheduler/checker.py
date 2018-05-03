"""Schedule checker.

Currently checking for:
    - Qualified computer skills
    - Passed qualifying exams
    - Conflicting times
    - MWF/TR conflicts
    - Preferences

Functions prefixed with `validate` check for hard requirements, and functions
prefixed with `check` check for soft requirements.
"""

import typing

from .checkerConstants import *
from .course import Course
from .person import Person


# ================ #
# Helper Functions #
# ================ #

def printError(person: Person, course: Course, message: str) -> None:
    """
    Print an error related to a person and course.
    :param person: The person related to the error or conflict.
    :param course: The course related to the error or conflict.
    :param message: Description of the error.
    :return: None
    """
    print("ERR: %s, %s. %s" % (person.name, course.courseNumber, message))


def appendError(person: Person, course: Course, message: str, errors: typing.List[str]) -> None:
    """
    Add an error related to a person and course to a list of errors.
    :param person: The person related to the error or conflict.
    :param course: The course related to the error or conflict.
    :param message: Description of the error.
    :param errors: List of errors that will have the new error message appended to it.
    :return: None
    """
    errors.append("ERR: %s, %s. %s" % (person.name, course.courseNumber, message))


def appendErrorNoCourse(person: Person, message: str, errors: typing.List[str]) -> None:
    """
    Add an error related to a person to a list of errors.
    :param person: The person related to the error or conflict.
    :param message: Description of the error.
    :param errors: List of errors that will have the new error message appended to it.
    :return: None
    """
    errors.append("ERR: %s. %s" % (person.name, message))


def checkTimeOverlap(courseA: Course, courseB: Course) -> bool:
    """
    Check if there are time overlaps between two courses.
    :param courseA:
    :param courseB:
    :return: True if there is a time conflict.
    """
    latestStart = max(courseA.startTime, courseB.startTime)
    earliestEnd = min(courseA.endTime, courseB.endTime)
    return earliestEnd > latestStart


# ========== #
# Validators #
# ========== #

def validateComputerSkill(person: Person, course: Course, errors: typing.List[str]) -> bool:
    """
    Validate that a person has the necessary computer skills to teach a class.
    :param person: The person expected to the teach the course.
    :param course: Course object.
    :param errors: List of errors to keep track of.
    :return: True if the person is qualified to teach the course.
    """
    # If course is not a lab, then return true because comp skills not needed
    if course.courseNumber[-1:] == 'L':

        # If insufficient computer skill
        if int(person.computerSkills) < 3:
            appendError(person,
                        course,
                        "Instructor has computer skill: %s. Course requires computer skill: 3" % person.computerSkills,
                        errors)
            return False
        else:
            return True
    else:
        return True


def validateQualifyingExam(person: Person, course: Course, errors: typing.List[str]) -> bool:
    """
    Validate that a person passed the necessary qualifying exams to teach a class.
    :param person: The person expected to teach the course.
    :param course: Course object.
    :param errors: List of errors for bookkeeping.
    :return: True if the person is qualified to teach the course.
    """
    # If no qualifying exams return true
    if course.courseNumber not in qualifyingExams:
        return True

    # If qualifying exam not fulfilled
    if qualifyingExams[course.courseNumber] not in person.qualifyingExams:
        appendError(person,
                    course,
                    "Instructor is missing required qualifying exam: %s" % qualifyingExams[course.courseNumber],
                    errors)
        return False
    else:
        return True



def validateHoursConstraint(person: Person, course: Course, errors: typing.List[str]) -> bool:
    """
    Validate that a person has enough hours remaining to teach a class. Used in the schedule checker.
    :param person: Person object.
    :param course: Course object.
    :param errors: List of errors for bookkeeping.
    :return: True if the person has enough hours remaining to teach a class.
    """
    courseHoursValue = course.hoursValue
    avaliableHours = person.availableHours() - courseHoursValue
    if avaliableHours < 0:
        # Error
        appendError(person, course, "Instructor has passed their allowed hours for this semester", errors)
        return False
    else:
        return True


def validateSchedulerHoursConstraint(person: Person, course: Course, errors: typing.List[str]) -> bool:
    """
    Validate that a person has enough hours remaining to teach a class. Used in the schedule generator.
    :param person: Person object.
    :param course: Course object.
    :param errors: List of errors for bookkeeping.
    :return: True if the person has enough hours remaining to teach a class.
    """
    courseHoursValue = course.hoursValue
    availableHours = person.availableHours() - courseHoursValue
    return availableHours >= 0


def validateClassTimes(person, course, courses, errors):
    """
    Validate that assigning a person to a class would not create conflicts with other classes the person is assigned to.
    :param person: Person object.
    :param course: Course to test.
    :param courses: List of courses the person is assigned to.
    :param errors: List of errors for bookkeeping.
    :return: True if there are no time conflicts.
    """
    for c in courses:
        if bool(set(course.days) & set(c.days)):    # Check if the days have overlap
            if checkTimeOverlap(course, c):
                appendError(person, course, "Course has a time conflict with the another course: %s-%s" % \
                            (c.courseNumber, c.section), errors)
                return False

        # Check for overlap with the person's conflicts
        for conflict in person.conflicts:
            if conflict.day in set(c.days):
                if checkTimeOverlap(conflict, c):
                    appendError(person, course, "Course time conflicts with personal conflicts: %s-%s" % \
                                (c.courseNumber, c.section), errors)
                    return False
    return True


# ======== #
# Checkers #
# ======== #

def checkIfClassIsPreferredClass(person: Person, course: Course, errors: typing.List[str]) -> bool:
    """
    Check that a course is one of the person's preferred classes.
    :param person: Person object.
    :param course: Course object.
    :param errors: List of errors for bookkeeping.
    :return: True if the class is one of the person's preferred class.
    """
    hoursVal = course.instructorToHoursVal[person.name]
    if hoursVal == 12:
        # Teaching
        if not any(course.courseNumber in val for val in person.teachingPrefs):
            appendError(person, course, "Instructor did not list course as one of their teaching preferences", errors)
            return False
    elif hoursVal == 3:
        # Recitation
        if not any(course.courseNumber in val for val in person.recitationPrefs):
            appendError(person, course, "Instructor did not list course as one of their recitation preferences", errors)
            return False
    elif hoursVal == 6 and ('L' in course.courseNumber):
        # Lab
        if not any(course.courseNumber in val for val in person.labPrefs):
            appendError(person, course, "Instructor did not list course as one of their lab preferences", errors)
            return False
    elif hoursVal == 6:
        # Assist
        if not any(course.courseNumber in val for val in person.assistingPrefs):
            appendError(person, course, "Instructor did not list course as one of their assisting preferences", errors)
            return False
    return True


def checkClassDaysOfTheWeek(person: Person, course: Course, courses: typing.List[Course], errors: typing.List[str]) \
        -> bool:
    """
    Check to make sure that a person doesn't have classes on both MWF and TR.
    :param person: Person object.
    :param course: Course object to check against.
    :param courses: List of courses that the person is currently assigned to.
    :param errors: List of errors for bookkeeping.
    :return: True if the person does not have any classes on both MWF and TR.
    """
    mwf = ['M', 'W', 'F']
    tr = ['T', 'R']
    teachingDays = set(course.days)
    for c in courses:
        teachingDays = teachingDays.union(set(c.days))

    # Check if there's overlap in both MWF and TR
    if bool(set(mwf) & teachingDays) and bool(set(tr) & teachingDays):
        appendError(person, course, "Cannot teach on both MWF and TR", errors) # TODO: say which classes they are
        return False
    return True


def checkFacultyHours(courses: typing.List[Course], facultyHours: typing.Dict[str, int], errors: typing.List[str]) \
        -> bool:
    """
    Validate that all faculty have the correct number of hours assigned.
    :param courses: List of all the courses.
    :param facultyHours: Dictionary mapping the faculty member's name to the hours.
    :param errors: List of errors for bookkeeping.
    :return: True if all faculty are correctly assigned.
    """
    # Faculty correct course check
    correctlyAssigned = True
    for faculty in facultyHours:
        courseCount = 0
        for course in courses:
            if course.instructor == faculty:
                courseCount += 1
        if courseCount != int(facultyHours[faculty]):
            errors.append("ERROR %s is NOT enrolled in correct number of courses, enrolled: %s, expected: %s" % (faculty, courseCount, facultyHours[faculty]))
            correctlyAssigned = False
    return correctlyAssigned


# ============== #
# Validate/Check #
# ============== #

def validate(person: Person, course: Course, personCourses: typing.Dict[str, Course], errors: typing.List[str]) -> bool:
    """
    Validate that a person can teach a course. This includes ensuring sufficient computer skills, qualification exams,
    the class is one of the person's preferences, and that the class makes it stick to either a MWF or TR schedule.
    :param person: Person object.
    :param course: Course to validate for.
    :param personCourses: The other courses the person is teaching.
    :param errors: List of errors for bookkeeping.
    :return: True if the person can teach the course.
    """
    return \
        validateClassTimes(person, course, personCourses.get(person.name, []), errors) and \
        checkClassDaysOfTheWeek(person, course, personCourses.get(person.name, []), errors) and \
        validateComputerSkill(person, course, errors) and validateQualifyingExam(person, course, errors) and \
        checkIfClassIsPreferredClass(person, course, errors) and \
        validateHoursConstraint(person, course, errors)


def checkIfAssignmentsAreValid(people: typing.List[Person], courses: typing.List[Course],
                               facultyHours: typing.Dict[str, int], errors: typing.List[str]) -> None:
    """
    Check that all the assigned instructors were passed in as people or faculty.
    :param people: List of all the people (graduate students).
    :param courses: List of all the courses.
    :param facultyHours: Map of the names of the faculty to their respective hours.
    :param errors: List of errors for bookkeeping.
    :return: None
    """
    # Addition for linda
    peopleList = {}
    for person in people:
        peopleList[person.name] = 1

    for course in courses:
        if course.instructor not in facultyHours and course.instructor not in peopleList:
            errors.append("ERR: %s is assigned to a course but not on the list of faculty or graduate students" %
                          course.instructor)


def check(courses: typing.List[Course], people: typing.List[Person], facultyHours: typing.Dict[str, int]) \
        -> typing.List[str]:
    """
    Check for all errors given a schedule.
    :param courses: List of all the courses.
    :param people: List of all the people (graduate students).
    :param facultyHours: Mapping of faculty names to their respective hours.
    :return: List of errors.
    """

    # Make set of courseNames that will be used to ensure every course is assigned
    courseNames = set([course.courseNumber for course in courses])
    print("START: " + str(courseNames))
    personCourses = {}      # Dict of mapping a person to their courses
    errors = []     # List of errors

    checkFacultyHours(courses, facultyHours, errors)
    checkIfAssignmentsAreValid(people, courses, facultyHours, errors)

    for person in people:
        for course in courses:
            # Found a course that person is teaching
            if person.name in course.instructorToHoursVal:
                # If course is valid remove it from the coursenameList
                if validate(person, course, personCourses, errors):
                    # We need course list to be empty at end, so if course is assigned correctly, remove it from list
                    try:
                        courseNames.remove(course.courseNumber)
                    except KeyError:
                        continue
                c = personCourses.get(person.name, [])
                c.append(course)
                personCourses[person.name] = c
    for course in courses:
        if course.instructor in facultyHours:
            try:
                courseNames.remove(course.courseNumber)
            except KeyError:
                continue

    print(errors)
    return errors
