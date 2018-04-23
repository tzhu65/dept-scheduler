import copy
import numpy as np

class Hungarian:
    def __init__(self, m1):
        self.n = len(m1)
        self.m1 = np.array(m1)
        self.m1Clone = np.array(m1) # keep a copy
        self.lines = [[0 for x in range(self.n)] for y in range(self.n)]
        self.numLines = 0

        self.rows = [0 for x in range(self.n)]
        self.occupiedCols = [0 for x in range(self.n)]

        # algorithm
        self.subtractRowMin()
        self.subtractColMin()
        self.coverZeroes()
        while self.numLines < self.n:
            self.createAdditionalZeroes()
            self.coverZeroes()
        self.createSchedule(0)

        print("final m1\n", self.m1)
        print("occupied columns (should all be 1)\n", self.occupiedCols)
        print("selected zeroes (index = row, value = column)\n", self.rows)

    def subtractRowMin(self):
        for row in self.m1:
            m = min(row)
            for index, value in enumerate(row):
                row[index] -= m

    def subtractColMin(self):
        for col in self.m1.transpose():
            m = min(col)
            for index, value in enumerate(col):
                col[index] -= m

    def coverZeroes(self):
        self.numLines = 0
        self.lines = [[0 for x in range(self.n)] for y in range(self.n)]
        for rowIndex, row in enumerate(self.m1): 
            for colIndex, col in enumerate(row):
                if self.m1[rowIndex][colIndex] == 0:
                    self.colorNeighbors(rowIndex, colIndex, self.maxVH(rowIndex, colIndex))

    def maxVH(self, rowIndex, colIndex):
        result = 0
        for i in range(0, self.n):
            if self.m1[i][colIndex] == 0:
                result += 1
            if self.m1[rowIndex][i] == 0:
                result -= 1
        return result

    def colorNeighbors(self, rowIndex, colIndex, maxVH):
        if self.lines[rowIndex][colIndex] == 2: # colored twice
            return
        if maxVH > 0 and self.lines[rowIndex][colIndex] == 1: # colored vertically and needs to be recolored vertically, don't color again
            return
        if maxVH <= 0 and self.lines[rowIndex][colIndex] == -1: # colored horizontally and needs to be recolored horizontally, don't color again
            return
        for i in range(0, self.n):
            if maxVH > 0: # color vertically
                self.lines[i][colIndex] = 2 if self.lines[i][colIndex] == -1 or self.lines[i][colIndex] == 2 else 1 # was horizontal, needs to be vertical
            else:
                self.lines[rowIndex][i] = 2 if self.lines[rowIndex][i] == 1 or self.lines[rowIndex][i] == 2 else -1 # was vertical, needs to be horizontal

        self.numLines += 1

    def createAdditionalZeroes(self):
        minUncoveredVal = 0

        for rowIndex, row in enumerate(self.m1):
            for colIndex, col in enumerate(row):
                if self.lines[rowIndex][colIndex] == 0 and \
                    (self.m1[rowIndex][colIndex] < minUncoveredVal or minUncoveredVal == 0):
                    minUncoveredVal = self.m1[rowIndex][colIndex]

        for rowIndex, row in enumerate(self.m1):
            for colIndex, col in enumerate(row):
                if self.lines[rowIndex][colIndex] == 0: # not covered
                    self.m1[rowIndex][colIndex] -= minUncoveredVal
                elif self.lines[rowIndex][colIndex] == 2: # covered twice
                    self.m1[rowIndex][colIndex] += minUncoveredVal

    def createSchedule(self, rowIndex):
        if rowIndex == len(self.rows):
            return True # done
        
        for colIndex in range(0, self.n):
            if self.m1[rowIndex][colIndex] == 0 and self.occupiedCols[colIndex] == 0:
                self.rows[rowIndex] = colIndex
                self.occupiedCols[colIndex] = 1
                if self.createSchedule(rowIndex + 1):
                    return True
                self.occupiedCols[colIndex] = 0 # go back and try again

        return False