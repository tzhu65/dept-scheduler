from datetime import datetime


class Person:

    def toString(self):
        str = ("name={%s}, fullySupported={%s}, yearInSchool={%s}, pureOrApplied={%s}, qualifyingExams={%s}"
               ", teachingPrefs={%s}, labPrefs={%s}, assistingPrefs={%s}, recitationPrefs={%s}"
               ", categoryPrefs={%s}, computerSkills={%s}" % (
                   self.name, self.fullySupported, self.yearInSchool, self.pureOrApplied, self.qualifyingExams,
                   self.teachingPrefs, self.labPrefs, self.assistingPrefs, self.recitationPrefs,
                   self.categoryPrefs, self.computerSkills))
        conflictStr = "\n"
        for conflict in self.conflicts:
            conflictStr += conflict.toString() + "\n"
        print(str, conflictStr)

    def __init__(self,
                 name,
                 fullySupported,
                 yearInSchool,
                 pureOrApplied,
                 qualifyingExams,
                 teachingPrefs,
                 labPrefs,
                 assistingPrefs,
                 recitationPrefs,
                 categoryPrefs,
                 conflicts,
                 computerSkills):
        self.name = name
        self.fullySupported = fullySupported
        self.yearInSchool = yearInSchool
        self.pureOrApplied = pureOrApplied
        self.qualifyingExams = qualifyingExams
        self.teachingPrefs = teachingPrefs
        self.labPrefs = labPrefs
        self.assistingPrefs = assistingPrefs
        self.recitationPrefs = recitationPrefs
        self.categoryPrefs = categoryPrefs
        self.conflicts = conflicts
        self.computerSkills = computerSkills
        self.qualifyingExams = qualifyingExams


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
