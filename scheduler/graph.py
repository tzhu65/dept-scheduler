

class WeightAssigner:
    def __init__(self):
        self.seniority = 1
        self.preference = 1

    def personWeight(self, person, course):
        return 1

    def professorWeight(self, professor, course):
        return 1


class Node:
    def __init__(self, type, data):
        self.type = type
        self.data = data
        self.edges = []


class Edge:
    def __init__(self, f, t):
        self.f = f
        self.t = t


class Graph:
    """
    Graph class to represent an undirected weighted graph.
    """
    def __init__(self, people, faculty, courses, wa):
        # self.people = people
        # self.faculty = faculty
        # self.courses = courses
        self.edges = []

        self.people = []
        self.faculty = []
        self.courses = []

        # Generate all the course nodes
        for c in courses:
            course = Node('course', c)
            self.courses.append(course)
            print(c)

        # Generate the edges here
        for p in people:
            for c in courses:
                person = Node('person', p)
                weight = wa.personWeight(p, c)
                # edge = Edge()

        # for p in faculty:
        #     for c in courses:
        #         professor = Node('professor', p)
        #         weight = wa.professorWeight(p, c)
        #         # edge = Edge()



    def generateSchedule(self):
        """
        Generate a schedule.
        :return:
        """
        pass


