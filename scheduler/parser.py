"""Parse input csv files.

Parsed files include the schedule, TA preferences, and faculty hours spreadsheets. The purpose of this module is to
check for necessary information in each csv, as well as sanitize inputs.
"""

import csv
from datetime import datetime, time
import re
import typing

from .course import Course
from .parserConstants import ParserConstants, ParserFacultyHoursHeaders, ParserPreferencesHeaders, ParserScheduleHeaders
from .person import Person, PersonalConflict


# ================= #
# Custom Exceptions #
# ================= #

class MissingHeaders(Exception):
    """Customized exception for missing headers in a csv."""
    def __init__(self, message, headers):
        super().__init__(message)
        self.headers = headers


class ImproperNameFormat(Exception):
    """Customized exception for when a name cannot be parsed."""
    def __init__(self, message):
        super().__init__(message)


class ImproperTimeFormat(Exception):
    """Customized exception for when a time cannot be parsed."""
    def __init__(self, message):
        super().__init__(message)


# ======================= #
# Helper Parser Functions #
# ======================= #

def sanitizeName(name: str) -> str:
    """Convert a name into a standardized format.

    The name can be either `Last, First`, `First Last`, or ``.

    :param name: Name of a person in.
    :return: Name in `first last` format, or empty string.
    :raises ImproperNameFormat: The input cannot be parsed into a name.
    """
    sanitized = name
    correctFormat = False
    if ',' in name:
        nameParts = name.split(',')
        sanitizedList = nameParts[1], ' ', nameParts[0]
        sanitized = ''.join(sanitizedList)
        correctFormat = True
    elif ' ' in name:
        correctFormat = True

    if not correctFormat:
        raise ImproperNameFormat("Improper name format, got: %s" % name)

    return sanitized.lower().strip()


def parseList(text: str) -> typing.List[str]:
    """Convert a list string into a python list of strings.

    (1) Replaces every semicolon with a comma, (2) splits by the comma, (3) strips each element, and (4) adds to the
    list if the result is not an empty string.

    :param text: List of elements in string form, like preferences or qualification exams.
    :return: The parsed list of elements as a python list.
    """
    text = text.replace(';', ',')
    return [x for x in (map(lambda x: x.strip(), text.split(','))) if x != '']


def parseTime(timeStr: str, formats: typing.List[str]) -> time:
    """Convert a time in string form into a datetime object.

    :param timeStr: Time like `9:30AM` or `9:30 AM`.
    :param formats: List of formats to try to parse with, like `%I:%M%p` `%I:%M %p`.
    :return: Datetime object that represents the time.
    :raises ImproperTimeFormat: The input cannot be parsed into a time.
    """
    # Try different formats (sometimes it's '9:30AM', sometimes '9:30 AM')
    for fmt in formats:
        try:
            return datetime.strptime(timeStr, fmt).time()
        except ValueError:
            pass
    raise ImproperTimeFormat("Improper time format, got: %s" % timeStr)


def parseConflicts(listOfConflicts: typing.List[str]) -> typing.List[PersonalConflict]:
    """Parse time conflict strings.

    :param listOfConflicts: List of conflict times represented as strings.
    :return: List of conflict times as conflict objects.
    """
    conflicts = []
    for potentialConflicts in listOfConflicts:
        conflictParts = potentialConflicts.split(' ')

        if len(conflictParts) != 5 or conflictParts[3] != '-':
            return conflicts
        days = conflictParts[1] == 'MWF' or conflictParts[1] == 'TR'
        valdidNum = conflictParts[0].isdigit()
        if not days or not valdidNum:
            return conflicts
        conflict = PersonalConflict(conflictParts[0], conflictParts[1], conflictParts[2], conflictParts[4])
        conflicts.append(conflict)
    return conflicts


def addInstructorToHoursVal(dictRep: typing.Dict[str, int], lineOfInstr: str, hoursVal: int):
    """Gets all the instructors and assigns them an hour value.
    :param dictRep: Mapping of an instructor to an hour value.
    :param lineOfInstr: Semicolon separated list of instructors.
    :param hoursVal: Hours to associate with the instructor.
    """
    delimVal = lineOfInstr.split(';')
    for val in delimVal:
        dictRep[sanitizeName(val)] = hoursVal


def mapHeaders(headers: typing.List[str], expectedHeaders: typing.Set[str]) -> typing.Dict[str, int]:
    """Map the header fields to the index in the row.
    :param headers: A row of headers in the csv file.
    :param expectedHeaders: The headers that are expected to be passed in.
    :return: The mapping from header to the index of the row.
    :raises MissingHeaders: Expected headers not present in headers.
    """
    fields = {}
    for index, field in enumerate(headers):
        fields[field] = index
        expectedHeaders.discard(field)

    # Check if all expected headers are present
    if len(expectedHeaders) != 0:
        print(expectedHeaders)
        raise MissingHeaders("Expected headers.", expectedHeaders)
    return fields


# ================= #
# Parsing Functions #
# ================= #

def parsePeopleFromPath(path: str) -> typing.List[Person]:
    """Parse TA preferences from a temporary file.
    :param path: The path to the csv file.
    :return: List of people and their teaching preferences.
    :raises MissingHeaders: Expected headers not present in the csv.
    """
    with open(path, newline='') as file:
        return parsePeople(file)


def parsePeople(file: typing.IO) -> typing.List[Person]:
    """Parse TA preferences from a file in memory.
    :param file: The csv file handle.
    :return: List of people and their teaching preferences.
    :raises MissingHeaders: Expected headers not present in the csv.
    """
    expectedHeaders = {
        ParserPreferencesHeaders.ASSISTING_PREF,
        ParserPreferencesHeaders.CATEGORY_ASSISTING,
        ParserPreferencesHeaders.CATEGORY_LABS,
        ParserPreferencesHeaders.CATEGORY_MHC,
        ParserPreferencesHeaders.CATEGORY_RECITATION,
        ParserPreferencesHeaders.CATEGORY_TEACHING,
        ParserPreferencesHeaders.COMPUTER_SKILLS,
        ParserPreferencesHeaders.DAY_PREF,
        ParserPreferencesHeaders.FULLY_SUPPORTED,
        ParserPreferencesHeaders.HOURS_COMPLETED,
        ParserPreferencesHeaders.LAB_PREF,
        ParserPreferencesHeaders.NAME,
        ParserPreferencesHeaders.PURE_OR_APPLIED,
        ParserPreferencesHeaders.QUALIFYING_EXAMS,
        ParserPreferencesHeaders.RECITATION_PREF,
        ParserPreferencesHeaders.RETURNING,
        ParserPreferencesHeaders.SUPPORTING_PROFESSOR,
        ParserPreferencesHeaders.TEACHING_PREF,
        ParserPreferencesHeaders.TIME_CONFLICT,
        ParserPreferencesHeaders.YEAR_IN_SCHOOL,
    }

    people = []
    reader = csv.reader(file)
    headers = next(reader)
    fields = mapHeaders(headers, expectedHeaders)

    # Loop through all the people
    for row in reader:

        # If has a datetime and is returning next semester, then create the person
        if row[0] and row[fields[ParserPreferencesHeaders.RETURNING]] != ParserConstants.NO:

            name = sanitizeName(row[fields[ParserPreferencesHeaders.NAME]])

            # Preferences
            categoryPrefs = {}
            categoryPrefs[ParserConstants.CATEGORY_PREFS_LABS] = re.sub(
                "[^0-9]", "", row[fields[ParserPreferencesHeaders.CATEGORY_LABS]])
            categoryPrefs[ParserConstants.CATEGORY_PREFS_TEACHING] = re.sub(
                "[^0-9]", "", row[fields[ParserPreferencesHeaders.CATEGORY_TEACHING]])
            categoryPrefs[ParserConstants.CATEGORY_PREFS_ASSISTING] = re.sub(
                "[^0-9]", "", row[fields[ParserPreferencesHeaders.CATEGORY_ASSISTING]])
            categoryPrefs[ParserConstants.CATEGORY_PREFS_RECITATION] = re.sub(
                "[^0-9]", "", row[fields[ParserPreferencesHeaders.CATEGORY_RECITATION]])
            categoryPrefs[ParserConstants.CATEGORY_PREFS_MHC] = re.sub(
                "[^0-9]", "", row[fields[ParserPreferencesHeaders.CATEGORY_MHC]])
            teachingPrefs = parseList(row[fields[ParserPreferencesHeaders.TEACHING_PREF]])
            labPrefs = parseList(row[fields[ParserPreferencesHeaders.LAB_PREF]])
            assistingPrefs = parseList(row[fields[ParserPreferencesHeaders.ASSISTING_PREF]])
            recitationPrefs = parseList(row[fields[ParserPreferencesHeaders.RECITATION_PREF]])
            dayPrefs = row[fields[ParserPreferencesHeaders.DAY_PREF]]

            # Supporting professor
            fullySupported = row[fields[ParserPreferencesHeaders.FULLY_SUPPORTED]]
            supportingProfessor = "N/A"
            if fullySupported == ParserConstants.YES:
                # TODO: NEEDS TO BE different this is a band-aid
                if isinstance(fields[ParserPreferencesHeaders.SUPPORTING_PROFESSOR], str):
                    supportingProfessor = sanitizeName(fields[ParserPreferencesHeaders.SUPPORTING_PROFESSOR])

            # Seniority
            yearInSchool = int(row[fields[ParserPreferencesHeaders.YEAR_IN_SCHOOL]]) \
                if row[fields[ParserPreferencesHeaders.YEAR_IN_SCHOOL]] != '' else 0

            # Hours bought out of
            try:
                hoursBoughtOut = int(re.search(r'\d+', row[fields[ParserPreferencesHeaders.HOURS_BOUGHT_OUT]]).group())
            except:
                hoursBoughtOut = 0

            pureOrApplied = row[fields[ParserPreferencesHeaders.PURE_OR_APPLIED]]
            qualifyingExams = parseList(row[fields[ParserPreferencesHeaders.QUALIFYING_EXAMS]])
            conflicts = parseConflicts(row[fields[ParserPreferencesHeaders.TIME_CONFLICT]].split(";"))
            computerSkills = row[fields[ParserPreferencesHeaders.COMPUTER_SKILLS]]
            hoursCompleted = row[fields[ParserPreferencesHeaders.HOURS_COMPLETED]]

            # Convert hours completed to a number
            if hoursCompleted.isdigit():
                hoursCompleted = int(hoursCompleted)
            else:
                hoursCompleted = 0

            # Convert computer skills to a number
            if computerSkills in ParserConstants.COMPUTER_SKILLS:
                computerSkills = ParserConstants.COMPUTER_SKILLS[computerSkills]
            else:
                computerSkills = ParserConstants.COMPUTER_SKILLS_NONE

            person = Person(name, fullySupported, supportingProfessor, yearInSchool, pureOrApplied, qualifyingExams,
                            teachingPrefs, labPrefs, assistingPrefs, recitationPrefs, categoryPrefs, conflicts,
                            computerSkills, hoursCompleted, hoursBoughtOut)
            people.append(person)

    return people


def parseCoursesFromPath(path: str) -> typing.List[Course]:
    """Parse the schedule from a temporary file.
    :param path: The path to the csv file.
    :return: List of courses.
    :raises MissingHeaders: Expected headers not present in the csv.
    """
    with open(path, newline='') as file:
        return parseCourses(file)


def parseCourses(file: typing.IO) -> typing.List[Course]:
    """Parse the schedule from a file in memory.
    :param file: The csv file handle.
    :return: List of courses.
    :raises MissingHeaders: Expected headers not present in the csv.
    """
    expectedHeaders = {
        ParserScheduleHeaders.ASSIST_COUNT,
        ParserScheduleHeaders.ASSISTING_ASSIGNMENT,
        ParserScheduleHeaders.BUILDING,
        ParserScheduleHeaders.CLASS,
        ParserScheduleHeaders.CLASS_NUMBER,
        ParserScheduleHeaders.DAYS,
        ParserScheduleHeaders.END_TIME,
        ParserScheduleHeaders.ENROLL_CAP,
        ParserScheduleHeaders.INSTRUCTOR,
        ParserScheduleHeaders.LAB_COUNT,
        ParserScheduleHeaders.RECITATION_COUNT,
        ParserScheduleHeaders.ROOM,
        ParserScheduleHeaders.ROOM_CAP,
        ParserScheduleHeaders.SECTION,
        ParserScheduleHeaders.START_TIME,
        ParserScheduleHeaders.TEACH_COUNT,
    }
    courses = []
    reader = csv.reader(file)
    next(reader)
    headers = next(reader)
    fields = mapHeaders(headers, expectedHeaders)
    with open('persons.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(headers)
        for row in reader:
            filewriter.writerow(row)
            if row[0]:

                # Skip a row if its length isn't long enough
                if len(row) == 1:
                    continue

                days = row[fields[ParserScheduleHeaders.DAYS]].strip()
                days = [day for day in days if days not in ['TBA', 'TBD', 'HONORS THESIS']]
                # This needs to be cleaned up to make better code and also generic
                # Dictionary of the open positions (i.e. {teach: 1, recitation: 2})
                positions = {}
                # Dictionary of instructor name to an assigned hours value for the course
                instructorToHoursVal = {}
                hoursValue = 0

                # Values for the row
                teachVal = int(row[fields[ParserScheduleHeaders.TEACH_COUNT]]) if \
                    row[fields[ParserScheduleHeaders.TEACH_COUNT]] else 0
                recitationVal = int(row[fields[ParserScheduleHeaders.RECITATION_COUNT]]) if \
                    row[fields[ParserScheduleHeaders.RECITATION_COUNT]] else 0
                assistVal = int(row[fields[ParserScheduleHeaders.ASSIST_COUNT]]) if \
                    row[fields[ParserScheduleHeaders.ASSIST_COUNT]] else 0
                labVal = int(row[fields[ParserScheduleHeaders.LAB_COUNT]]) if \
                    row[fields[ParserScheduleHeaders.LAB_COUNT]] else 0
                instructor = row[fields[ParserScheduleHeaders.INSTRUCTOR]] if \
                    row[fields[ParserScheduleHeaders.INSTRUCTOR]] else ""
                assistant = row[fields[ParserScheduleHeaders.ASSISTING_ASSIGNMENT]] if \
                    row[fields[ParserScheduleHeaders.ASSISTING_ASSIGNMENT]] else ""

                if instructor != "" and (teachVal+recitationVal+assistVal+labVal) == 0:
                    # Only an instructor and no graduate students
                    addInstructorToHoursVal(instructorToHoursVal, instructor, 0)
                elif instructor != "" and teachVal == 1:
                    # A graduate student instructing a course
                    addInstructorToHoursVal(instructorToHoursVal, instructor, 12)
                    if recitationVal > 0:
                        addInstructorToHoursVal(instructorToHoursVal, assistant, 3)
                    elif assistVal > 0:
                        addInstructorToHoursVal(instructorToHoursVal, assistant, 6)
                    elif labVal > 0:
                        addInstructorToHoursVal(instructorToHoursVal, assistant, 6)
                elif instructor != "" and assistant == "":
                    if recitationVal > 0:
                        addInstructorToHoursVal(instructorToHoursVal, instructor, 3)
                    elif assistVal > 0:
                        addInstructorToHoursVal(instructorToHoursVal, instructor, 6)
                    elif labVal > 0:
                        addInstructorToHoursVal(instructorToHoursVal, instructor, 6)

                # Standardize the keys for positions
                positions[ParserConstants.POSITION_TEACH] = {"hours": 12, "amount": teachVal}
                positions[ParserConstants.POSITION_RECITATION] = {"hours": 3, "amount": recitationVal}
                positions[ParserConstants.POSITION_ASSIST] = {"hours": 6, "amount": assistVal}
                positions[ParserConstants.POSITION_LAB] = {"hours": 6, "amount": labVal}

                try:
                    instructorName = sanitizeName(row[fields[ParserScheduleHeaders.INSTRUCTOR]])
                except ImproperNameFormat:
                    instructorName = ''

                try:
                    startTime = parseTime(row[fields[ParserScheduleHeaders.START_TIME]].strip(),
                                          ['%I:%M %p', '%I:%M%p'])
                except ImproperTimeFormat:
                    startTime = 'N/A'

                try:
                    endTime = parseTime(row[fields[ParserScheduleHeaders.END_TIME]].strip(), ['%I:%M %p', '%I:%M%p'])
                except ImproperTimeFormat:
                    endTime = 'N/A'

                course = Course(row[fields[ParserScheduleHeaders.CLASS]].strip(),  # Course number
                                row[fields[ParserScheduleHeaders.SECTION]].strip(),  # Section
                                days,
                                positions,
                                startTime,
                                endTime,
                                instructorName,
                                hoursValue,
                                instructorToHoursVal
                                )
                courses.append(course)

    return courses


def parseFacultyHoursFromPath(path: str) -> typing.Tuple[typing.Dict[str, int], typing.Dict[str, int]]:
    """Parse the hours each faculty member has for teaching.
    :param path: The path to the csv file.
    :return: A tuple of two dictionaries (fall and spring) that map the professor's name to the hours.
    :raises MissingHeaders: Expected headers not present in the csv.
    """
    with open(path, newline='') as file:
        return parseFacultyHours(file)


def parseFacultyHours(file: typing.IO) -> typing.Tuple[typing.Dict[str, int], typing.Dict[str, int]]:
    """Parse the hours each faculty member has for teaching.
    :param file: The csv file handle.
    :return: A tuple of two dictionaries (fall and spring) that map the professor's name to the hours.
    :raises MissingHeaders: Expected headers not present in the csv.
    """
    expectedHeaders = {
        ParserFacultyHoursHeaders.FALL,
        ParserFacultyHoursHeaders.PROFESSOR_NAME,
        ParserFacultyHoursHeaders.SPRING,
    }
    fallFacultyLoadDict = {}
    springFacultyLoadDict = {}
    reader = csv.reader(file)
    headers = next(reader)
    fields = mapHeaders(headers, expectedHeaders)

    for row in reader:
        if row[0]:
            professorName = sanitizeName(row[fields[ParserFacultyHoursHeaders.PROFESSOR_NAME]])

            fallHoursStr = row[fields[ParserFacultyHoursHeaders.FALL]].strip()
            fallHours = int(fallHoursStr) if fallHoursStr.isdigit() else 0
            fallFacultyLoadDict[professorName] = fallHours

            springHoursStr = row[fields[ParserFacultyHoursHeaders.SPRING]].strip()
            springHours = int(springHoursStr) if springHoursStr.isdigit() else 0
            springFacultyLoadDict[professorName] = springHours

    return fallFacultyLoadDict, springFacultyLoadDict
