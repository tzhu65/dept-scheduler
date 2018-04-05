from .checkerConstants import *
import string

def printError(person, course, message):
    print("ERR: %s, %s. %s" % (person.name, course.courseNumber, message))


def appendError(person, course, message, errors):
    errors.append("ERR: %s, %s. %s" % (person.name, course.courseNumber, message))


def validateComputerSkill(person, course, errors):
    # if course is not a lab then return true cuz comp skills not needed
    if course.courseNumber[-1:] == 'L':
        # If insufficient computer skill
        if (int(person.computerSkills) < 3):
            printError(person, course,
                "Instructor has computer skill: %s. Course requires computer skill: 3" % person.computerSkills)
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
        printError(person, course, "Instructor is missing required qualifying exam: %s" % qualifyingExams[course.courseNumber])
        appendError(person, course, "Instructor is missing required qualifying exam: %s" % qualifyingExams[course.courseNumber], errors)
        return False
    else:
        return True


def checkIfClassIsPreferredClass(person, course, errors):
    if not any(course.courseNumber in val for val in person.teachPrefs.values()):
        printError(person, course, "Instructor did not list course as one of their preferences")
        appendError(person, course, "Instructor did not list course as one of their preferences", errors)
        return False
    else:
        return True

def checkHoursConstraint(person, course, errors):
    print("GET HERE!_@#!@$@#$!#$")
    avaliableHours = 30-person.hoursCompleted-course.hoursValue
    if avaliableHours < 0:
        #error
        printError(person,course,"Instructor has passed their allowed hours for this semester")
        appendError(person,course,"Instructor has passed their allowed hours for this semester", errors)
        return False
    else:
        return True
        print("%s is enrolled in the proper number of hours, he has %i remaining" % (person.name,person.hoursCompleted))



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
    return True

def checkFacultyHours(courses, facultyHours, errors):
    #Faculty correct course check
    for faculty in facultyHours:
        courseCount = 0
        for course in courses:
            if course.instructor.lower() == faculty.lower():
                courseCount+=1
        if courseCount == int(facultyHours[faculty]):
            #Expected Nothing is wrong
            print("%s is enrolled in correct number of courses, enrolled: %s, expected: %s" % (faculty, facultyHours[faculty], courseCount))
        else:
            #error
            print("ERROR %s is NOT enrolled in correct number of courses, enrolled: %s, expected: %s" % (faculty, facultyHours[faculty], courseCount))


def checkTimeOverlap(courseA, courseB):
    latestStart = max(courseA.startTime, courseB.startTime)
    earliestEnd = min(courseA.endTime, courseB.endTime)
    return earliestEnd > latestStart    # Returns true if their is a time conflict


def validate(person, course, personCourses, errors):
    print("Performing validations")
    # Ensure sufficient computer skills
    # Ensure sufficient qualification exams passed
    # Ensure course is one of person's preferences
    # Ensure either M/W/F or T/Th schedule
    return \
        checkClassTimes(person, course, personCourses.get(person.name, []), errors) and \
        checkClassDaysOfTheWeek(person, course, personCourses.get(person.name, []), errors) and \
        validateComputerSkill(person, course, errors) and validateQualifyingExam(person, course, errors) and \
        checkIfClassIsPreferredClass(person, course, errors) and \
        checkHoursConstraint(person,course,errors)


def check(courses, people, facultyHours):
    # Make set of courseNames that will be used to ensure every course is assigned
    courseNames = set([course.courseNumber for course in courses])
    print("START: " + str(courseNames))
    personCourses = {}      # Dict of mapping a person to their courses
    errors = []     # List of errors

    checkFacultyHours(courses, facultyHours, errors)

    for person in people:
        for course in courses:
            # Found a course that person is teaching
            if person.name == course.instructor:
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

    print("Invalid courses are: " + str(courseNames))
    print(errors)

    # print(courses, people)
