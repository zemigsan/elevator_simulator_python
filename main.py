import building_traffic as BuildingTraffic
import elevator_simulator as ElevatorSimulator
import elevator_system as ElevatorSystem
import elevator_functions as sample_funcs
import pandas as pd


#sample distribution of traffic per hour
percentage_traffic_per_hour = {0:0.01,1:0.01,2:0.01,3:0.01,4:0.01,5:0.01,
                              6:0.01, 7:0.03, 8:0.12,9:0.09,10:0.03,
                              11:0.02,12:0.07,13:0.10,14:0.05,15:0.02,
                              16:0.03,17:0.12,18:0.11,19:0.06,20:0.03,
                              21:0.02,22:0.01,23:0.01}
#sample elevator carateristics
total_elevator_traffic = 1000
average_group_size = 2
number_floors = 10

#elevator config list of elevator (capacity, floors/minute. current floor) 
elevators_config = [[10,7],[10,7]]

#creates the building to generate traffic
pg = BuildingTraffic.BuildingTraffic(percentage_traffic_per_hour, total_elevator_traffic, average_group_size, number_floors)

for i in range(1):
  t = pg.generate()
  traffic = pg.calculate_total_traffic()

  ev = ElevatorSystem.ElevatorSystem(elevators_config)
  simulator = ElevatorSimulator.ElevatorSimulator(t, ev, sample_funcs.elevator_sim_naive_multiple_elevators)
  
  ##run simulation
  res = simulator.run_simulation()
  results_df = pd.DataFrame.from_dict(res)
  print('\n\n=== RESULTS - elevator_sim_optimal ===')
  print(results_df.describe()[['total_time','wait_time']])

  ev2 = ElevatorSystem.ElevatorSystem(elevators_config)
  simulator2 = ElevatorSimulator.ElevatorSimulator(t, ev2, sample_funcs.elevator_sim_naive_single_elevator)

  ##run simulation
  res2 = simulator2.run_simulation()
  results_df2 = pd.DataFrame.from_dict(res2)
  print('\n\n=== RESULTS - elevator_sim_naive_single_elevator ===')
  print(results_df2.describe()[['total_time','wait_time']])
