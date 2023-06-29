class Event:

  def __init__(self) -> None:
    self.events = []
    self.eventsDict = {'events': {}}
    self.type = None
    self.counter, self.x, self.y = 0, 0, 0


  def update(self, x, y, inputType) -> None:
    self.x = x
    self.y = y
    self.type = inputType
    self.to_dict()
    self.counter += 1
  
  def to_dict(self):
      self.eventsDict['events'][self.counter] = {
          "type": self.type,
          "x": "{0:,.2f}".format(self.x),
          "y": "{0:,.2f}".format(self.y),
        }
