from datetime import datetime


class Person:

    def toString(self):
        str = ("name={%s} , year={%s}, currHours={%s}, availHours={%s}, "
               "teach={%s} , assist={%s}, recitation={%s}"
               ", category={%s} , leastCategoryPref={%s}" % (
                   self.name, self.year, self.currHours, self.availHours,
                   self.teachPrefs, self.assistPrefs, self.recitationPrefs,
                   self.categoryPrefs, self.categoryLeastPrefs))
        conflictStr = "\n"
        for conflict in self.conflicts:
            conflictStr += conflict.toString() + "\n"
        print(str, conflictStr)

    def __init__(self,
                 name,
                 year,
                 exams,
                 currHours,
                 availHours,
                 teachPrefs,
                 assistPrefs,
                 recitationPrefs,
                 categoryPrefs,
                 categoryLeastPrefs,
                 conflicts):
        self.name = name
        self.year = year
        self.exams = exams
        self.currHours = currHours
        self.availHours = availHours
        self.teachPrefs = teachPrefs
        self.assistPrefs = assistPrefs
        self.recitationPrefs = recitationPrefs
        self.categoryPrefs = categoryPrefs
        self.categoryLeastPrefs = categoryLeastPrefs
        self.conflicts = conflicts


class Conflict:

    def toString(self):
        if hasattr(self, "day"):
            return ("day={%s}, start={%s}, end={%s}" % (
                self.day, self.startTime, self.endTime))
        else:
            return ""

    def __init__(self,
                 day
                 , startTime
                 , endTime):
        if datetime.strptime(startTime, "%H:%M") < datetime.strptime(endTime, "%H:%M"):
            self.day = day
            self.startTime = datetime.strptime(startTime, "%H:%M").time()
            self.endTime = datetime.strptime(endTime, "%H:%M").time()
