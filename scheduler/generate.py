from .graph import WeightAssigner, Graph
import copy
import csv

def generate(courses, people, faculty):

    # Keep looping until all courses are matched or no more people can be matched
    wa = WeightAssigner()
    fullGraph = Graph(people, faculty, courses, wa)
    completedSchedule = {}
    coursesMatched = 0

    peopleCopy = [copy.deepcopy(p) for p in people]
    facultyCopy = [copy.deepcopy(p) for p in faculty]
    coursesCopy = [copy.deepcopy(c) for c in courses]

    while coursesMatched < len(fullGraph.courses):

        # Generate the assignment
        wa = WeightAssigner()
        g = Graph(peopleCopy, facultyCopy, coursesCopy, wa)
        g.printGraph()
        m1 = g.generateHungarianMatrix()
        schedule = g.generateSchedule(m1)
        courseMapper = {}
        usedCourses = set()
        for i in range(len(coursesCopy)):
            courseMapper[i] = i

        # Break if no more assignments can be made
        if len(schedule) == 0:
            break

        coursesMatched += len(schedule)
        print('got this many courses', coursesMatched)

        # Add the schedule to the completed schedule
        for personIndex, courseIndex in schedule.items():
            if personIndex in completedSchedule:
                pickedCourses = completedSchedule[personIndex]
                pickedCourses.append(courseIndex)
            else:
                completedSchedule[personIndex] = [courseIndex]

        # Recalculate the hours of the students
        peopleCopy = []
        for i, p in enumerate(people):
            personCopy = copy.deepcopy(p)
            peopleCopy.append(personCopy)

            # Check if the person is in the schedule
            if i in schedule:
                # Increase their hours completed amounts
                course = fullGraph.courses[courseMapper[schedule[i]]].data
                personCopy.hoursCompleted += course.hoursValue

        # Remove the used courses
        for i in schedule.values():
            usedCourses.add(courseMapper[i])
        coursesCopy = []
        indexCounter = 0

        for i, c in enumerate(fullGraph.courses):

            # Check if the course is in the schedule
            if i in usedCourses:
                continue

            courseCopy = copy.deepcopy(c.data)
            coursesCopy.append(courseCopy)
            courseMapper[indexCounter] = i
            indexCounter += 1

    printSchedule(fullGraph, completedSchedule)
    csvFilePath = readFromScheduleCSV(fullGraph, completedSchedule)
    return csvFilePath, completedSchedule

def printSchedule(graph, schedule):
    print('%30s' % 'INSTRUCTOR' +
          '%6s' % 'CSE' +
          '%6s' % ' SEC' +
          ' CATEGORY\n')
    for i in sorted(schedule.items(), key=lambda x: graph.people[x[0]].data.name):
        pIndex = i[0]
        for cIndex in i[1]:
            print('%30s' % graph.people[pIndex].data.name +
                  ": " +
                  '%5s' % graph.courses[cIndex].data.courseNumber +
                  ", " +
                  '%5s' % graph.courses[cIndex].data.section +
                  ", " +
                  graph.courses[cIndex].data.category)

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

def readFromScheduleCSV(g,schedule):
    print(type(schedule))
    print(schedule)
    newSchedule = []
    with open('persons.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            classScheduled = g.classInSchedule(schedule,row[0],row[1])
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

        with open(fileName, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for header in headers:
                filewriter.writerow(header)
