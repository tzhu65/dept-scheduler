import copy
import numpy as np
import math
import sys

from .checker import validateComputerSkill, validateQualifyingExam, checkClassTimes, checkSchedulerHoursConstraint
from .hungarian import Hungarian


class WeightAssigner:
    def __init__(self):
        self.seniority = 1.0
        self.preference = 1.9
        self.category_pref = 1.2

        self.undefined_category_pref = 3
        self.undefined_seniority = 5

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

        # Use those three categories to determine the weight of the edge
        weight = (self.preference * prefIndex) * (self.seniority * seniority) * (self.category_pref * categoryPrefIndex)
        if weight <= 0:
            print('bad weight', weight)
        return weight

    def professorWeight(self, professor, course):
        return 1


class Node:
    def __init__(self, type, data):
        self.type = type    # Represents the kind of node (i.e. course, ta, professor)
        self.data = data
        self.edges = {}

    def __str__(self):
        return self.type + self.data.__str__()


class Edge:
    def __init__(self, f, t, weight):
        self.f = f
        self.t = t
        self.weight = weight
        # if weight == '':
        #     print("BLAAAAAAAAAAAAAAAAAAH", f, t)


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
    if not checkSchedulerHoursConstraint(person, course, errors):
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
            for t in c.positions:
                for i in range(c.positions[t]["amount"]):
                    # Deep copy this node and set the category
                    course = copy.deepcopy(c)
                    course.positions = {t: {"amount": 1, "hours": c.positions[t]["hours"]}}
                    course.category = t
                    course.hoursValue = c.positions[t]["hours"]
                    if not isinstance(course.hoursValue, int):
                        course.hoursValue = 0
                    n = Node('course', course)
                    self.courses.append(n)

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

    def printGraph(self):
        print('PEOPLE:', len(self.people))
        print('FACULTY:', len(self.faculty))
        print('COURSES:', len(self.courses))
        print('EDGES:', len(self.edges))

    def generateHungarianMatrix(self):
        n = max(len(self.courses), len(self.people))
        m1 = [[0 for x in range(n)] for y in range(n)]
        for row in range(0, n):
            for col in range(0, n):
                if row < len(self.people) and col in self.people[row].edges.keys():
                    m1[row][col] = self.people[row].edges[col].weight
                else:
                    # m1[row][col] = sys.float_info.max
                    m1[row][col] = 5000.0
        print('*** M1 GENERATED ***')
        return m1

    def generateSchedule(self, m1):
        hungarian = Hungarian(m1)
        hungarian.calculate()
        schedule = hungarian.get_results()

        # Convert the list of tuples into a dictionary
        scheduleDict = {}
        for personIndex, courseIndex in schedule:
            if personIndex < len(self.people) and courseIndex < len(self.courses):
                scheduleDict[personIndex] = courseIndex
        return scheduleDict


    def printSchedule(self, schedule):
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

    def classInSchedule(self,schedule,cse,sec):
        for i in sorted(schedule.items(), key=lambda x: self.people[x[0]].data.name):
            pIndex = i[0]
            cIndices = i[1]
            for cIndex in cIndices:
                if cse == self.courses[cIndex].data.courseNumber and sec == self.courses[cIndex].data.section:
                    tup = (self.people[pIndex].data.name,self.courses[cIndex].data.courseNumber,self.courses[cIndex].data.section,self.courses[cIndex].data.category)
                    return tup
        return None

#max of vertical vs horizontal at index row col
def hvMax(m1, rowIndex, colIndex):
        vertical = 0
        horizontal = 0

        # check horizontal
        for index, value in enumerate(m1):
            if m1[rowIndex][index] == 0:
                horizontal = horizontal + 1

        # check vertical
        for index, value in enumerate(m1):
            if m1[index][colIndex] == 0:
                vertical = vertical + 1

        # negative for horizontal, positive for vertical
        return vertical if vertical > horizontal else horizontal * -1

# clear the neighbors of the picked largest value, the sign will let the
# app decide which direction to clear
def clearNeighbors(m2, m3, rowIndex, colIndex):
        # if vertical
        if m2[rowIndex][colIndex] > 0:
            for index, val in enumerate(m2):
                if m2[index][colIndex] > 0:
                    m2[index][colIndex] = 0 # clear neighbor
                m3[index][colIndex] = 1 # draw line
        else:
            for index, val in enumerate(m2):
                if m2[rowIndex][index] < 0:
                    m2[rowIndex][index] = 0 # clear neighbor
                m3[rowIndex][index] = 1 # draw line

        m2[rowIndex][colIndex] = 0
        m3[rowIndex][colIndex] = 1
