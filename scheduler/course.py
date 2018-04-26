class Course:

    def __init__(self, courseNumber, section, days, positions, startTime, endTime, instructor, hoursValue,
                 instructorToHoursVal, assistants):
        self.courseNumber = courseNumber
        self.section = section
        self.days = days
        self.positions = positions      # Dictionary of the open positions (i.e. {teach: 1, recitation: 2})
        self.startTime = startTime
        self.endTime = endTime
        self.instructor = instructor
        self.hoursValue = hoursValue
        self.instructorToHoursVal = instructorToHoursVal
        self.assistants = assistants
        self.recitationCount = 0    # Count of other recitations of the same section type (for generation)

    def __str__(self):
        return '%5s' % self.courseNumber + ' ' + \
          '%6s' % self.section + ' ' + \
          '%18s' % str(self.days) + ' ' + \
          '%18s' % str(self.positions) + ' ' + \
          '%10s' % self.startTime + ' ' + \
          '%10s' % self.endTime + '   ' + \
          '%10s' % self.instructorToHoursVal + '   ' + \
          self.instructor
