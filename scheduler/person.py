from datetime import datetime


class Person:

    def __init__(self,
                 name,
                 fullySupported,
                 supportingProfessor,
                 yearInSchool,
                 pureOrApplied,
                 qualifyingExams,
                 teachingPrefs,
                 labPrefs,
                 assistingPrefs,
                 recitationPrefs,
                 categoryPrefs,
                 conflicts,
                 computerSkills,
                 hoursCompleted,
                 hoursBoughtOut):
        self.name = name
        self.fullySupported = fullySupported
        self.supportingProfessor = supportingProfessor
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
        self.hoursCompleted = hoursCompleted
        self.hoursBoughtOut = hoursBoughtOut
        self.coursesAssigned = []

    def __str__(self):
        stri = ("name={%s}, fullySupported={%s}, supportingProfessor={%s}, yearInSchool={%s}, pureOrApplied={%s}"
               ", qualifyingExams={%s}, teachingPrefs={%s}, labPrefs={%s}, assistingPrefs={%s}, recitationPrefs={%s}"
               ", categoryPrefs={%s}, conflicts={%s},computerSkills={%s}, hoursCompleted={%s}, hoursBoughtOut={%s}" % (
                   self.name, self.fullySupported, self.supportingProfessor ,self.yearInSchool, self.pureOrApplied,
                   self.qualifyingExams, self.teachingPrefs, self.labPrefs, self.assistingPrefs, self.recitationPrefs,
                   self.categoryPrefs, self.conflicts, self.computerSkills, self.hoursCompleted, self.hoursBoughtOut))
        conflictStr = "\n"
        for conflict in self.conflicts:
            conflictStr += str(conflict) + "\n"
        return stri + conflictStr


class PersonalConflict:

    def __init__(self, classNumber, day, startTime, endTime):
        if datetime.strptime(startTime, "%H:%M") < datetime.strptime(endTime, "%H:%M"):
            self.classNumber = classNumber
            self.day = day
            self.startTime = datetime.strptime(startTime, "%H:%M").time()
            self.endTime = datetime.strptime(endTime, "%H:%M").time()

    def __str__(self):
        if hasattr(self, "day"):
            return ("class={%s}, day={%s}, start={%s}, end={%s}" % (
                self.classNumber, self.day, self.startTime, self.endTime))
        else:
            return ""
