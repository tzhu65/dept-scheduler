from django.test import TestCase
from scheduler.graph import Graph, WeightAssigner


class HungarianTestCase(TestCase):

    def test_case_1(self):
        wa = WeightAssigner
        g = Graph([], [[], []], [], wa)
        n = 3
        m1 = [[0 for x in range(n)] for y in range(n)]
        m1[0][0] = 250
        m1[0][1] = 450
        m1[0][2] = 350
        m1[1][0] = 400
        m1[1][1] = 400
        m1[1][2] = 350
        m1[2][0] = 200
        m1[2][1] = 500
        m1[2][2] = 250
        schedule = g.generateSchedule(m1, False)
        self.assertDictEqual(schedule, {0: 0, 1: 1, 2: 2}, "Hungarian produced the wrong output.")

    def test_case_2(self):
        wa = WeightAssigner
        g = Graph([], [[], []], [], wa)
        n = 4
        m1 = [[0 for x in range(n)] for y in range(n)]
        m1[0][0] = 82
        m1[0][1] = 83
        m1[0][2] = 69
        m1[0][3] = 92
        m1[1][0] = 77
        m1[1][1] = 37
        m1[1][2] = 49
        m1[1][3] = 92
        m1[2][0] = 11
        m1[2][1] = 69
        m1[2][2] = 5
        m1[2][3] = 86
        m1[3][0] = 8
        m1[3][1] = 9
        m1[3][2] = 98
        m1[3][3] = 23
        schedule = g.generateSchedule(m1, False)
        self.assertDictEqual(schedule, {0: 2, 1: 1, 2: 0, 3: 3}, "Hungarian produced the wrong output.")

    def test_case_3(self):
        wa = WeightAssigner
        g = Graph([], [[], []], [], wa)
        n = 4
        m1 = [[0 for x in range(n)] for y in range(n)]
        m1[0][0] = 20
        m1[0][1] = 25
        m1[0][2] = 22
        m1[0][3] = 28
        m1[1][0] = 15
        m1[1][1] = 18
        m1[1][2] = 23
        m1[1][3] = 17
        m1[2][0] = 19
        m1[2][1] = 17
        m1[2][2] = 21
        m1[2][3] = 24
        m1[3][0] = 25
        m1[3][1] = 23
        m1[3][2] = 24
        m1[3][3] = 24
        schedule = g.generateSchedule(m1, False)
        self.assertDictEqual(schedule, {0: 0, 1: 3, 2: 1, 3: 2}, "Hungarian produced the wrong output.")
