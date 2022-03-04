
class ElevatorSimulator:
    """A elevator simulator class.
  The elevator simulator class runs a simulation taking into consideration a particular Building Traffic pattern, an Elevator System and a elevator algorithm function, and generates the results.
  Parameters
  ----------
  traffic : dictionary {hour: percentage_traffic}
        distribuition of traffic per hour of the day of the building
  elevators : ElevatorSystem
        list of elevators available
  elevator_func : function(current_minute, elevator_system)
        function that controls the elevator system - it changes the priority floors for each elevator to go (changes each elevator floor queue)
  Attributes
  ----------
  people_queue : [[number_people,floor_in,floor_destination,minute_arrived],]
        list of people waiting for elevator
  people_queue_elevators : [[number of people, floor_in, floor_out, minute_arrived, time_elevator_arrived;elevator_id],]
        list of people that are inside an elevator 
  simulation_data : dictionary([])
        dictionary that records the final results of the simulation
  Attributes
  ----------
  elevator_system : 
      list of all elevators in the building
   people_queue: list of people waiting for elevator
  Methods
   ----------
  add_people_stats : people ([number_people,floor_in,floor_out]), time_destination (float), elevator_id (int)
      records the stats of a group of people that reached destination
  get_people_at_floor : floor (int)
      returns everyone that is waiting to board the elevator at a particular floor
  add_people_into_elevator :  people ([number_people,floor_in,floor_out]), elevator_id (int)
      tries to add people into a particular elevator
      returns true if people entering elevator is sucessful
  remove_people_elevator :  elevator_id (int), current_minute (float)
      removes any people that are in this elevator (elevator_id) that wants to leave in this floor
      returns total number of people removed
  run_simulation
      runs the simulation, calling the elevator_func every minute of simulation to determine the decisions
      returns the simulation_data (simulation results)
  ----------
  """
    def __init__(self, traffic, elevator_system, elevator_func):
        self.traffic = traffic
        self.elevator_system = elevator_system
        self.elevator_func = elevator_func
        self.people_queue = []
        #queue of queues
        self.people_queue_elevators = []
        for el in self.elevator_system.elevators:
            self.people_queue_elevators.append([])
        #data result format (to be read by pandas)
        self.simulation_data = {
            'number_people': [],
            'minute_arrived': [],
            'floor_in': [],
            'time_destination': [],
            'floor_destination': [],
            'time_elevator_arrived': [],
            'elevator_id': [],
            'total_time': [],
            'wait_time': []
        }

    def add_people_stats(self, people, time_destination, elevator_id):
        #append to list
        wait_time = people[4] - people[3]
        total_time = time_destination - people[3]
        self.simulation_data['number_people'].append(people[0])
        self.simulation_data['minute_arrived'].append(people[3])
        self.simulation_data['floor_in'].append(people[1])
        self.simulation_data['time_destination'].append(time_destination)
        self.simulation_data['floor_destination'].append(people[2])
        self.simulation_data['time_elevator_arrived'].append(people[4])
        self.simulation_data['elevator_id'].append(elevator_id)
        self.simulation_data['total_time'].append(total_time)
        self.simulation_data['wait_time'].append(wait_time)
        return True

    def get_people_at_floor(self, floor):
        people_at_floor = []
        for p in self.people_queue:
            if p[1] == floor:
                people_at_floor.append(p)
        return people_at_floor

    def add_people_into_elevator(self, people, elevator_id):
        #returns true if people entering elevator is sucessful
        number_of_people = people[0]
        floor_destination = people[2]
        el = self.elevator_system.elevators[elevator_id]
        #if elevator has free capacity removes from queue and adds
        if el.get_free_capacity() >= number_of_people:
            el.add_occupants(number_of_people, floor_destination)
            self.people_queue_elevators[elevator_id].append(people)
            self.people_queue.remove(people)
            return True
        else:
            return False

    def remove_people_elevator(self, elevator_id, current_minute):
        elevator = self.elevator_system.elevators[elevator_id]
        el_people = self.people_queue_elevators[elevator_id]
        number_people_removed = 0
        #removes any people that want to leave in this floor
        for p in el_people:
            if p[2] == elevator.current_floor:
                elevator.remove_occupants(p[0])
                number_people_removed += p[0]
                self.add_people_stats(p, current_minute, elevator_id)
                el_people.remove(p)
        return number_people_removed

    def run_simulation(self):

        for minute in range(1440):
            #retrieves the people that arrived at this minute from traffic log
            people = self.traffic[minute]

            #add the new pressed elevators to the system
            for person in people:
                #stores minute that person arrived for adding later to simulation data (creates copy of the list to be unique to this simulation)
                p_copy = person.copy()
                p_copy.append(minute)
                #adds the request for a floor
                self.elevator_system.floors_requested.add(p_copy[1])
                self.people_queue.append(p_copy)

            #execute algorithm function with current minute, elevators,
            self.elevator_func(minute, self.elevator_system)
            #TODO: check that there were no changes in elevator system except the elevator queue (avoid "cheating")

            #goes elevator by elevator and executes the moves requested by the algorithm for this minute
            for elevator_id, el in enumerate(self.elevator_system.elevators):
                #controls elevator minute
                current_elevator_minute = minute
                
                #time counter (1 minute)
                allotted_minutes = 1
              
                # while there is still time and places to go for this elevator
                while (len(el.floors_queue) > 0 and allotted_minutes > 0):
                    requested_floor = el.floors_queue[0]
                    travel_time = el.minutes_to_floor(requested_floor)
                  
                    #checks if has enough time to reach next floor
                    if (travel_time < allotted_minutes):
                        current_elevator_minute += travel_time
                        # move elevator to destination and remove from elevator queue
                        el.move_minutes(travel_time)

                        # Passenger removal first (to free up capacity)
                        self.remove_people_elevator(elevator_id,
                                                    current_elevator_minute)
                        # then board any passenger if capacity allows
                        people_to_get_in = self.get_people_at_floor(
                            requested_floor)
                        for p in people_to_get_in:
                            #goes group by group and checks if they fit in elevator
                            if self.add_people_into_elevator(p, elevator_id):
                                #if fits removes from the people queuee
                                people_to_get_in.remove(p)
                                #adds elevator arrival minute for stats
                                p.append(current_elevator_minute)
                              
                        #check if all people waiting in that floor are in, if yes, remove it from the system
                        if len(people_to_get_in) == 0:
                            #realistically would be to remove and press again but as we are not keeping track order in this phase does not matter
                            if requested_floor in self.elevator_system.floors_requested:
                                self.elevator_system.floors_requested.remove(
                                    requested_floor)
                    else:
                        #if does not reach destination floor, just moves what it can and advances one minute
                        el.move_minutes(travel_time)
        return self.simulation_data
