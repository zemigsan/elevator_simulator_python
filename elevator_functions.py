"""
A set of examples algorithms to operate the elevator. You can create your own and test the efficiency.
Format of the fucntion receives current_minute and the Elevator System, and needs to adjust each elevator floor_queue as orders.
"""


"""
elevator_sim_naive: this is the most naive solution for the elevator problem, it uses only one elevator and does just a FIFO, just adds the union of the floors.
"""
def elevator_sim_naive_single_elevator(current_minute, elevator_system):
  elevators = elevator_system.elevators
  main_elevator = elevators[0]
  main_elevator.floors_queue = list(main_elevator.floors_pressed.union(elevator_system.floors_requested)) 
  #the rest of elevators just keep going in the direction of the floors that are pressed
  for i in range(1, len(elevators)):
    elevators[i].floors_queue = list(elevators[i].floors_pressed)



"""
elevator_sim_optimal: this solution checks for any new floors that are not in elevator queue, and adds it to the elevator that is closest
"""
def elevator_sim_naive_multiple_elevators(current_minute, elevator_system):
  elevators = elevator_system.elevators
  #key to know if a elevator was already asked
  floor_elevator = {}
  default_elevator = 0
  
  #adds first all requested elevators in the queue
  for i in range(0, len(elevators)):
    elevators[i].floors_queue = []
    for floor in elevators[i].floors_pressed:
      elevators[i].floors_queue.append(floor)
      floor_elevator[floor] = i

  # adds new floors that were pressed/request
  floors_to_add = elevator_system.floors_requested
  for floor in floors_to_add:
    #checks if is not in queue of existing elevator
    if floor not in floor_elevator.keys():
      default_elevator = 0
      min_distance = abs(elevators[0].current_floor-floor)
      #checks which elevator is closest
      for i in range(1, len(elevators)):
        dist = abs(elevators[i].current_floor-floor)
        if dist < min_distance:
          min_distance = dist
          default_elevator = i
      elevators[default_elevator].floors_queue.append(floor)
  

  
