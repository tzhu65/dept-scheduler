from .graph import WeightAssigner, Graph
import copy


def generate(courses, people, faculty):

    # Initial pass
    wa = WeightAssigner()
    g = Graph(people, faculty, courses, wa)
    g.printGraph()
    schedule = g.generateSchedule2()

    # Recalculate the hours of the students
    # peopleCopy = []
    # for p in people:
    #     peopleCopy.append(copy.deepcopy(p))

    # for pIndex, cIndex in schedule.items():
    #     p = peopleCopy[pIndex]

    #     print(pIndex, cIndex)
    # g.printSchedule(schedule)
