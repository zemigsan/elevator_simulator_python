from collections import deque


class Elevator:
  """A elevator class.

    The Elevator class manages the state of an elevator. It is time agnostic 
    and just represents the current state of the elevator. The elevator can 
    hold a certain capacity of people and moves at a certain speed.
    
    When occupants are added, their destination floors should be specified, 
    and the elevator will keep track of which floors have been requested. 
    The elevator will also track a queue of floors to stop at in order.

    Raises ValueError if an attempt is made to add more occupants than 
    the elevator can hold, or remove more occupants than are present.
    """

  def __init__(self,
               capacity: int,
               floors_per_minute: float,
               current_floor: float = 0) -> None:
    self.capacity = capacity
    self.floors_per_minute = floors_per_minute
    self.current_floor = current_floor
    self.requested_floors = set()
    self.floors_queue = deque()
    self.current_capacity = 0

  @property
  def free_capacity(self) -> int:
    return self.capacity - self.current_capacity

  def add_occupants(self, number_people: int, floor_destination: int) -> None:
    if self.free_capacity < number_people:
      raise ValueError("Not enough room in the elevator.")
    self.requested_floors.add(floor_destination)
    self.current_capacity += number_people

  def remove_occupants(self, number_people: int) -> None:
    if self.current_capacity < number_people:
      raise ValueError("Not enough occupants in the elevator.")
    self.current_capacity -= number_people
    if int(self.current_floor) == self.current_floor:
      self.requested_floors.discard(self.current_floor)

  def minutes_to_floor(self, destination_floor: int) -> float:
    return abs(self.current_floor - destination_floor) / self.floors_per_minute

  def move_minutes(self, minutes: float) -> float:
    if not self.floors_queue:
      return self.current_floor

    dest_floor = self.floors_queue[0]
    max_number_floors_to_move = self.floors_per_minute * minutes
    if dest_floor > self.current_floor:
      self.current_floor = min(self.current_floor + max_number_floors_to_move,
                               dest_floor)
    else:
      self.current_floor = max(self.current_floor - max_number_floors_to_move,
                               dest_floor)

    if self.current_floor == dest_floor:
      self.floors_queue.popleft()

    return self.current_floor
