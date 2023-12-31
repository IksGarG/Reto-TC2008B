from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from .agent import *
import json

from GridGen.grid_gen import gDown, gUp, gLeft, gRight, get_finder, create_world

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, module):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("static/city_files/mapDictionary.json"))

        self.traffic_lights = []
        self.next_agents = 0
        self.finder = get_finder()
        self.world = create_world()
        self.kill_list = []
        self.module = module
        self.steps_with_cars_in_positions = 0
        self.cars_in_destinations = 0

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('static/city_files/2023_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
        self.running = True
        
    def add_car(self):
        agent_positions = [(0, 0), (23, 0), (0, 24), (23, 24)]
        #agent_positions = [(0, 0)]
        all_positions_have_cars = True

        for i, pos in enumerate(agent_positions):
            # Check the contents of the position
            position_contents = self.grid.get_cell_list_contents(pos)

            # Check if there is only a road agent at the position
            if any(isinstance(agent, Road) for agent in position_contents) and not any(isinstance(agent, Car) for agent in position_contents):
                car = Car(i + 1000 + self.next_agents, self, pos)
                self.schedule.add(car)
                self.grid.place_agent(car, pos)
                self.next_agents += 2
                all_positions_have_cars = False
            self.next_agents += 2

        if all_positions_have_cars:
            self.steps_with_cars_in_positions += 1
            if self.steps_with_cars_in_positions >= 20:
                # Detener el modelo
                self.running = False
                print("Cars are stuck! Stopping the model.")
        else:
            self.steps_with_cars_in_positions = 0  # Resetear el contador si no todos tienen autos


    def step(self):
        '''Advance the model by one step.'''
        while self.kill_list:
            self.cars_in_destinations += 1
            agent = self.kill_list.pop()
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)
        if self.schedule.steps % self.module == 0:
            self.add_car()
        if self.schedule.steps == 1000:
            self.running = False
        self.schedule.step()