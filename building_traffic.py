from numpy import random


class BuildingTraffic:
    """A building traffic class.
    The Building class is able to generate traffic for a particular building characteristics. It receives a pattern of traffic and randomizes the traffic throughout a 24 hour period according tot that pattern.
    Parameters
    ----------
    percentage_traffic_hour : dictionary {hour: percentage_traffic}
        configures the distribuition of traffic per hour of the day of the building
    total_elevator_traffic : integer
        configures the average number of people that use the building per day
    average_group_size : float
        configures the average group size of people that use the elevator
    number_floors : integer
        configures the number of floors of the building
    Attributes
    ----------
    people_log : dictionary {minute: [[number_people,floor_in,floor_destination],]}
        records the list of people that request the usage of elevator at each minute of the day
    Methods
    ----------
    generate : 
        returns a randomized generated traffic log based on the Building conditions
    calculate_total_traffic : 
        returns the total number of people that are using the elevator in the current log
  """
    def __init__(self, percentage_traffic_per_hour, total_elevator_traffic,
                 average_group_size, number_floors):
        self.percentage_traffic_per_hour = percentage_traffic_per_hour
        self.total_elevator_traffic = total_elevator_traffic
        self.average_group_size = average_group_size
        self.people_log = {}
        self.number_floors = number_floors

    def generate(self):

        #go calculate each minute and add to dictionary
        for i in range(1440):
            hour = i // 60
            #calculates the average # people to
            average_number_people = round(
                random.normal((self.percentage_traffic_per_hour[hour] *
                               self.total_elevator_traffic) / 60))
            average_number_groups = round(
                (average_number_people / self.average_group_size))

            #initialize variables (n=number of groups; minute will save the list of groups)
            n = 0
            minute = []
            while n < average_number_groups:
                group_size = round(random.normal(self.average_group_size))
                if group_size <= 0: group_size = 1
                floor_in = random.randint(0, self.number_floors)
                floor_out = random.randint(0, self.number_floors)
                while floor_out == floor_in:
                    floor_out = random.randint(0, self.number_floors)
                minute.append([group_size, floor_in, floor_out])
                n += 1

            self.people_log[i] = minute
        return self.people_log

    def calculate_total_traffic(self):
        traffic = 0
        for key in self.people_log:
            for val in self.people_log[key]:
                traffic += val[0]
        return traffic
