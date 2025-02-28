import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mesa import Agent, Model
from mesa.space import MultiGrid

class Car(Agent):
    def __init__(self, unique_id, model, direction):
        super(Car, self).__init__(model=model)  # 🚀 Explicitly pass `model`
        self.unique_id = unique_id  # 🚀 Ensure ID is explicitly stored
        self.direction = direction  # "N", "S", "E", "W"
        self.speed = 1  # Cells per step

    def move(self):
        possible_moves = self.get_possible_moves()
        if possible_moves:
            self.model.grid.move_agent(self, possible_moves[0])  # Move forward if possible

    def get_possible_moves(self):
        x, y = self.pos
        moves = {
            "N": (x, y + self.speed),
            "S": (x, y - self.speed),
            "E": (x + self.speed, y),
            "W": (x - self.speed, y),
        }
        new_pos = moves[self.direction]
        if self.model.grid.out_of_bounds(new_pos):
            return []
        return [new_pos] if self.model.grid.is_cell_empty(new_pos) else []

    def step(self):
        self.move()

class TrafficModel(Model):
    def __init__(self, width=10, height=10, num_cars=10):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.car_agents = []  # 🚀 Store agents in `self.car_agents`

        for i in range(num_cars):
            direction = np.random.choice(["N", "S", "E", "W"])
            x, y = np.random.randint(0, width), np.random.randint(0, height)
            car = Car(unique_id=i, model=self, direction=direction)  # 🚀 Pass `model=self`
            self.grid.place_agent(car, (x, y))
            self.car_agents.append(car)  # 🚀 Use `self.car_agents`

    def step(self):
        for agent in self.car_agents:
            agent.step()

# Run the simulation and visualize
def run_simulation(steps=20):
    model = TrafficModel(width=10, height=10, num_cars=10)
    fig, ax = plt.subplots()
    
    def update(frame):
        model.step()
        ax.clear()
        grid_data = np.zeros((10, 10))
        for agent in model.car_agents:
            x, y = agent.pos
            grid_data[y, x] = 1
        ax.imshow(grid_data, cmap="Greys")
        ax.set_title(f"Step {frame}")
    
    ani = animation.FuncAnimation(fig, update, frames=steps, repeat=False)
    plt.show()

# Run the fully fixed simulation
run_simulation()
