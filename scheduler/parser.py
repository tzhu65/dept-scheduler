import csv
from datetime import datetime
from person import Person
from course import Course

def sanitizeList(text):
  return [x for x in (map(lambda x:x.strip(), text.split(','))) if x != '']

def parseTime(time, formats):
  # try different formats (sometimes it's '9:30AM', sometimes '9:30 AM')
  for format in formats:
    try:
      return datetime.strptime(time, format).time()
    except ValueError:
      pass
  return 'N/A'

def parsePeople(path):
  people = []
  fields = {}
  with open(path, newline='') as file:
    reader = csv.reader(file)
    headers = next(reader)
    for i, field in enumerate(headers):
      fields[field] = i
    print(headers)
    for row in reader:
      # if has a datetime and are returning next semester, then we create person object
      if row[0] and row[fields['Will you be returning in Spring 2018?']] != 'No':
        teachPrefs = {}
        teachPrefs[1] = sanitizeList(row[fields['teachPref1']])
        teachPrefs[2] = sanitizeList(row[fields['teachPref2']])
        person = Person(row[fields['Name']],                                                    # name
                        6 if row[fields['What year will you be in Spring 2018?']] == '>5'       # year
                          else int(row[fields['What year will you be in Spring 2018?']]),
                        sanitizeList(row[fields['Qualifying exams passed to date?']]),          # exams
                        -1 if not row[fields['currentHours']].strip().isnumeric()               # current hours
                          else int(row[fields['currentHours']].strip()),
                        -1 if not row[fields['availableHours']].strip().isnumeric()             # available hours
                          else int(row[fields['availableHours']].strip()),
                        teachPrefs,                                                             # teaching preferences
                        sanitizeList(row[fields['assistPref']]),                                # assisting preferences
                        sanitizeList(row[fields['recitationPref']]),                            # recitation preferences
                        [x for x in ['assisting', 'teaching', 'recitation', 'Math Help Center'] # category preferences
                          if x in row[fields['categoryPref']]],
                        [x for x in ['assisting', 'teaching', 'recitation', 'Math Help Center'] # category least preferences
                          if x in row[fields['categoryLeastPref']]]
                        )
        print(person.categoryLeastPrefs)
        people.append(person)
  return people

def parseCourses(path):
  courses = []
  fields = {}
  with open(path, newline='') as file:
    reader = csv.reader(file)
    next(reader)
    headers = next(reader)
    for i, field in enumerate(headers):
      fields[field] = i
    for row in reader:
      if row[0]:
        days = row[fields['Days']].strip()
        days = [day for day in days if days not in ['TBA', 'TBD', 'HONORS THESIS']]
        course = Course(row[fields['Cse']].strip(),                                             # course number
                        row[fields['Sec']].strip(),                                             # section
                        days,                                                                   # days
                        parseTime(row[fields['Start Time']].strip(), ['%I:%M %p', '%I:%M%p']),  # start time
                        parseTime(row[fields['End Time']].strip(), ['%I:%M %p', '%I:%M%p']),    # end time
                        row[fields['Instructor']].strip())                                      # instructor
        courses.append(course)
  return courses

if __name__ == '__main__':
  people = parsePeople('./static/data/s2018.csv')
  courses = parseCourses('./static/data/s2018_schedule.csv')
  # for course in courses:
  #   print(course)