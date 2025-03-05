
import numpy as np
import random


class Car:
    def __init__(self, lane, position, speed, direction=1, max_speed=5):
        """
        Initialize a car with specific properties

        :param lane: Lane number the car is in
        :param position: Initial position on the highway
        :param speed: Speed of the car (units per time step)
        :param direction: 1 for forward, -1 for backward
        :param max_speed: Maximum speed the car can travel
        """
        self.lane = lane
        self.position = position
        self.speed = speed
        self.direction = direction
        self.max_speed = max_speed
        self.color = f"rgb({random.randint(50,200)}, {random.randint(50,200)}, {random.randint(50,200)})"


class HighwayTrafficSimulation:
    def __init__(self, highway_length=100, road_width=6, side_width=2):
        """
        Initialize the highway traffic simulation

        :param highway_length: Total length of the highway
        :param road_width: Number of lanes
        :param side_width: Width of the road sides
        """
        self.highway_length = highway_length
        self.road_width = road_width
        self.side_width = side_width
        self.cars = []

    def generate_cars(self, num_cars):
        """
        Generate a specified number of cars with random properties

        :param num_cars: Number of cars to generate
        """
        self.cars = []
        for _ in range(num_cars):
            lane = random.randint(1, self.road_width)
            position = random.randint(0, self.highway_length)
            speed = random.randint(1, 5)
            direction = random.choice([1, 1])
            self.cars.append(Car(lane, position, speed, direction))

    def update_car_positions(self, time_step):
        """
        Update positions of all cars based on their speed and traffic conditions

        :param time_step: Number of time steps elapsed
        :return: Updated car positions
        """
        # Sort cars by lane and position to check for cars ahead
        lane_cars = {}
        for car in self.cars:
            if car.lane not in lane_cars:
                lane_cars[car.lane] = []
            lane_cars[car.lane].append(car)

        # Sort cars in each lane by position
        for lane in lane_cars:
            lane_cars[lane].sort(key=lambda x: x.position)

        updated_cars = []
        for car in self.cars:
            # Find cars in the same lane
            cars_in_lane = lane_cars.get(car.lane, [])

            # Find the car directly in front (if any)
            car_ahead = None
            for other_car in cars_in_lane:
                # Skip the current car itself
                if other_car == car:
                    continue

                # Check if the other car is ahead of the current car
                # Account for wraparound in highway length
                if car.direction == 1:
                    if (
                        other_car.position > car.position
                        and other_car.position - car.position < self.highway_length / 2
                    ):
                        car_ahead = other_car
                        break
                else:
                    if (
                        other_car.position < car.position
                        and car.position - other_car.position < self.highway_length / 2
                    ):
                        car_ahead = other_car
                        break

            # Adjust speed based on car ahead
            if car_ahead:
                # If car ahead is moving slower, match its speed
                car.speed = min(car.speed, car_ahead.speed)
            else:
                # If no car ahead, gradually return to max speed
                car.speed = min(car.speed + 0.5, car.max_speed)

            # Update position
            new_position = (
                car.position + car.speed * car.direction * time_step
            ) % self.highway_length

            # Create updated car
            updated_car = Car(
                car.lane, new_position, car.speed, car.direction, car.max_speed
            )
            updated_car.color = car.color  # Preserve original color
            updated_cars.append(updated_car)

        return updated_cars
