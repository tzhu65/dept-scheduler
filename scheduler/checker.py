from .checkerConstants import *
import string

def check(courses, people):
  
  # Make set of courseNames that will be used to ensure every course is assigned
  courseNames = set([course.cse for course in courses])
  print("START: " + str(courseNames))

  for person in people:
    for course in courses:
      # Found a course that person is teaching
      if person.name == course.instructor:

        # Have to be on T/Th or M/W/F schedule, no in-between

        # Ensure sufficient computer skills
        if course.cse[-1:] == 'L':
          # If insufficient computer skill
          if (int(person.computerSkills) < 3):
            print("%s has computer skill: %s. %s requires computer skill: %s" %
              (person.name, person.computerSkills,
              course.cse, '3'))
            continue
        
        # Ensure sufficient qualification exams passed
        if course.cse in qualifyingExams:
          # If qualifying exam not fulfilled
          if qualifyingExams[course.cse] not in person.qualifyingExams:
            print("%s cannot teach %s, missing required qualifying exam: %s" %
              (person.name, course.cse, qualifyingExams[course.cse]))
            continue

        # 600-level courses must have passed appropriate COMP
        # if int(course.cse.strip(string.ascii_letters)) >= 600:

        # Ensure course is one of person's preferences
        if not any(course.cse in val for val in person.teachPrefs.values()):
          print("%s did not list %s as one of their preferences" %
            (person.name, course.cse))
          continue

        # We need course list to be empty at end, so if course is assigned correctly, remove it from list
        # TODO add catch KeyError exception
        courseNames.remove(course.cse)
        
  print("END: " + str(courseNames))

  # print(courses, people)