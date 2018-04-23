from .graph import WeightAssigner, Graph
import copy
import csv

def generate(courses, people, faculty):

    # Keep looping until all courses are matched or no more people can be matched
    wa = WeightAssigner()
    g = Graph(people, faculty, courses, wa)
    m1 = g.generateHungarianMatrix()
    g.printGraph()
    schedule = g.generateSchedule(m1)
    g.printSchedule(schedule)
    readFromScheduleCSV(g,schedule)

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
                print('modified' , row)


            newSchedule.append(row)
            # print('this mah shit' ,row)
    createScheduleCSV(newSchedule)

def createScheduleCSV(headers):
    for header in headers:
        # print('header is ' , header)

        with open('newschedule.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for header in headers:
                filewriter.writerow(header)
