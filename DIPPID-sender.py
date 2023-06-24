import socket, time, json, random
from typing import TypedDict


class Event:

  T_Input_State = TypedDict('event', { 'type': str, 'x': float, 'y': float }) # instead of 'event' number?

  def __init__(self) -> None:
    self.x, self.y, self.type = 0, 0, None


  def update(self, counter: int) -> None:
    # check detected events / touch input from touch-input.py
    return
  
  def to_dict(self) -> T_Input_State:
    return {
        "type": self.type,
        "x": "{0:,.2f}".format(self.x),
        "y": "{0:,.2f}".format(self.y),
      }


IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

TICKS_PER_SEC = 10
LOOP_INTERVAL = 1 / TICKS_PER_SEC
COUNTER = 0
  
random.seed(time.time())

# init of events?
events = Event()

while True:
  one_sec_mark = COUNTER % TICKS_PER_SEC == 0

  # events function
  # result should look like this, x and y normalized
  # {'events' :
  #   {0 : {'type' : 'touch/hover',
  #         'x' : float,
  #         'y' : float},
  #    1 : {'type' : 'touch/hover',
  #         'x' : float,
  #         'y' : float},
  #   ...}
  # }


  message = json.dumps({ "events": events.to_dict()})

  sock.sendto(message.encode(), (IP, PORT))

  COUNTER += 1
  time.sleep(LOOP_INTERVAL)