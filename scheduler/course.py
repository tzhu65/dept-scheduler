class Course:

  def __init__(self, courseNumber, section, days, types, startTime, endTime, instructor, category):
    self.courseNumber = courseNumber
    self.section = section
    self.days = days
    self.types = types
    self.startTime = startTime
    self.endTime = endTime
    self.instructor = instructor
    self.category = category
    self.hoursVal = 0

  def __str__(self):
    return '%5s' % self.courseNumber + ' ' + \
      '%6s' % self.section + ' ' + \
      '%18s' % str(self.days) + ' ' + \
      '%18s' % str(self.types) + ' ' + \
      '%10s' % self.startTime + ' ' + \
      '%10s' % self.endTime + '   ' + \
      '%10s' % self.category + '   ' + \
      self.instructor
