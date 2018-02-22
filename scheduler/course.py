class Course:
  
  def __init__(self, cse, section, days, startTime, endTime, instructor):
    self.cse = cse
    self.section = section
    self.days = days
    self.startTime = startTime
    self.endTime = endTime
    self.instructor = instructor

  def __str__(self):
    return '%5s' % self.cse + ' ' + \
      '%6s' % self.section + ' ' + \
      '%18s' % str(self.days) + ' ' + \
      '%10s' % self.startTime + ' ' + \
      '%10s' % self.endTime + '   ' + \
      self.instructor