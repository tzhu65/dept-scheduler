import csv
from person import Person

people = []
fields = {}

with open('./static/data/s2018.csv', newline='') as file:
    reader = csv.reader(file)
    headers = next(reader)
    for i, field in enumerate(headers):
      fields[field] = i
    for row in reader:
      person = Person(row[fields['Name']])
      people.append(person)