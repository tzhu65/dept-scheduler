import copy
import numpy as np
import math
import random


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
        seniority = person.yearInSchool

        # Check if the instructor is the person's sponsor
        # sponsor = person.supportingProfessor == course.instructor

        # Use those three categories to determine the weight of the edge
        weight = prefIndex * seniority

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
            for t in c.positions:
                for i in range(c.positions[t]["amount"]):
                    # Deep copy this node and set the category
                    course = copy.deepcopy(c)
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

    def generateSchedule(self):
            n = max(len(self.courses), len(self.people)) # size of matrix

            # initial input
            m1 = [[0 for x in range(n)] for y in range(n)] 

            # EXAMPLE 1
            # Expected output: map:  {0: 0, 2: 2, 1: 1}
            # m1[0][0] = 250 
            # m1[0][1] = 450
            # m1[0][2] = 350 
            # m1[1][0] = 400
            # m1[1][1] = 400
            # m1[1][2] = 350
            # m1[2][0] = 200
            # m1[2][1] = 500
            # m1[2][2] = 250

            # EXAMPLE 2
            # Expected output: {0: 2, 1: 1, 2: 0, 3: 3}

            # m1[0][0] = 82
            # m1[0][1] = 83
            # m1[0][2] = 69
            # m1[0][3] = 92
            # m1[1][0] = 77
            # m1[1][1] = 37
            # m1[1][2] = 49
            # m1[1][3] = 92
            # m1[2][0] = 11
            # m1[2][1] = 69
            # m1[2][2] = 5
            # m1[2][3] = 86
            # m1[3][0] = 8
            # m1[3][1] = 9
            # m1[3][2] = 98
            # m1[3][3] = 23

            # EXAMPLE 3
            # Expected output: {2: 1, 0: 0, 1: 3, 3: 2}

            # m1[0][0] = 20
            # m1[0][1] = 25
            # m1[0][2] = 22
            # m1[0][3] = 28
            # m1[1][0] = 15
            # m1[1][1] = 18
            # m1[1][2] = 23
            # m1[1][3] = 17
            # m1[2][0] = 19
            # m1[2][1] = 17
            # m1[2][2] = 21
            # m1[2][3] = 24
            # m1[3][0] = 25
            # m1[3][1] = 23
            # m1[3][2] = 24
            # m1[3][3] = 24

            for row in range(0, len(self.people)):
                for col in range(0, len(self.courses)):
                    if col in self.people[row].edges.keys():
                        m1[row][col] = self.people[row].edges[col].weight
                    else:
                        m1[row][col] = math.inf

            print('*** M1 GENERATED ***')            
            
            m1 = np.array(m1)
            m1Copy = np.array(m1) # copy of initial input

            for row in m1:
                m = min(row)
                for index, value in enumerate(row):
                    row[index] -= m

            for col in m1.transpose():
                m = min(col)
                for index, value in enumerate(col):
                    col[index] -= m

            m2 = np.array([[0 for x in range(n)] for y in range(n)]) 
            m3 = np.array([[0 for x in range(n)] for y in range(n)])

            lines = 0
            rows = [0] * n
            cols = [0] * n
            
            while lines < n:
                # loop on zeroes from the input array, and store the max num of zeroes
                for rowIndex, row in enumerate(m1): 
                    for colIndex, col in enumerate(row):
                        if m1[rowIndex][colIndex] == 0:
                            m2[rowIndex][colIndex] = hvMax(m1, rowIndex, colIndex)

                # loop on m2 elements, clear neighbors and draw the lines
                for rowIndex, row in enumerate(m1): 
                    for colIndex, col in enumerate(row):
                        if abs(m2[rowIndex][colIndex]) > 0:
                            clearNeighbors(m2, m3, rowIndex, colIndex)

                for index, row in enumerate(m3):
                    if np.count_nonzero(row == 1) == n:
                        lines = lines + 1
                        rows[index] = 1
                for index, col in enumerate(m3.transpose()):
                    if np.count_nonzero(col == 1) == n:
                        lines = lines + 1
                        cols[index] = 1

                if (lines >= n):
                    break

                minVal = math.inf
                for index, row in enumerate(m3):
                    for rowIndex, value in enumerate(row):
                        if value == 0: # uncovered
                            minVal = min(minVal, m1[index][rowIndex])

                for index, row in enumerate(m3):
                    for rowIndex, value in enumerate(row):
                        if value == 0: # uncovered
                            m1[index][rowIndex] -= minVal # subtract from each uncovered
                        elif rows[index] == 1 and cols[rowIndex] == 1:
                            m1[index][rowIndex] += minVal # add to intersections

            m4 = {} # mapping from row to col

            for index, row in enumerate(m1):
                if np.count_nonzero(row == 0) == 1:
                    m4[index] = row.tolist().index(0)
            # print("map: ", m4)

            print('*** BEGINNING CHOOSING ZEROES ***')

            while len(m4.keys()) < n:
                keySize = len(m4.keys())
                for index, row in enumerate(m1):
                    if index in m4.keys():
                        continue
                    indices = set([i for i, x in enumerate(row) if x == 0])
                    # print("indices before remove ", indices)
                    for i in m4.values():
                        indices.discard(i)
                    # print("indices after remove ", indices)
                    if len(indices) == 1:
                        m4[index] = indices.pop()

                # print("***stuck, will now choose arbitrary***")

                # if no new info was added in an entire iteration,
                # do the same thing but don't require len(indices == 1)
                if keySize == len(m4.keys()): 
                    for index, row in enumerate(m1):
                        if index in m4.keys():
                            continue
                        indices = set([i for i, x in enumerate(row) if x == 0])
                        # print("indices before remove ", indices)
                        for i in m4.values():
                            indices.discard(i)
                        # print("indices after remove ", indices)
                        try: 
                            m4[index] = indices.pop() # choose a random one doesn't matter
                        except KeyError as e:
                            print("ALGORITHM YIELDS NO RESULTS")
                            print("ERR: ", e)
                            return

                # print("map: ", m4)

            print(m1)

            # if a full row is inf, cut it now
            # TODO: to same for courses (columns)
            if len(self.people) < n:
                for i in range(len(self.people), n):
                    m4.pop(i, None)

            print('*** FINISHED GENERATING SCHEDULE ***')

            return m4

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