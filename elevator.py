class Elevator:
    """A elevator class.
    The elevator class creates and manages the state of an individual elevator. It is time agnostic and just represents the current state of the elevator.
    Parameters
    ----------
    capacity : integer
        tells the number of people that the elevator can hold
    floors_per_minute : float
        gives the speed of elevator in number of floors per minute
    current_floor : float
        floor (or middle of floor) where the elevator is
    Attributes
    ----------
    current_capacity : integer
        tells the current capacity of the elevator (how many occupants there are)
    floors_pressed : (integer)
        set of floors requested inside the elevator
    floors_queue : [integer]
        list of floors that elevator should go in order (this is controlled by the elevator algorithm function)
    Methods
    ----------
    get_free_capacity : 
        returns the number of empty capacity that exists in elevator
    add_occupants : number_people (int), floor_destination (int)
        add new occupants to the elevator, adjusting the capacity
   remove_occupants : number_people (int)
        remove occupants from the elevator to the current floor, adjusting the capacity
    minutes_to_floor: destination_floor (int)
        returns the number of minutes that takes to reach floor X from current place
    move_minutes: minutes (float)
        moves the elevator in the direction of the next floor for X minutes; returns the new current floor
  """
    def __init__(self, capacity, floors_per_minute, current_floor=0):
        self.capacity = capacity
        self.floors_per_minute = floors_per_minute
        self.current_floor = current_floor
        self.floors_pressed = set()
        self.floors_queue = []
        self.current_capacity = 0

    def get_free_capacity(self):
        return self.capacity - self.current_capacity

    def add_occupants(self, number_people, floor_destination):
        #add the floor to pressed and updates capacity
        self.floors_pressed.add(floor_destination)
        self.current_capacity += number_people
        return True

    def remove_occupants(self, number_people):
        #updates capacity and removes the floor pressed
        self.current_capacity -= number_people
        self.floors_pressed.discard(self.current_floor)
        return True

    def minutes_to_floor(self, destination_floor):
        return abs(self.current_floor -
                   destination_floor) / self.floors_per_minute

    def move_minutes(self, minutes):
        # if no floors to go, stays in the same
        if len(self.floors_queue) == 0:
            return self.current_floor

        dest_floor = self.floors_queue[0]
        if (dest_floor != self.current_floor):
            maxNumberFloorsToMove = self.floors_per_minute / minutes
            if (dest_floor > self.current_floor):
                self.current_floor = min(
                    self.current_floor + maxNumberFloorsToMove, dest_floor)
            else:
                self.current_floor = max(
                    self.current_floor - maxNumberFloorsToMove, dest_floor)

        #if arrives to destination floor, removes from the qeues
        if (self.current_floor == dest_floor):
            self.floors_queue.pop(0)


        return self.current_floor
