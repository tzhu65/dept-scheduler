class Course:

  def __init__(self, courseNumber, section, days, hoursValue ,startTime, endTime, instructor, category):
    self.courseNumber = courseNumber
    self.section = section
    self.days = days
    self.hoursValue = hoursValue
    self.startTime = startTime
    self.endTime = endTime
    self.instructor = instructor
    self.category = category

  def __str__(self):
    return '%5s' % self.courseNumber + ' ' + \
      '%6s' % self.section + ' ' + \
      '%18s' % str(self.days) + ' ' + \
      '%18s' % str(self.hoursValue) + ' ' + \
      '%10s' % self.startTime + ' ' + \
      '%10s' % self.endTime + '   ' + \
      '%10s' % self.category + '   ' + \
      self.instructor
