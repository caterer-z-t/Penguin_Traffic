# In[1]:
# highway_simulation.py
import random
import numpy as np

# Highway parameters
HIGHWAY_LENGTH = 100
# ROAD_WIDTH = 6
SIDE_WIDTH = 2
# ROAD_LANES = ROAD_WIDTH  # Using the same number for lanes as road width

# In[2]:
class Car:
    def __init__(self, lane, position, speed, type="car", driver_type="normal"):
        self.lane = lane
        self.position = position
        self.speed = speed
        self.type = type
        self.id = random.randint(0, 10000000000000)
        self.color = f"rgb({random.randint(50,200)}, {random.randint(50,200)}, {random.randint(50,200)})"
        self.driver_type = driver_type  # normal, aggressive, cautious

        # penguin information
        self.time_in_huddle = 0
        self.is_in_huddle = False

        if driver_type == "normal":
            self.safe_distance = 2
            self.acceleration = 0.5
            self.deceleration = 1.0
        elif driver_type == "aggressive":
            self.safe_distance = 1
            self.acceleration = 1.0
            self.deceleration = 1.5
        elif driver_type == "cautious":
            self.safe_distance = 3
            self.acceleration = 0.3 
            self.deceleration = 0.8

        self.ideal_speed = speed
        self.time = 0
        self.happiness = 10

# In[3]:
class HighwayTrafficSimulation:
    def __init__(self):
        self.cars = []
        self.time_elapsed = 0
        self.statistics = {
            "time_elapsed": [],
            "num_cars": [],
            "avg_speed": [],
            "avg_density": [],
            "cars_on_highway": [],
            "lane_distribution": [],
            "avg_num_cars_per_lane": [],
            "happiness_factor": [],
            "avg_time_to_exit": [],
        }

        self.cars_reached_destination = []

    def _add_car(self, spawn_probability, lane_value):
        """Randomly adds a car based on the spawn probability."""
        for lane in range(1, lane_value + 1):
            if random.random() < (
                spawn_probability / 100 
            ):  # Convert slider value to probability
                driver_type = random.choice(["normal", "aggressive", "cautious"])

                # Set speed based on driver type
                if driver_type == "aggressive":
                    desired_speed = random.randint(5, 10)
                elif driver_type == "normal":
                    desired_speed = random.randint(3, 8)
                elif driver_type == "cautious":
                    desired_speed = random.randint(2, 6)

                self.cars.append(Car(lane, 0, desired_speed, driver_type=driver_type))

    def _sort_cars_in_lane(self, lane_value):
        """Sorts cars in each lane by position."""

        lanes = {i: [] for i in range(1, lane_value + 1)}
        for car in self.cars:
            lanes[car.lane].append(car)

        for lane in lanes:
            lanes[lane] = sorted(lanes[lane], key=lambda x: x.position)

        return lanes

    def _calculate_statistics(self, lane_value_slider, type="none"):
        """Calculates enhanced statistics for the simulation."""
        num_cars = len(self.cars)
        avg_speed = sum(car.speed for car in self.cars) / num_cars if num_cars > 0 else 0
        avg_density = num_cars / HIGHWAY_LENGTH
        lane_distribution = [0] * lane_value_slider

        speeds = []
        times_to_exit = []
        num_exited_cars = 0
        slow_car_threshold = 10  # Define a threshold for slow-moving cars
        num_slow_cars = 0

        for car in self.cars:
            if 1 <= car.lane <= lane_value_slider:
                lane_distribution[car.lane - 1] += 1
            speeds.append(car.speed)

            # Track slow-moving cars
            if car.speed < slow_car_threshold:
                num_slow_cars += 1

            # Track cars reaching destination
            if car.position >= HIGHWAY_LENGTH:
                num_exited_cars += 1
                times_to_exit.append(
                    self.time_elapsed - car.start_time
                )  # Assuming car.start_time exists

        # cars_reached_destination = []

        lanes = self._sort_cars_in_lane(lane_value=lane_value_slider)

        for lane in lanes:
            for car in lanes[lane]:
                car.time += 1

                if car.position >= 90:
                    # car reached destination
                    self.cars_reached_destination.append(car.time)

        # print(f"Cars reached destination: {self.cars_reached_destination}")

        self.statistics["time_elapsed"].append(self.time_elapsed)
        self.statistics["num_cars"].append(num_cars)
        self.statistics["avg_speed"].append(avg_speed)
        self.statistics["avg_density"].append(avg_density)
        self.statistics["lane_distribution"].append(lane_distribution)
        self.statistics["avg_num_cars_per_lane"].append(
            np.mean(lane_distribution)
        )
        self.statistics['happiness_factor'].append(
            sum(car.happiness for car in self.cars) / num_cars if num_cars > 0 else 0
        )
        self.statistics["avg_time_to_exit"].append(
            sum(self.cars_reached_destination) / len(self.cars_reached_destination) if self.cars_reached_destination else 0
        )

        # save the statistics to a csv file
        with open(f"../../results/statistics_{type}.csv", "w") as f:
            f.write("time_elapsed,num_cars,avg_speed,avg_density,lane_distribution,avg_num_cars_per_lane,happiness_factor,avg_time_to_exit\n")
            for i in range(len(self.statistics["time_elapsed"])):
                f.write(
                    f"{self.statistics['time_elapsed'][i]},"
                    f"{self.statistics['num_cars'][i]},"
                    f"{self.statistics['avg_speed'][i]},"
                    f"{self.statistics['avg_density'][i]},"
                    f"{self.statistics['lane_distribution'][i]},"
                    f"{self.statistics['avg_num_cars_per_lane'][i]},"
                    f"{self.statistics['happiness_factor'][i]},"
                    f"{self.statistics['avg_time_to_exit'][i]}\n"
                )

    def _remove_cars(self):
        """Removes cars that have reached the end of the highway."""
        return [car for car in self.cars if car.position < HIGHWAY_LENGTH]

    def _apres_simulation(self, spawn_rate, lane_value, type="none"):
        # Remove cars that have reached the end of the highway
        self.cars = self._remove_cars()

        # Add new cars
        self._add_car(spawn_rate, lane_value)

        # Update statistics
        if self.cars:
            self._calculate_statistics(lane_value_slider=lane_value, type=type)

        self.time_elapsed += 1
        return self.cars

    def update_simple(self, spawn_rate, lane_value):
        """Updates the entire simulation for one time step."""
        # Organize cars by lane
        lanes = self._sort_cars_in_lane(lane_value=lane_value)

        for lane in lanes:
            if len(lanes[lane]) > 1:
                for i in range(len(lanes[lane]) - 1):  # Loop through all consecutive cars
                    front_car = lanes[lane][i + 1]
                    rear_car = lanes[lane][i]

                    front_car_position = front_car.position
                    front_car_speed = front_car.speed
                    front_car_position_next_step = front_car_position + front_car_speed

                    rear_car_position = rear_car.position
                    rear_car_speed = rear_car.speed
                    rear_car_position_next_step = rear_car_position + rear_car_speed

                    # Check if the rear car will collide with the front car
                    if rear_car_position_next_step >= (front_car_position_next_step - rear_car.safe_distance):   

                        # Adjust the rear car's speed to avoid collision
                        rear_car.speed = min(front_car_speed, rear_car_speed)
                        rear_car.position = front_car_position - rear_car.safe_distance

                        rear_car.happiness -= 3
                    else:
                        # the cars will not collide so we can move them
                        rear_car.position += rear_car.speed
                # ensure we continue to move the front car
                car = lanes[lane][-1]
                car.position += car.speed

            elif len(lanes[lane]) == 1:
                car = lanes[lane][0]
                car.position += car.speed

        return self._apres_simulation(spawn_rate, lane_value, type="simple")

    def update_individualistic(self, spawn_rate, lane_value):
        # Organize cars by lane
        lanes = self._sort_cars_in_lane(lane_value=lane_value)

        for lane in lanes:
            if len(lanes[lane]) > 1:
                for i in range(
                    len(lanes[lane]) - 1
                ):  # Loop through all consecutive cars
                    front_car = lanes[lane][i + 1]
                    rear_car = lanes[lane][i]

                    front_car_position = front_car.position
                    front_car_speed = front_car.speed
                    front_car_position_next_step = front_car_position + front_car_speed

                    rear_car_position = rear_car.position
                    rear_car_speed = rear_car.speed
                    rear_car_position_next_step = rear_car_position + rear_car_speed

                    # Check if the rear car will collide with the front car
                    if rear_car_position_next_step >= (
                        front_car_position_next_step - rear_car.safe_distance
                    ):

                        # get the neighboring lanes
                        neighboring_lanes = [lane - 1, lane + 1]
                        neighboring_lanes = [x for x in neighboring_lanes if 1 <= x <= lane_value]

                        best_lane = None

                        num_cars_in_lanes = {}

                        rear_car_safe_distance = [rear_car.safe_distance - rear_car.position, rear_car.safe_distance + rear_car.position]

                        # check if the neighboring lanes would allow the rear car to move
                        for neighboring_lane in neighboring_lanes:

                            # no cars in the neighboring lane
                            if len(lanes[neighboring_lane]) == 0:
                                best_lane = neighboring_lane
                                break

                            # there are some cars in the neighboring lane
                            else:

                                # check to see if there are any cars in the neighboring lane that would collide with the rear car
                                for car in lanes[neighboring_lane]:

                                    # if the car in the neighboring lane would collide with the rear car
                                    if car.position + car.speed >= rear_car_position_next_step - rear_car_safe_distance[0] and car.position - car.speed <= rear_car_position_next_step + rear_car_safe_distance[1]:
                                        break

                                # if the car in the neighboring lane would not collide with the rear car
                                # obtain the number of cars in the neighboring lane ahead of the rear car
                                # get the number of cars in the neighboring lane ahead of the rear car
                                num_cars_in_lanes[neighboring_lane] = len([x for x in lanes[neighboring_lane] if x.position > rear_car.position])

                        # find the lane with the least number of cars ahead of the rear car
                        if num_cars_in_lanes:
                            best_lane = min(num_cars_in_lanes, key=num_cars_in_lanes.get)

                        rear_car.lane = best_lane
                        rear_car.position = rear_car_position + rear_car.speed

                        rear_car.happiness -= 2

                    else:
                        # the cars will not collide so we can move them
                        rear_car.position += rear_car.speed
                # ensure we continue to move the front car
                car = lanes[lane][-1]
                car.position += car.speed

            elif len(lanes[lane]) == 1:
                car = lanes[lane][0]
                car.position += car.speed

        return self._apres_simulation(spawn_rate, lane_value, type="individualistic")

    def update_penguin(self, spawn_rate, lane_value):

        huddle_distance = 1
        lanes = self._sort_cars_in_lane(lane_value=lane_value)

        for lane in lanes:
            if len(lanes[lane]) > 1:
                for i in range(
                    len(lanes[lane]) - 1
                ):  # Loop through all consecutive cars
                    front_car = lanes[lane][i + 1]
                    rear_car = lanes[lane][i]

                    front_car_position = front_car.position
                    front_car_speed = front_car.speed
                    front_car_position_next_step = front_car_position + front_car_speed

                    rear_car_position = rear_car.position
                    rear_car_speed = rear_car.speed
                    rear_car_position_next_step = rear_car_position + rear_car_speed

                    # rear car is in a huddle, increemnt the time in huddle
                    if rear_car.is_in_huddle:
                        rear_car.time_in_huddle += 1

                    # rear car has been in the huddle for 3 steps, it will now adapt the huddle mindset
                    if rear_car.time_in_huddle >= 3:
                        rear_car.speed = min(front_car_speed, rear_car_speed)
                        rear_car.position = front_car_position_next_step - huddle_distance

                        rear_car.happiness += 1

                    else:
                        # Check if the rear car will collide with the front car
                        if rear_car_position_next_step >= (
                            front_car_position_next_step - rear_car.safe_distance
                        ):

                            # Adjust the rear car's speed to avoid collision
                            rear_car.speed = min(front_car_speed, rear_car_speed)
                            rear_car.position = front_car_position - rear_car.safe_distance
                            rear_car.is_in_huddle = True

                            rear_car.happiness -= 1
                        else:
                            # the cars will not collide so we can move them
                            rear_car.position += rear_car.speed
                # ensure we continue to move the front car
                car = lanes[lane][-1]
                car.position += car.speed
            elif len(lanes[lane]) == 1:
                # Single car in lane
                car = lanes[lane][0]
                car.position += car.speed

        return self._apres_simulation(spawn_rate, lane_value, type="penguin")
