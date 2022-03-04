import elevator as Elevator


class ElevatorSystem:
    """A elevator system class.
    The Elevator System keeps the state of the list of elevators and the current floors requested.
  Parameters
  ----------
  elevator_config : list[capacity, floors/minute]
      tells how many elevators and what are the characteristics of the elevators
  Attributes
  ----------
    floors_requested : set
         tells the floors where an elevator was requested
    elevators : list[elevator]
        gives the list of current elevators
   
  """
    def __init__(self, elevators_config):
        self.elevators = []
        self.floors_requested = set()
        for ev in elevators_config:
            self.elevators.append(Elevator.Elevator(ev[0], ev[1]))
