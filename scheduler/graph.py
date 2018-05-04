"""Graph representation for schedule generation."""

import copy
import typing

from .checker import validateComputerSkill, validateQualifyingExam, validateClassTimes, validateSchedulerHoursConstraint
from .course import Course
from .hungarian import Hungarian
from .person import Person


class WeightAssigner:
    def __init__(self):
        self.seniority = 1.0
        self.preference = 1.9
        self.category_pref = 1.2

        self.undefined_category_pref = 3
        self.undefined_seniority = 5

    def personWeight(self, person: Person, course: Course):
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
        categoryPref = ''
        if course.category == 'teach':
            prefs = person.teachingPrefs
            categoryPref = person.categoryPrefs["Teaching"]
        elif course.category == 'assist':
            prefs = person.assistingPrefs
            categoryPref = person.categoryPrefs["Assisting"]
        elif course.category == 'lab':
            prefs = person.labPrefs
            categoryPref = person.categoryPrefs["Labs"]
        elif course.category == 'recitation':
            prefs = person.recitationPrefs
            categoryPref = person.categoryPrefs["Recitation"]

        if categoryPref == '':
            categoryPrefIndex = self.undefined_category_pref
        else:
            categoryPrefIndex = int(categoryPref)

        categoryPrefIndex = (1.0/5) * categoryPrefIndex

        try:
            prefIndex = prefs.index(course.courseNumber) + 1
        except ValueError:
            prefIndex = 100

        # Grab the seniority
        if person.yearInSchool == 0:
            seniority = self.undefined_seniority
        else:
            seniority = (1 / 6.0) * person.yearInSchool

        # Check if the instructor is the person's sponsor
        # sponsor = person.supportingProfessor == course.instructor

        # Grab the same recitation multiplier
        recitationMultiplier = 1
        if course.category == "recitation":
            for c in person.coursesAssigned:
                if c.courseNumber == course.courseNumber and c.section[0] == course.section[0]:
                    recitationMultiplier *= 0.00001

            # Check if the person can teach the other recitations as well
            teachableSlots = 1.0 * person.availableHours() / course.hoursValue
            fractionOfTeachable = min(1.0 * teachableSlots / (course.recitationCount + 1), 1)
            recitationMultiplier /= fractionOfTeachable

        # Use those three categories to determine the weight of the edge
        weight = (self.preference * prefIndex) * (self.seniority * seniority) * (self.category_pref * categoryPrefIndex)
        weight *= recitationMultiplier
        return weight

    def professorWeight(self, professor: str, course: Course):
        return 1


class Node:
    def __init__(self, nodeType: str, data: typing.Union[Person, Course]):
        self.type = nodeType    # Represents the kind of node (i.e. course, ta, professor)
        self.data = data
        self.edges = {}

    def __str__(self):
        return self.type + self.data.__str__()


class Edge:
    def __init__(self, f: typing.Union[Person, Course], t: typing.Union[Person, Course], weight: float):
        self.f = f
        self.t = t
        self.weight = weight


def validPersonCourseEdge(person: Person, course: Course, errors: typing.List[str]):
    """
    Returns true if a person can teach a course.
    :param person: Person object.
    :param course: Course object.
    :param errors: List of errors for bookkeeping.
    :return: True if the person can teach the course.
    """
    # Check if there is a time conflict
    if not validateClassTimes(person, course, person.coursesAssigned, errors):
        return False

    # Check for qualifying exams
    if not validateQualifyingExam(person, course, errors):
        return False

    # Check if the person has enough teaching hours
    if not validateSchedulerHoursConstraint(person, course, errors):
        return False

    # Check if the class needs a computer science background
    if not validateComputerSkill(person, course, errors):
        return False

    return True


def validProfessorCourseEdge(professor: str, course: Course, errors: typing.List[str]):
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
    def __init__(self, people: typing.List[Person], faculty: typing.Dict[str, int],
                 courses: typing.List[Course], wa: WeightAssigner):
        """
        Create a graph with all the input.
        :param people: List of all the people.
        :param faculty: Mapping of faculty names to their respective hours.
        :param courses: List of all the courses.
        :param wa: Weight assigner for determining edge weights.
        """
        self.edges = []

        self.people = []
        self.faculty = []
        self.courses = []
        self.courseMapper = {}  # Map the indices in self.courses to the indices in courses
        recitationMapper = {}  # Map a recitation type to the course object

        coursesWithRecitations = set()

        # Generate all the course nodes
        courseCounter = 0
        for courseIndex, c in enumerate(courses):
            for t in c.positions:

                if t == "recitation":
                    courseTuple = (c.courseNumber, c.section[0])
                    if courseTuple in coursesWithRecitations:
                        recitationMapper[courseTuple].recitationCount += 1
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
                n = Node('course', course)
                self.courses.append(n)
                self.courseMapper[courseCounter] = courseIndex
                courseCounter += 1

                if t == "recitation":
                    coursesWithRecitations.add((c.courseNumber, c.section[0]))
                    recitationMapper[(c.courseNumber, c.section[0])] = course

        # Generate all the people nodes
        for p in people:
            n = Node('person', p)
            self.people.append(n)

        # Generate the faculty nodes
        for p in faculty[1]:            # TODO: remove this hack of hard coding the fall value
            n = Node('professor', p)
            self.faculty.append(n)

        # Generate the edges
        for pIndex, p in enumerate(self.people):
            for cIndex, c in enumerate(self.courses):
                errors = []
                if validPersonCourseEdge(p.data, c.data, errors):
                    weight = wa.personWeight(p.data, c.data)
                    e = Edge(p, c, weight)
                    p.edges[cIndex] = e
                    c.edges[pIndex] = e
                    self.edges.append(e)

        for pIndex, p in enumerate(self.faculty):
            for cIndex, c in enumerate(self.courses):
                errors = []
                if validProfessorCourseEdge(p.data, c.data, errors):
                    weight = wa.professorWeight(p.data, c.data)
                    e = Edge(p, c, weight)
                    p.edges[cIndex] = e
                    c.edges[pIndex] = e
                    self.edges.append(e)

    def printGraph(self) -> None:
        """
        Print details of the graph.
        :return: None
        """
        print('PEOPLE:', len(self.people))
        print('FACULTY:', len(self.faculty))
        print('COURSES:', len(self.courses))
        print('EDGES:', len(self.edges))

    def generateHungarianMatrix(self, undefinedEdgeWeight: float=5000.0) -> typing.List[typing.List[float]]:
        """
        Generate an adjacency matrix of the graph.
        :param undefinedEdgeWeight: Weight assigned to nonexistent edges.
        :return: Matrix represented as a two dimensional list with all the weights.
        """
        n = max(len(self.courses), len(self.people))
        m1 = [[0 for x in range(n)] for y in range(n)]
        for row in range(0, n):
            for col in range(0, n):
                if row < len(self.people) and col in self.people[row].edges.keys():
                    m1[row][col] = self.people[row].edges[col].weight
                else:
                    m1[row][col] = undefinedEdgeWeight
        print('*** M1 GENERATED ***')
        return m1

    def generateSchedule(self, m1: typing.List[typing.List[float]]) -> typing.Dict[int, int]:
        """
        Generate a schedule using the hungarian algorithm.
        :param m1: Two-dimensional graph.
        :return: Mapping of people indices to course indices.
        """
        hungarian = Hungarian(m1)
        hungarian.calculate()
        schedule = hungarian.get_results()

        # Convert the list of tuples into a dictionary
        scheduleDict = {}
        for personIndex, courseIndex in schedule:
            if personIndex < len(self.people) and courseIndex < len(self.courses):
                scheduleDict[personIndex] = self.courseMapper[courseIndex]
        return scheduleDict

    def printSchedule(self, schedule: typing.Dict[int, int]) -> None:
        """
        Prints the schedule in a readable format.
        :param schedule: Mapping of people indices to the course indices.
        :return: None
        """
        print('%30s' % 'INSTRUCTOR' +
              '%6s' % 'CSE' +
              '%6s' % ' SEC' +
              ' CATEGORY\n')
        for i in sorted(schedule.items(), key=lambda x: self.people[x[0]].data.name):
            pIndex = i[0]
            cIndex = i[1]
            print('%30s' % self.people[pIndex].data.name +
                    ": " +
                    '%5s' % self.courses[cIndex].data.courseNumber +
                    ", " +
                    '%5s' % self.courses[cIndex].data.section +
                    ", " +
                    self.courses[cIndex].data.category)
