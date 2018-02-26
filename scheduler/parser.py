import csv
from datetime import datetime
from .person import Person
from .person import Conflict
from .course import Course
from .parserConstants import *


def sanitizeList(text):
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
        if row[0] and row[fields[RETURNING_2018]] != 'No':
            # get all data besides the conflicts
            teachPrefs = {}
            name = row[fields[NAME]]
            yearInSchool = int(row[fields[YEAR]])
            exams = sanitizeList(row[fields[EXAMS]])
            currHours = int(row[fields[CURRENT_HOURS]])
            availHours = int(row[fields[AVAILABLE_HOURS]])
            teachPrefs[1] = row[fields[TEACHING_PREF_1]].split(",")
            teachPrefs[2] = row[fields[TEACHING_PREF_2]].split(",")
            assitancePref = row[fields[ASSISTANCE_PREF]].split(",")
            recitationPref = row[fields[RECITATION_PREF]].split(",")
            categoryPref = row[fields[PREFERED_CATEGORY]].split(",")
            leastPrefCategory = row[fields[LEAST_PREFERED_CATEGORY]].split(",")
            conflicts = getConflicts(row, fields)
            person = Person(name, yearInSchool, exams, currHours, availHours,
                            teachPrefs, assitancePref, recitationPref,
                            categoryPref, leastPrefCategory, conflicts)

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
