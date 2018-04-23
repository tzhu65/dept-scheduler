from .graph import WeightAssigner, Graph
import copy


def generate(courses, people, faculty):

    # Keep looping until all courses are matched or no more people can be matched
    wa = WeightAssigner()
    g = Graph(people, faculty, courses, wa)
    g.printGraph()
    schedule = g.generateSchedule2()



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
