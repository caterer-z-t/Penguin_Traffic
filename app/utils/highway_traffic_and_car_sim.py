# In[1]:
# highway_simulation.py
import random

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

        if driver_type == "normal":
            self.safe_distance = 1
            self.acceleration = 0.5
            self.deceleration = 1.0
        elif driver_type == "aggressive":
            self.safe_distance = 0.5
            self.acceleration = 1.0
            self.deceleration = 1.5
        elif driver_type == "cautious":
            self.safe_distance = 2
            self.acceleration = 0.3 
            self.deceleration = 0.8

    def adjust_speed(self, distance, car_in_front_speed=None):
        # If no distance is provided, maintain current speed
        if distance is None:
            return

        # If we're too close to the car in front
        if distance <= self.safe_distance:
            if car_in_front_speed is not None:
                self.speed = min(self.speed, car_in_front_speed)
            else:
                self.speed -= self.deceleration
        else:
            # Accelerate if we have space
            self.speed += self.acceleration

        # Ensure speed doesn't go below 0
        if self.speed < 0:
            self.speed = 0

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
        }

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

    def _calculate_statistics(self):
        """Calculates statistics for the simulation."""
        num_cars = len(self.cars)
        avg_speed = sum(car.speed for car in self.cars) / num_cars if num_cars > 0 else 0
        avg_density = num_cars / HIGHWAY_LENGTH
        lane_distribution = [0, 0, 0]
        for car in self.cars:
            if 1 <= car.lane <= 3:
                lane_distribution[car.lane - 1] += 1

        self.statistics["time_elapsed"].append(self.time_elapsed)
        self.statistics["num_cars"].append(num_cars)
        self.statistics["avg_speed"].append(avg_speed)
        self.statistics["avg_density"].append(avg_density)
        self.statistics["lane_distribution"].append(lane_distribution)

    def _remove_cars(self):
        """Removes cars that have reached the end of the highway."""
        return [car for car in self.cars if car.position < HIGHWAY_LENGTH]

    def _apres_simulation(self, spawn_rate, lane_value):
        # Remove cars that have reached the end of the highway
        self.cars = self._remove_cars()

        # Add new cars
        self._add_car(spawn_rate, lane_value)

        # Update statistics
        if self.cars:
            self._calculate_statistics()

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
                    else:
                        # the cars will not collide so we can move them
                        rear_car.position += rear_car.speed
                # ensure we continue to move the front car
                car = lanes[lane][-1]
                car.position += car.speed

            elif len(lanes[lane]) == 1:
                car = lanes[lane][0]
                car.position += car.speed

        return self._apres_simulation(spawn_rate, lane_value)

    def update_individualistic(self, spawn_rate, lane_value):
        # Organize cars by lane
        lanes = self._sort_cars_in_lane()



        
        return self._apres_simulation(spawn_rate, lane_value)

    def update_penguin(self, spawn_rate, lane_value):
        # Organize cars by lane
        lanes = self._sort_cars_in_lane()

        # implement code to allow cars to act like penguins with a collective group mindset -- ideally 
        # functioning so that they move in a group and avoid collisions and optimize statisticts

        return self._apres_simulation(spawn_rate, lane_value)
