from .checkerConstants import *
from .parser import sanitizeName
import string

def printError(person, course, message):
    print("ERR: %s, %s. %s" % (person.name, course.courseNumber, message))


def appendError(person, course, message, errors):
    errors.append("ERR: %s, %s. %s" % (person.name, course.courseNumber, message))

def appendErrorNoCourse(person, message, errors):
    errors.append("ERR: %s. %s" % (person.name, message))

def validateComputerSkill(person, course, errors):
    # if course is not a lab then return true cuz comp skills not needed
    if course.courseNumber[-1:] == 'L':
        # If insufficient computer skill
        if (int(person.computerSkills) < 3):
            appendError(person, course,
                "Instructor has computer skill: %s. Course requires computer skill: 3" % person.computerSkills, errors)
            return False
        else:
            return True
    else:
        return True


def validateQualifyingExam(person, course, errors):
    # if no qualifying exams return true
    if course.courseNumber not in qualifyingExams:
        return True
        # If qualifying exam not fulfilled
    if qualifyingExams[course.courseNumber] not in person.qualifyingExams:
        appendError(person, course, "Instructor is missing required qualifying exam: %s" % qualifyingExams[course.courseNumber], errors)
        return False
    else:
        return True


def checkIfClassIsPreferredClass(person, course, errors):
    hoursVal = course.instructorToHoursVal[person.name]
    if hoursVal==12:
        #TEACHING
        if not any(course.courseNumber in val for val in person.teachingPrefs):
            appendError(person, course, "Instructor did not list course as one of their teaching preferences", errors)
            return False
    elif hoursVal==3:
        #Recitation
        if not any(course.courseNumber in val for val in person.recitationPrefs):
            appendError(person, course, "Instructor did not list course as one of their recitation preferences", errors)
            return False
    elif hoursVal==6 and ('L' in course.courseNumber):
        #Lab
        if not any(course.courseNumber in val for val in person.labPrefs):
            appendError(person, course, "Instructor did not list course as one of their lab preferences", errors)
            return False
    elif hoursVal==6:
        #Assist
        if not any(course.courseNumber in val for val in person.assistingPrefs):
            appendError(person, course, "Instructor did not list course as one of their assisting preferences", errors)
            return False
    return True


def checkHoursConstraint(person, course, errors):
    courseHoursValue = course.hoursValue
    avaliableHours = MAX_HOURS-person.hoursCompleted-person.hoursBoughtOut-courseHoursValue
    if avaliableHours < 0:
        #error
        appendError(person,course,"Instructor has passed their allowed hours for this semester", errors)
        return False
    else:
        return True
        print("%s is enrolled in the proper number of hours, he has %i remaining" % (person.name,person.hoursCompleted))
        person.hoursCompleted = person.hoursCompleted - courseHoursValue

def checkSchedulerHoursConstraint(person, course, errors):
    courseHoursValue = course.hoursValue
    availableHours = MAX_HOURS - person.hoursCompleted - person.hoursBoughtOut - courseHoursValue
    return availableHours >= 0


def checkSchedulerHoursConstraint(person, course, errors):
    courseHoursValue = course.hoursValue#instructorToHoursVal[person.name]
    avaliableHours = MAX_HOURS-person.hoursCompleted-person.hoursBoughtOut-courseHoursValue
    if avaliableHours < 0:
        #error
        appendError(person,course,"Instructor has passed their allowed hours for this semester", errors)
        return False
    else:
        return True
        print("%s is enrolled in the proper number of hours, he has %i remaining" % (person.name,person.hoursCompleted))
        person.hoursCompleted = person.hoursCompleted - courseHoursValue


# Check to make sure that no person has classes on MWF and TR
def checkClassDaysOfTheWeek(person, course, courses, errors):
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


def checkClassTimes(person, course, courses, errors):
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

def checkFacultyHours(courses, facultyHours, errors):
     #Faculty correct course check
    for faculty in facultyHours:
        courseCount = 0
        for course in courses:
            if course.instructor == faculty:
                courseCount += 1
        if courseCount != int(facultyHours[faculty]):
            errors.append("ERROR %s is NOT enrolled in correct number of courses, enrolled: %s, expected: %s" % (faculty, courseCount, facultyHours[faculty]))


def checkTimeOverlap(courseA, courseB):
    latestStart = max(courseA.startTime, courseB.startTime)
    earliestEnd = min(courseA.endTime, courseB.endTime)
    return earliestEnd > latestStart    # Returns true if their is a time conflict


def validate(person, course, personCourses, errors):
    # Ensure sufficient computer skills
    # Ensure sufficient qualification exams passed
    # Ensure course is one of person's preferences
    # Ensure either M/W/F or T/Th schedule
    return \
        checkClassTimes(person, course, personCourses.get(person.name, []), errors) and \
        checkClassDaysOfTheWeek(person, course, personCourses.get(person.name, []), errors) and \
        validateComputerSkill(person, course, errors) and validateQualifyingExam(person, course, errors) and \
        checkIfClassIsPreferredClass(person, course, errors) and \
        checkHoursConstraint(person, course, errors)

def checkIfAssignmentsAreValid(people, courses, facultyHours,errors):
    #addition for linda
    peopleList = {}
    for person in people:
        peopleList[person.name] = 1

    for course in courses:
        if course.instructor not in facultyHours and course.instructor not in peopleList:
            errors.append("ERR: %s is assigned to a course but not on the list of faculty or graduate students" % course.instructor)

def check(courses, people, facultyHours):
    # Make set of courseNames that will be used to ensure every course is assigned
    courseNames = set([course.courseNumber for course in courses])
    print("START: " + str(courseNames))
    personCourses = {}      # Dict of mapping a person to their courses
    errors = []     # List of errors


    checkFacultyHours(courses, facultyHours, errors)
    checkIfAssignmentsAreValid(people,courses,facultyHours,errors)

    for person in people:
        for course in courses:
            # Found a course that person is teaching
            if (person.name in course.instructorToHoursVal):
                # if course is valid remove it from the coursenameList
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

    #print("Invalid courses are: " + str(courseNames) +"\n")
    #print (facultyHours)
    #print (peopleList)
    print(errors)
    return errors
