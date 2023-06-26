import socket, time, json, random
from typing import TypedDict


class Event:

  T_Input_State = TypedDict('event', { 'type': str, 'x': float, 'y': float }) # instead of 'event' number?

  def __init__(self) -> None:
    self.events, self.counter, self.x, self.y, self.type = [], 0, 0, 0, None


  def update(self, counter: int) -> None:
    # check detected events / touch input from touch-input.py
    return
  
  def to_dict(self) -> T_Input_State:
    return { self.counter:
        {
          "type": self.type,
          "x": "{0:,.2f}".format(self.x),
          "y": "{0:,.2f}".format(self.y),
        }
      }
