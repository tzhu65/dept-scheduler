import copy

from .checker import validateComputerSkill, validateQualifyingExam, checkClassTimes, checkHoursConstraint


class WeightAssigner:
    def __init__(self):
        self.seniority = 1
        self.preference = 1

    def personWeight(self, person, course):
        """
        Generates a weight for an edge that exists between a person and a course. The factors to take into account
        include:
            - seniority of the person
            - preference order
            - sponsor teaches the class

        :param person:
        :param course:
        :return:
        """

        # Determine preference
        prefs = []
        if course.category == 'teach':
            prefs = person.teachingPrefs
        elif course.category == 'assist':
            prefs = person.assistingPrefs
        elif course.category == 'lab':
            prefs = person.labPrefs
        elif course.category == 'recitation':
            prefs = person.recitationPrefs

        try:
            prefIndex = prefs.index(course.courseNumber)
        except ValueError:
            prefIndex = -1

        # Grab the seniority
        seniority = person.yearsInSchool

        # Check if the instructor is the person's sponsor
        sponsor = person.supportingProfessor == course.instructor

        # Use those three categories to determine the weight of the edge
        weight = prefIndex * seniority * sponsor

        return weight

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


def validPersonCourseEdge(person, course, errors):
    """
    Returns true if a person can teach a course.
    :param person:
    :param course:
    :return:
    """
    # Check if there is a time conflict
    if not checkClassTimes(person, course, [], errors):
        return False

    # Check for qualifying exams
    if not validateQualifyingExam(person, course, errors):
        return False

    # Check if the person has enough teaching hours
    if not checkHoursConstraint(person, course, errors):
        return False

    # Check if the class needs a computer science background
    if not validateComputerSkill(person, course, errors):
        return False

    return True


def validProfessorCourseEdge(professor, course, errors):
    """
    Returns true if the professor can teach a course. Currently, they are only allowed to teach a course.
    :param professor:
    :param course:
    :return:
    """
    return course.category == 'teach'


class Graph:
    """
    Graph class to represent an undirected weighted graph.
    """
    def __init__(self, people, faculty, courses, wa):
        global val
        self.edges = []

        self.people = []
        self.faculty = []
        self.courses = []

        # Generate all the course nodes
        for c in courses:
            for t in c.types:
                print(t)
                for i in range(c.types[t]["amount"]):
                    # Deep copy this node and set the category
                    course = copy.deepcopy(c)
                    course.category = t
                    course.hoursValue = c.types[t]["hours"]
                    if not isinstance(course.hoursValue, int):
                        course.hoursValue = 0
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
                errors = []
                if validPersonCourseEdge(p.data, c.data, errors):
                    weight = wa.personWeight(p.data, c.data)
                    e = Edge(p, c, weight)
                    p.edges.append(e)
                    c.edges.append(e)
                    self.edges.append(e)

        for p in self.faculty:
            for c in self.courses:
                errors = []
                if validProfessorCourseEdge(p.data, c.data, errors):
                    weight = wa.professorWeight(p.data, c.data)
                    e = Edge(p, c, weight)
                    p.edges.append(e)
                    c.edges.append(c)
                    self.edges.append(e)

    def printGraph(self):
        print('PEOPLE:', len(self.people))
        print('FACULTY:', len(self.faculty))
        print('COURSES:', len(self.courses))
        print('EDGES:', len(self.edges))

    def generateSchedule(self):
        """
        Generate a schedule.
        :return:
        """
        pass
