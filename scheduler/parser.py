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


def getConflicts(row, fields):
    index = 0
    conflicts = []
    if (row[fields[TIME_CONFLICT]] == "NO"):
        return conflicts
    i = 1
    while True:
        day = row[fields[CONFLICT_DAY + str(i)]]
        time = row[fields[CONFLICT_TIME + str(i)]].split("-")
        conflict = Conflict(day, time[0], time[1])
        conflicts.append(conflict)
        nextval = ADDITIONAL_CONFLICT + str(i)
        if row[fields[nextval]] == "No":
            break
        i += 1;
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
            yearInSchool = row[fields[YEAR_IN_SCHOOL]]
            pureOrApplied = row[fields[PURE_OR_APPLIED]]
            qualifyingExams = sanitizeList(row[fields[QUALIFYING_EXAMS]])
            teachingPrefs = row[fields[TEACHING_PREF]].split(",")
            labPrefs = row[fields[LAB_PREF]].split(",")
            assistingPrefs = row[fields[ASSISTING_PREF]].split(",")
            recitationPrefs = row[fields[RECITATION_PREF]].split(",")
            dayPrefs = row[fields[DAY_PREF]]
            # conflicts = getConflicts(row, fields)
            computerSkills = row[fields[COMPUTER_SKILLS]]
            
            person = Person(name, fullySupported, yearInSchool, pureOrApplied,
                            qualifyingExams, teachingPrefs, labPrefs, assistingPrefs,
                            recitationPrefs, categoryPrefs, "", computerSkills)

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
            course = Course(row[fields['Cse']].strip(),  # course number
                            row[fields['Sec']].strip(),  # section
                            days,  # days
                            parseTime(row[fields['Start Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # start time
                            parseTime(row[fields['End Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # end time
                            row[fields['Instructor']].strip())  # instructor
            courses.append(course)
    return courses


# if __name__ == '__main__':
#     people = parsePeople('./static/data/formS2018.csv')
#     courses = parseCoursesFromPath('./static/data/s2018_schedule.csv')

    # for course in courses:
    #   print(course)
