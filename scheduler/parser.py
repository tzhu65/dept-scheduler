import csv
import re
from datetime import datetime
from .person import Person
from .person import Conflict
from .course import Course
from .parserConstants import *


class MissingHeaders(Exception):
    def __init__(self, message, headers):
        super().__init__(message)
        self.headers = headers

class ImproperNameFormat(Exception):
    def __init__(self, message):
        super().__init__(message)

def sanitizeName(name):
    #Expect either 'Last, First' or 'First Last' as input
    expectValueToBeOne = 0
    sanitized = name
    if ',' in name:
        nameParts = name.split(',')
        sanitizedList = nameParts[1] , ' ' ,nameParts[0]
        sanitized = ''.join(sanitizedList)
        expectValueToBeOne = 1
    elif ' ' in name:
        expectValueToBeOne = 1

    if expectValueToBeOne!=1:
        raise ImproperNameFormat("Improper name format, Expect either 'Last, First' or 'First Last' as input ")
    return sanitized.lower().strip()


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
    # Expected headers
    expectedHeaders = {
        RETURNING,
        CATEGORY_LABS,
        CATEGORY_TEACHING,
        CATEGORY_ASSISTING,
        CATEGORY_RECITATION,
        CATEGORY_MHC,
        NAME,
        FULLY_SUPPORTED,
        SUPPORTING_PROFESSOR,
        YEAR_IN_SCHOOL,
        PURE_OR_APPLIED,
        QUALIFYING_EXAMS,
        TEACHING_PREF,
        LAB_PREF,
        ASSISTING_PREF,
        RECITATION_PREF,
        DAY_PREF,
        TIME_CONFLICT,
        COMPUTER_SKILLS,
        HOURS_COMPLETED,
    }

    people = []
    fields = {}
    reader = csv.reader(file)
    headers = next(reader)
    for index, field in enumerate(headers):
        fields[field] = index
        expectedHeaders.discard(field)

    # Check if all expected headers are present
    if len(expectedHeaders) != 0:
        raise MissingHeaders("Expected headers.", expectedHeaders)

    # Loop through all the people
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
            name = sanitizeName(row[fields[NAME]])
            fullySupported = row[fields[FULLY_SUPPORTED]]
            if fullySupported == 'Yes':
                supportingProfessor = sanitizeName(fields[SUPPORTING_PROFESSOR])
            else:
                supportingProfessor = "N/A"
            yearInSchool = int(row[fields[YEAR_IN_SCHOOL]]) if row[fields[YEAR_IN_SCHOOL]] != '' else 0
            try:
                hoursBoughtOut = int(re.search(r'\d+', row[fields[HOURS_BOUGHT_OUT]]).group())
            except:
                hoursBoughtOut = 0
            pureOrApplied = row[fields[PURE_OR_APPLIED]]
            qualifyingExams = sanitizeList(row[fields[QUALIFYING_EXAMS]])
            teachingPrefs = sanitizeList(row[fields[TEACHING_PREF]])
            labPrefs = sanitizeList(row[fields[LAB_PREF]])
            assistingPrefs = sanitizeList(row[fields[ASSISTING_PREF]])
            recitationPrefs = sanitizeList(row[fields[RECITATION_PREF]])
            dayPrefs = row[fields[DAY_PREF]]
            conflicts = getConflicts(row[fields[TIME_CONFLICT]].split(";"))
            computerSkills = row[fields[COMPUTER_SKILLS]]
            hoursCompleted = row[fields[HOURS_COMPLETED]]

            # Convert hours completed to a number
            if hoursCompleted.isdigit():
                hoursCompleted = int(hoursCompleted)

            # Convert computer skills to a number
            if computerSkills in SKILLS:
                computerSkills = SKILLS[computerSkills]
            else:
                computerSkills = 0

            person = Person(name, fullySupported, supportingProfessor ,yearInSchool, pureOrApplied,
                            qualifyingExams, teachingPrefs, labPrefs, assistingPrefs,
                            recitationPrefs, categoryPrefs, conflicts, computerSkills, hoursCompleted, hoursBoughtOut)

            # print(person.toString())

            people.append(person)
    return people


def parseCoursesFromPath(path):
    with open(path, newline='') as file:
        return parseCourses(file)


def parseCourses(file):
    expectedHeaders = {
        'Class',
        'Sec',
        'Class #',
        'Days',
        'Bldg',
        'Rm',
        'Rm Cap',
        'Enroll Cap',
        'Assisting Assignment',
        'Teach(12)',
        'Recitation(3)',
        'Assist(6)',
        'Start Time',
        'End Time',
        'Instructor'
    }
    courses = []
    fields = {}
    reader = csv.reader(file)
    next(reader)
    headers = next(reader)
    for i, field in enumerate(headers):
        fields[field] = i
        expectedHeaders.discard(field)

    # Check if all expected headers are present
    if len(expectedHeaders) != 0:
        raise MissingHeaders("Expected headers.", expectedHeaders)

    for row in reader:
        if row[0]:

            # Skip a row if it's length isn't long enough
            if len(row) == 1:
                continue

            days = row[fields['Days']].strip()
            days = [day for day in days if days not in ['TBA', 'TBD', 'HONORS THESIS']]
            #This needs to be cleaned up to make better code & also generic
            # Dictionary of the open positions (i.e. {teach: 1, recitation: 2})
            positions = {}
            #Dictionary of instructor name to an assigned hours value for the course
            instructorToHoursVal = {}
            hoursValue = 0
            if row[fields["Teach(12)"]] and int(row[fields["Teach(12)"]]) > 0:
                positions["teach"] = {"hours": 12, "amount": int(row[fields["Teach(12)"]])}
                hoursValue = 12
                addInstructorToHoursVal(instructorToHoursVal,row[fields['Instructor']],hoursValue)
            if row[fields["Recitation(3)"]] and int(row[fields["Recitation(3)"]]) > 0:
                positions["recitation"] = {"hours": 3, "amount": int(row[fields["Recitation(3)"]])}
                hoursValue = 3
                addInstructorToHoursVal(instructorToHoursVal,row[fields['Assisting Assignment']],hoursValue)
            if row[fields["Assist(6)"]] and int(row[fields["Assist(6)"]]) > 0:
                positions["assist"] = {"hours": 6, "amount": int(row[fields["Assist(6)"]])}
                hoursValue = 6
                addInstructorToHoursVal(instructorToHoursVal,row[fields['Assisting Assignment']],hoursValue)
            if row[fields["Lab(6)"]] and int(row[fields["Lab(6)"]]) > 0:
                positions["lab"] = {"hours": 6, "amount": int(row[fields["Lab(6)"]])}
                hoursValue = 6
                addInstructorToHoursVal(instructorToHoursVal,row[fields['Assisting Assignment']],hoursValue)
            if len(positions) == 0:
                #Just one instructor
                addInstructorToHoursVal(instructorToHoursVal,row[fields['Instructor']],0)
            course = Course(row[fields['Class']].strip(),  # course number
                            row[fields['Sec']].strip(),  # section
                            days,  # days
                            positions,
                            parseTime(row[fields['Start Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # start time
                            parseTime(row[fields['End Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # end time
                            row[fields['Instructor']].strip(),  # instructor
                            hoursValue,
                            instructorToHoursVal
                            )
            courses.append(course)
    return courses

def addInstructorToHoursVal(dictRep, lineOfInstr, hoursVal):
    delimVal = getListOfDelimWord(lineOfInstr, ';')
    for val in delimVal:
        dictRep[sanitizeName(val)] = hoursVal

def getListOfDelimWord(word, delimVal):
    delimList = word.split(delimVal)
    return delimList

def parseFacultyHoursFromPath(path):
    with open(path, newline='') as file:
        return parseFacultyHours(file)

def parseFacultyHours(file):
    expectedHeaders = {
        'Professor Name',
        'Fall',
        'Spring',
    }
    #currently hardcoded for fall
    fields = {}
    fallFacultyLoadDict = {}
    springFacultyLoadDict = {}
    reader = csv.reader(file)
    headers = next(reader)
    for i, field in enumerate(headers):
        fields[field] = i
        expectedHeaders.discard(field)

    # Check if all expected headers are present
    if len(expectedHeaders) != 0:
        raise MissingHeaders("Expected headers.", expectedHeaders)

    for row in reader:
        if row[0]:
            professorName = sanitizeName(row[fields['Professor Name']]).strip().lower()
            fallFacultyLoadDict[professorName] = row[fields['Fall']].strip()
            springFacultyLoadDict[professorName] = row[fields['Spring']].strip()
            print(professorName,fallFacultyLoadDict[professorName],springFacultyLoadDict[professorName])
    return fallFacultyLoadDict, springFacultyLoadDict

# if __name__ == '__main__':
#     people = parsePeople('./static/data/formS2018.csv')
#     courses = parseCoursesFromPath('./static/data/s2018_schedule.csv')

    # for course in courses:
    #   print(course)
