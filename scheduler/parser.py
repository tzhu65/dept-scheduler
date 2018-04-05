import csv
import re
from datetime import datetime
from .person import Person
from .person import Conflict
from .course import Course
from .parserConstants import *


def sanitizeList(text):
    text = text.replace(';', ',')
    return [x for x in (map(lambda x: x.strip(), text.split(','))) if x != '']


def parseTime(time, formats):
    # try different formats (sometimes it's '9:30AM', sometimes '9:30 AM')
    for format in formats:
        try:
            return datetime.strptime(time, format).time()
        except ValueError:
            pass
    return 'N/A'


def getConflicts(listOfConflicts):
    index = 0
    conflicts = []
    for potentialConflicts in listOfConflicts:
        conflictParts = potentialConflicts.split(' ')

        if len(conflictParts) != 5 or conflictParts[3] != '-':
            return conflicts
        days = conflictParts[1] == 'MWF' or conflictParts[1] == 'TR'
        valdidNum = conflictParts[0].isdigit()
        if not days or not valdidNum:
            return conflicts
        conflict = Conflict(conflictParts[0],conflictParts[1],conflictParts[2],conflictParts[4])
        conflicts.append(conflict)
    return conflicts


def parsePeopleFromPath(path):
    with open(path, newline='') as file:
        return parsePeople(file)


def parsePeople(file):
    people = []
    fields = {}
    reader = csv.reader(file)
    headers = next(reader)
    for index, field in enumerate(headers):
        fields[field] = index
    for row in reader:
        # if has a datetime and are returning next semester, then we create person object
        if row[0] and row[fields[RETURNING]] != 'No':
            # get all data besides the conflicts
            teachingPrefs = []
            labPrefs = []
            recitationPrefs = []
            assistingPrefs = []
            categoryPrefs = {}
            categoryPrefs["Labs"] = re.sub("[^0-9]", "", row[fields[CATEGORY_LABS]])
            categoryPrefs["Teaching"] = re.sub("[^0-9]", "", row[fields[CATEGORY_TEACHING]])
            categoryPrefs["Assisting"] = re.sub("[^0-9]", "", row[fields[CATEGORY_ASSISTING]])
            categoryPrefs["Recitation"] = re.sub("[^0-9]", "", row[fields[CATEGORY_RECITATION]])
            categoryPrefs["MHC"] = re.sub("[^0-9]", "", row[fields[CATEGORY_MHC]])
            name = row[fields[NAME]]
            fullySupported = row[fields[FULLY_SUPPORTED]]
            if fullySupported == 'Yes':
                supportingProfessor = fields[SUPPORTING_PROFESSOR]
            else:
                supportingProfessor = "N/A"
            yearInSchool = row[fields[YEAR_IN_SCHOOL]]
            pureOrApplied = row[fields[PURE_OR_APPLIED]]
            qualifyingExams = sanitizeList(row[fields[QUALIFYING_EXAMS]])
            teachingPrefs = row[fields[TEACHING_PREF]].split(",")
            labPrefs = row[fields[LAB_PREF]].split(",")
            assistingPrefs = row[fields[ASSISTING_PREF]].split(",")
            recitationPrefs = row[fields[RECITATION_PREF]].split(",")
            dayPrefs = row[fields[DAY_PREF]]
            conflicts = getConflicts(row[fields[TIME_CONFLICT]].split(";"))
            computerSkills = row[fields[COMPUTER_SKILLS]]
            hoursCompleted = row[fields[HOURS_COMPLETED]]

            person = Person(name, fullySupported, supportingProfessor ,yearInSchool, pureOrApplied,
                            qualifyingExams, teachingPrefs, labPrefs, assistingPrefs,
                            recitationPrefs, categoryPrefs, conflicts, computerSkills, hoursCompleted)

            print(person.toString())

            people.append(person)
    return people


def parseCoursesFromPath(path):
    with open(path, newline='') as file:
        return parseCourses(file)


def parseCourses(file):
    courses = []
    fields = {}
    reader = csv.reader(file)
    next(reader)
    headers = next(reader)
    for i, field in enumerate(headers):
        fields[field] = i
    for row in reader:
        if row[0]:
            days = row[fields['Days']].strip()
            days = [day for day in days if days not in ['TBA', 'TBD', 'HONORS THESIS']]
            #This needs to be cleaned up to make better code & also generic
            hoursValue = 0
            if row[fields["Teach(12)"]] == 1:
                hoursValue = 12
            elif row[fields["Recitation(3)"]] == 1:
                hoursValue = 3
            elif row[fields["Assist(6)"]] == 1:
                hoursValue = 6
            elif row[fields["Lab(6)"]] == 1:
                hoursValue = 6
            course = Course(row[fields['Class']].strip(),  # course number
                            row[fields['Sec']].strip(),  # section
                            days,  # days
                            hoursValue,
                            parseTime(row[fields['Start Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # start time
                            parseTime(row[fields['End Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # end time
                            row[fields['Instructor']].strip(),  # instructor
                            row[fields['Category']]
                            )
            courses.append(course)
    return courses

def parseFacultyHoursFromPath(path):
    with open(path, newline='') as file:
        return parseFacultyHours(file)

def parseFacultyHours(file):
    #currently hardcoded for fall
    fields = {}
    fallFacultyLoadDict = {}
    springFacultyLoadDict = {}
    reader = csv.reader(file)
    headers = next(reader)
    for i, field in enumerate(headers):
        fields[field] = i
    for row in reader:
        if row[0]:
            professorName = row[fields['Professor Name']].strip()
            fallFacultyLoadDict[professorName] = row[fields['Fall']].strip()
            springFacultyLoadDict[professorName] = row[fields['Spring']].strip()
    return fallFacultyLoadDict, springFacultyLoadDict

# if __name__ == '__main__':
#     people = parsePeople('./static/data/formS2018.csv')
#     courses = parseCoursesFromPath('./static/data/s2018_schedule.csv')

    # for course in courses:
    #   print(course)
