import csv
from person import Person
from course import Course

people = []
fields = {}

with open('./static/data/s2018.csv', newline='') as file:
  reader = csv.reader(file)
  headers = next(reader)
  for i, field in enumerate(headers):
    fields[field] = i
  for row in reader:
    if row[0]:
      person = Person(row[fields['Name']])
      people.append(person)

courses = []
fields = {}

with open('./static/data/s2018_schedule.csv', newline='') as file:
  reader = csv.reader(file)
  next(reader)
  headers = next(reader)
  for i, field in enumerate(headers):
    fields[field] = i
  for row in reader:
    if row[0]:
      course = Course(row[fields['Instructor']])
      courses.append(course)
  