from .graph import WeightAssigner, Graph, Node
import copy
import csv

def generateAllCourses(courses):

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

def generate(courses, people, faculty):

    # Keep looping until all courses are matched or no more people can be matched
    peopleCopy = [copy.deepcopy(p) for p in people]
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
    usedCourses = set()     # Courses that have already been matched

    while coursesMatched < len(coursesCopy):
        # Generate the assignment
        wa = WeightAssigner()
        g = Graph(peopleCopy, facultyCopy, newCoursesCopy, wa)
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
            if personIndex in completedSchedule:
                pickedCourses = completedSchedule[personIndex]
                pickedCourses.append(courseMapper[courseIndex])
            else:
                completedSchedule[personIndex] = [courseMapper[courseIndex]]

        # Recalculate the hours of the students
        newPeopleCopy = []
        for i, p in enumerate(peopleCopy):
            personCopy = copy.deepcopy(p)
            newPeopleCopy.append(personCopy)

            # Check if the person is in the schedule
            if i in schedule:
                # Increase their hours completed amounts
                course = coursesCopy[courseMapper[schedule[i]]]
                personCopy.hoursCompleted += course.hoursValue
        peopleCopy = newPeopleCopy

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

def printSchedule(people, courses, schedule):
    print('%30s' % 'INSTRUCTOR' +
          '%6s' % 'CSE' +
          '%6s' % ' SEC' +
          ' CATEGORY\n')
    for i in sorted(schedule.items(), key=lambda x: people[x[0]].name):
        pIndex = i[0]
        for cIndex in i[1]:
            print('%30s' % people[pIndex].name +
                  ": " +
                  '%5s' % courses[cIndex].courseNumber +
                  ", " +
                  '%5s' % courses[cIndex].section +
                  ", " +
                  courses[cIndex].category)

# def createScheduleCSV(headers):
#     for header in headers:
#         # print('header is ' , header)
#
#         with open('newschedule.csv', 'w') as csvfile:
#             filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#             for header in headers:
#                 filewriter.writerow(header)

#
# def courseInSchedule(cse,sec,schedule):
#     for i in sorted(schedule.items(), key=lambda x: self.people[x[0]].data.name):
#         pIndex = i[0]
#         cIndex = i[1]


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
                # print(row)
                classScheduled = classInSchedule(people, courses, schedule,row[0],row[1])
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
                # print('this mah shit' ,row)

    fileName = 'newschedule.csv'
    createScheduleCSV(newSchedule, fileName)
    return fileName


def createScheduleCSV(headers, fileName):
    for header in headers:
        # print('header is ' , header)

        with open(fileName, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for header in headers:
                if header[0]:
                    filewriter.writerow(header)
