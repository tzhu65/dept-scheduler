class Course:

  def __init__(self, courseNumber, section, days, positions, startTime, endTime, instructor, category, hoursValue):
    self.courseNumber = courseNumber
    self.section = section
    self.days = days
    self.positions = positions      # Dictionary of the open positions (i.e. {teach: 1, recitation: 2})
    self.startTime = startTime
    self.endTime = endTime
    self.instructor = instructor
    self.category = category        # Type of course when generating the graph (i.e. teach, recitation, lab, etc.)
    self.hoursValue = hoursValue

  def __str__(self):
    return '%5s' % self.courseNumber + ' ' + \
      '%6s' % self.section + ' ' + \
      '%18s' % str(self.days) + ' ' + \
      '%18s' % str(self.positions) + ' ' + \
      '%10s' % self.startTime + ' ' + \
      '%10s' % self.endTime + '   ' + \
      '%10s' % self.category + '   ' + \
      self.instructor
