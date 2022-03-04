# ElevatorSimulator
Python console-based elevator simulator.
- that allows to run a Monte Carlo simulation and outputting key metrics of elevator system around wait time.
- allows for testing different elevator algorithms (you can extend your own) and has a Building traffic generator.

## Elevator (elevator.py)
The elevator class creates and manages the state of an individual elevator. It is time agnostic and just represents the current state of the elevator.

## Elevator System (elevator_system.py)
The Elevator System keeps the state of the list of elevators and the current floors requested.

## Elevator Simulator (elevator_simulator.py)
The elevator simulator class runs a simulation taking into consideration a particular Building Traffic pattern, an Elevator System and a elevator algorithm function, and generates the results.

## Sample elevator functions (elevator_functions.py)
A set of examples algorithms to operate the elevator. You can create your own and test the efficiency.

## Building Traffic (building_traffic.py)
The Building class is able to generate traffic for a particular building characteristics. It receives a pattern of traffic and randomizes the traffic throughout a 24 hour period according tot that pattern.



