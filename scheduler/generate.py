from .graph import WeightAssigner, Graph


def generate(courses, people, faculty):
    wa = WeightAssigner()
    g = Graph(people, faculty, courses, wa)
    g.printGraph()
    schedule = g.generateSchedule()
    g.printSchedule(schedule)
