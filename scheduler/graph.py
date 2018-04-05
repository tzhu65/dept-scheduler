import copy


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

    def __str__(self):
        return self.type + self.data.__str__()


class Edge:
    def __init__(self, f, t, weight):
        self.f = f
        self.t = t
        self.weight = weight


def validPersonCourseEdge(person, course):
    """
    Returns true if a person can teach a course.
    :param person:
    :param course:
    :return:
    """
    print(person, course)
    return True


def validProfessorCourseEdge(professor, course):
    """
    Returns true if the professor can teach a course.
    :param professor:
    :param course:
    :return:
    """
    return True


class Graph:
    """
    Graph class to represent an undirected weighted graph.
    """
    def __init__(self, people, faculty, courses, wa):
        self.edges = []

        self.people = []
        self.faculty = []
        self.courses = []

        # Generate all the course nodes
        for c in courses:
            for type in c.types:
                for i in range(c.types[type]["amount"]):
                    # Deep copy this node and set the category
                    course = copy.deepcopy(c)
                    course.category = type
                    course.hoursVal = c.types[type]["hours"]
                    n = Node('course', course)
                    self.courses.append(n)

        # Generate all the people nodes
        for p in people:
            n = Node('person', p)
            self.people.append(n)

        # Generate the faculty nodes
        for p in faculty:
            n = Node('professor', p)
            self.faculty.append(n)

        # Generate the edges
        for p in self.people:
            for c in self.courses:
                if validPersonCourseEdge(p.data, c.data):
                    weight = wa.personWeight(p.data, c.data)
                    e = Edge(p, c, weight)
                    p.edges.append(e)
                    c.edges.append(e)
                    self.edges.append(e)

        for p in self.faculty:
            for c in self.courses:
                if validProfessorCourseEdge(p.data, c.data):
                    weight = wa.professorWeight(p.data, c.data)
                    e = Edge(p, c, weight)
                    p.edges.append(e)
                    c.edges.append(c)
                    self.edges.append(e)

    def generateSchedule(self):
        """
        Generate a schedule.
        :return:
        """
        pass
