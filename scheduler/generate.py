"""Schedule generator."""

import copy
import csv
import typing

from .course import Course
from .graph import Graph, WeightAssigner
from .person import Person


def generateAllCourses(courses: typing.List[Course]) -> typing.List[Course]:
    """
    Generate all course nodes from the parsed courses.

    This function goes through all available positions in a course, and generates new courses for them. This way the
    algorithm can generate an assignment for all available positions of a course.
    :param courses: List of all the courses.
    :return: List of all the courses, where each course represents an available position.
    """

    coursesCopy = []

    # Generate all the course nodes
    for c in courses:

        # Calculate the total number of open positions
        availablePositions = 0
        for t in c.positions:
            availablePositions += c.positions[t]["amount"]

        for t in c.positions:

            # Skip if it's a teach node and the instructor is set
            if t == "teach" and c.instructor != "":
                continue

            # Skip if the amount needed is only 1 and the instructor is already set or assistants are set
            if availablePositions == 1 and c.instructor != "":
                continue

            for i in range(c.positions[t]["amount"]):

                # Check the number of assistants
                if t == "assist" and i < len(c.assistants):
                    continue
                            
                # Deep copy this node and set the category
                course = copy.deepcopy(c)
                course.positions = {t: {"amount": 1, "hours": c.positions[t]["hours"]}}
                course.category = t
                course.hoursValue = c.positions[t]["hours"]
                course.instructor = ""
                course.assistants = []
                if not isinstance(course.hoursValue, int):
                    course.hoursValue = 0
                coursesCopy.append(course)
    return coursesCopy


def generate(courses: typing.List[Course], people: typing.List[Person], faculty: typing.Dict[str, int]):
    """
    Generate a schedule.
    :param courses: List of all the courses.
    :param people: List of all the people.
    :param faculty: Mapping of the faculty names to their respective hours.
    :return: The path to the final csv, and a mapping of the people to the courses.
    """

    # Keep looping until all courses are matched or no more people can be matched
    peopleCopy = [copy.deepcopy(p) for p in people]
    newPeopleCopy = [copy.deepcopy(x) for x in peopleCopy]
    facultyCopy = [copy.deepcopy(p) for p in faculty]
    coursesCopy = generateAllCourses(courses)
    newCoursesCopy = [copy.deepcopy(x) for x in coursesCopy]

    wa = WeightAssigner()
    fullGraph = Graph(peopleCopy, facultyCopy, coursesCopy, wa)
    completedSchedule = {}
    coursesMatched = 0

    courseMapper = {}   # Map the index generated in the schedule to the actual course
    for i in range(len(coursesCopy)):
        courseMapper[i] = i
    personMapper = {}   # Map the index generated in the schedule to the actual person
    for i in range(len(peopleCopy)):
        personMapper[i] = i
    usedCourses = set()     # Courses that have already been matched

    while coursesMatched < len(coursesCopy):
        # Generate the assignment
        wa = WeightAssigner()
        g = Graph(newPeopleCopy, facultyCopy, newCoursesCopy, wa)
        g.printGraph()
        m1 = g.generateHungarianMatrix()
        schedule = g.generateSchedule(m1)

        # Break if no more assignments can be made
        if len(schedule) == 0:
            break

        coursesMatched += len(schedule)

        # Add the schedule to the completed schedule
        for personIndex, courseIndex in schedule.items():
            usedCourses.add(courseMapper[courseIndex])
            if personMapper[personIndex] in completedSchedule:
                pickedCourses = completedSchedule[personMapper[personIndex]]
                pickedCourses.append(courseMapper[courseIndex])
            else:
                completedSchedule[personMapper[personIndex]] = [courseMapper[courseIndex]]

            # Update the person's hours
            person = peopleCopy[personMapper[personIndex]]
            course = coursesCopy[courseMapper[courseIndex]]
            person.hoursCompleted += course.hoursValue
            person.coursesAssigned.append(course)

        # Remove people with not enough hours to do anything
        newPeopleCopy = []
        personIndex = 0
        newPersonMapper = {}
        for i, p in enumerate(peopleCopy):
            if p.availableHours() < 3:
                # Not enough hours to do anything, so don't include on next run of hungarian
                continue

            personCopy = copy.deepcopy(p)
            newPeopleCopy.append(personCopy)
            newPersonMapper[personIndex] = i
            personIndex += 1
        personMapper = newPersonMapper

        newCoursesCopy = []
        indexCounter = 0
        newCourseMapper = {}
        for i, c in enumerate(coursesCopy):

            # Check if the course is in the schedule
            if i in usedCourses:
                continue

            courseCopy = copy.deepcopy(c)
            newCoursesCopy.append(courseCopy)
            newCourseMapper[indexCounter] = i
            indexCounter += 1

        courseMapper = newCourseMapper

    printSchedule(peopleCopy, coursesCopy, completedSchedule)
    csvFilePath = readFromScheduleCSV(peopleCopy, coursesCopy, completedSchedule)
    return csvFilePath, completedSchedule


def printSchedule(people: typing.List[Person], courses: typing.List[Course], schedule: typing.Dict[int, int]):
    """
    Prints the generated schedule in a readable format.
    :param people: List of all the people.
    :param courses: List of all the possible course positions.
    :param schedule: Mapping of the indices between the people and courses.
    :return: None
    """
    print('%30s' % 'INSTRUCTOR' +
          '%6s' % 'CSE' +
          '%6s' % ' SEC' +
          ' CATEGORY\n')
    count = 0
    for i in sorted(schedule.items(), key=lambda x: people[x[0]].name):
        pIndex = i[0]
        for cIndex in i[1]:
            count += 1
            print('%5d' % count +
                  '%30s' % people[pIndex].name +
                  ": " +
                  '%5s' % courses[cIndex].courseNumber +
                  ", " +
                  '%5s' % courses[cIndex].section +
                  ", " +
                  courses[cIndex].category)


def classInSchedule(people, courses, schedule,cse,sec):
    for i in sorted(schedule.items(), key=lambda x: people[x[0]].name):
        pIndex = i[0]
        cIndices = i[1]
        for cIndex in cIndices:
            if cse == courses[cIndex].courseNumber and sec == courses[cIndex].section:
                tup = (people[pIndex].name,courses[cIndex].courseNumber,courses[cIndex].section,courses[cIndex].category)
                return tup
    return None

def readFromScheduleCSV(people, courses,schedule):
    print(type(schedule))
    print(schedule)
    newSchedule = []
    with open('persons.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                classScheduled = classInSchedule(people, courses, schedule, row[0], row[1])
                if classScheduled is not None:
                    if classScheduled[3] == 'assist':
                        row[12] = classScheduled[0]
                        row[15] = 1
                    else:
                        row[11] = classScheduled[0]
                        if classScheduled[3] == 'teach':
                            row[12] = 1
                        elif classScheduled[3] == 'recitation':
                            row[14] = 1
                    print('modified', row)

                newSchedule.append(row)

    fileName = 'newschedule.csv'
    createScheduleCSV(newSchedule, fileName)
    return fileName


def createScheduleCSV(headers, fileName):
    for header in headers:
        with open(fileName, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for header in headers:
                if header[0]:
                    filewriter.writerow(header)
