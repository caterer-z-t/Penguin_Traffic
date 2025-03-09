import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
ROAD_LENGTH = 1000  # Length of the highway
ROAD_LANES = 3  # Number of lanes
MAX_SPEED = 5  # Maximum speed of cars
SAFE_DISTANCE = 10  # Safe following distance
SLOW_PROBABILITY = (
    0.1  # Probability of random slowdowns (to simulate brake lights, distractions)
)
AGGRESSION_FACTOR = 0.8  # How aggressively drivers accelerate (0-1)


class Car:
    def __init__(self, lane, position, speed, desired_speed=None, driver_type="normal"):
        self.lane = lane
        self.position = position
        self.speed = speed
        self.desired_speed = (
            desired_speed if desired_speed else random.randint(3, MAX_SPEED)
        )
        self.driver_type = driver_type  # 'cautious', 'normal', 'aggressive'

        # Assign driver behavior factors based on driver type
        if driver_type == "cautious":
            self.safe_distance_factor = 1.5  # Wants more safe distance
            self.acceleration = 0.5  # Accelerates slowly
            self.deceleration = 1.0  # Brakes harder
        elif driver_type == "aggressive":
            self.safe_distance_factor = 0.7  # Accepts shorter distances
            self.acceleration = 1.0  # Accelerates quickly
            self.deceleration = 0.8  # Doesn't brake as hard
        else:  # normal
            self.safe_distance_factor = 1.0
            self.acceleration = 0.8
            self.deceleration = 0.9

    def adjust_speed(self, distance_to_next_car):
        """Implements an improved car-following model"""
        # Random slowdown (simulates brake lights, distractions)
        if random.random() < SLOW_PROBABILITY and self.speed > 1:
            self.speed -= 1
            return

        if distance_to_next_car is None:  # No car ahead
            # Gradually accelerate to desired speed
            if self.speed < self.desired_speed:
                self.speed += self.acceleration
            elif self.speed > self.desired_speed:
                self.speed -= self.deceleration
        else:
            # Calculate safe speed based on distance to car ahead
            required_safe_distance = SAFE_DISTANCE * self.safe_distance_factor

            if distance_to_next_car < required_safe_distance / 2:
                # Emergency braking
                self.speed = max(0, self.speed - 2 * self.deceleration)
            elif distance_to_next_car < required_safe_distance:
                # Gradual braking
                self.speed = max(0, self.speed - self.deceleration)
            elif self.speed < self.desired_speed:
                # Accelerate if not at desired speed and safe to do so
                self.speed = min(self.desired_speed, self.speed + self.acceleration)

        # Ensure speed is within valid range
        self.speed = max(0, min(MAX_SPEED, self.speed))

    def change_lane(self, current_lane_cars, other_lanes_cars):
        """Determines if a lane change is beneficial and safe"""
        # Only consider changing lanes if not at desired speed
        if self.speed >= self.desired_speed:
            return self.lane

        # Check if there's a car ahead slowing us down
        car_ahead = None
        min_distance = float("inf")

        for car in current_lane_cars:
            if car.position > self.position:
                distance = car.position - self.position
                if distance < min_distance:
                    min_distance = distance
                    car_ahead = car

        # If no car ahead or car ahead isn't slowing us down, stay in lane
        if not car_ahead or min_distance > SAFE_DISTANCE * self.safe_distance_factor:
            return self.lane

        # Consider changing lanes
        best_lane = self.lane
        best_score = -float("inf")

        for potential_lane, lane_cars in other_lanes_cars.items():
            # Skip current lane
            if potential_lane == self.lane:
                continue

            # Check if lane change is safe by looking for cars nearby in target lane
            safe = True
            next_car_distance = float("inf")
            prev_car_distance = float("inf")

            for car in lane_cars:
                if car.position > self.position:
                    distance = car.position - self.position
                    next_car_distance = min(next_car_distance, distance)
                    # Not safe if too close to a car ahead in new lane
                    if distance < SAFE_DISTANCE * self.safe_distance_factor:
                        safe = False
                        break
                else:
                    distance = self.position - car.position
                    prev_car_distance = min(prev_car_distance, distance)
                    # Not safe if too close to a car behind in new lane
                    if distance < SAFE_DISTANCE * 0.7:  # Less space needed behind
                        safe = False
                        break

            if safe:
                # Score the lane change based on distances to other cars
                score = next_car_distance - prev_car_distance * 0.5

                if score > best_score:
                    best_score = score
                    best_lane = potential_lane

        return best_lane


class HighwayTrafficSimulation:
    def __init__(self):
        self.cars = []
        self.time_elapsed = 0
        self.statistics = {
            "average_speed": [],
            "cars_on_road": [],
            "lane_distribution": [],
        }

    def add_car(self, spawn_rate):
        """Adds a car with probability based on spawn_rate."""
        if random.random() < spawn_rate:
            lane = random.randint(1, ROAD_LANES)
            position = 0  # Start at the beginning of the road
            speed = random.randint(1, 3)  # Start at slower speed

            # Random driver type
            driver_types = ["cautious", "normal", "normal", "normal", "aggressive"]
            driver_type = random.choice(driver_types)

            # Higher desired speed for aggressive drivers
            desired_speed = random.randint(3, MAX_SPEED)
            if driver_type == "aggressive":
                desired_speed = min(MAX_SPEED, desired_speed + 1)
            elif driver_type == "cautious":
                desired_speed = max(2, desired_speed - 1)

            # Ensure there's enough space for the new car
            can_add = True
            for car in self.cars:
                if car.lane == lane and car.position < 2 * SAFE_DISTANCE:
                    can_add = False
                    break

            if can_add:
                self.cars.append(Car(lane, position, speed, desired_speed, driver_type))

    def update(self, spawn_rate, traffic_jam_factor=0):
        """Updates the entire simulation for one time step."""
        # Organize cars by lane
        lanes = {i: [] for i in range(1, ROAD_LANES + 1)}
        for car in self.cars:
            lanes[car.lane].append(car)

        # Sort cars in each lane by position
        for lane in lanes:
            lanes[lane].sort(key=lambda car: car.position)

        # Track cars that have changed lanes
        changed_lane = set()

        # Update car speeds and handle lane changes
        for lane_num, lane_cars in lanes.items():
            for i, car in enumerate(lane_cars):
                # If car already moved lanes in this update, skip
                if car in changed_lane:
                    continue

                # Find distance to next car in current lane
                distance_to_next = None
                for ahead_car in lane_cars[i + 1 :]:
                    distance = ahead_car.position - car.position
                    if distance > 0:
                        distance_to_next = distance
                        break

                # Adjust speed based on traffic conditions
                car.adjust_speed(distance_to_next)

                # Consider changing lanes
                other_lanes = {l: lanes[l] for l in lanes if l != lane_num}
                new_lane = car.change_lane(lane_cars, other_lanes)

                if new_lane != car.lane:
                    car.lane = new_lane
                    changed_lane.add(car)

        # Create traffic jam by slowing down cars in a section
        if traffic_jam_factor > 0:
            jam_position = ROAD_LENGTH // 2
            jam_radius = 100

            for car in self.cars:
                # If car is in the traffic jam zone
                if abs(car.position - jam_position) < jam_radius:
                    # Reduce speed based on how close to center of jam
                    distance_factor = 1 - abs(car.position - jam_position) / jam_radius
                    slow_factor = traffic_jam_factor * distance_factor
                    car.speed = max(0, car.speed - slow_factor * 2)

        # Move cars forward
        for car in self.cars:
            car.position += car.speed

        # Remove cars that have reached the end of the road
        self.cars = [car for car in self.cars if car.position < ROAD_LENGTH]

        # Add new cars
        self.add_car(spawn_rate)

        # Collect statistics
        if self.cars:
            avg_speed = sum(car.speed for car in self.cars) / len(self.cars)
            self.statistics["average_speed"].append(avg_speed)
            self.statistics["cars_on_road"].append(len(self.cars))

            lane_counts = [0] * ROAD_LANES
            for car in self.cars:
                lane_counts[car.lane - 1] += 1
            self.statistics["lane_distribution"].append(lane_counts)

        self.time_elapsed += 1

        return self.cars

    def get_statistics(self):
        """Returns the current statistics of the simulation."""
        return self.statistics


def visualize_simulation(
    simulation, num_frames=200, spawn_rate=0.3, traffic_jam_factor=0
):
    """Creates an animation of the traffic simulation."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=3)

    # Set up the highway plot
    ax1.set_xlim(0, ROAD_LENGTH)
    ax1.set_ylim(0, ROAD_LANES + 1)
    ax1.set_title("Highway Traffic Simulation")
    ax1.set_xlabel("Position")
    ax1.set_ylabel("Lane")

    # Draw lane markings
    for i in range(1, ROAD_LANES):
        ax1.axhline(y=i + 0.5, color="white", linestyle="--")

    # Set up the statistics plot
    ax2.set_xlim(0, num_frames)
    ax2.set_ylim(0, MAX_SPEED + 1)
    ax2.set_title("Traffic Statistics")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Average Speed")

    # Initialize the scatter plot for cars
    scatter = ax1.scatter([], [], c=[], s=50, cmap="coolwarm")

    # Initialize the line plot for average speed
    (line,) = ax2.plot([], [], "b-", label="Average Speed")
    cars_text = ax2.text(0.02, 0.95, "", transform=ax2.transAxes)

    def init():
        scatter.set_offsets(np.empty((0, 2)))
        scatter.set_array(np.array([]))
        line.set_data([], [])
        cars_text.set_text("")
        return scatter, line, cars_text

    def update(frame):
        # Update the simulation
        cars = simulation.update(spawn_rate, traffic_jam_factor)

        # Update the car positions
        if cars:
            positions = np.array([[car.position, car.lane] for car in cars])
            speeds = np.array([car.speed for car in cars])
            scatter.set_offsets(positions)
            scatter.set_array(speeds)
        else:
            scatter.set_offsets(np.empty((0, 2)))
            scatter.set_array(np.array([]))

        # Update the statistics
        stats = simulation.get_statistics()
        if stats["average_speed"]:
            times = list(range(len(stats["average_speed"])))
            line.set_data(times, stats["average_speed"])

            # Update the cars count text
            current_cars = stats["cars_on_road"][-1] if stats["cars_on_road"] else 0
            cars_text.set_text(f"Cars on road: {current_cars}")

        return scatter, line, cars_text

    anim = FuncAnimation(
        fig, update, frames=num_frames, init_func=init, blit=True, interval=50
    )
    plt.colorbar(scatter, ax=ax1, label="Speed")

    plt.show()

    return anim


# Example usage
if __name__ == "__main__":
    simulation = HighwayTrafficSimulation()
    visualize_simulation(
        simulation, num_frames=300, spawn_rate=0.3, traffic_jam_factor=1.5
    )
