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
        dataDictionary = json.load(open("carSimulation/city_files/mapDictionary.json"))

        self.traffic_lights = []
        self.next_agents = 0
        self.finder = get_finder()
        self.world = create_world()
        self.kill_list = []
        self.module = module

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('carSimulation/city_files/2022_base.txt') as baseFile:
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

        for i, pos in enumerate(agent_positions):
            # Check the contents of the position
            position_contents = self.grid.get_cell_list_contents(pos)

            # Check if there is only a road agent at the position
            if any(isinstance(agent, Road) for agent in position_contents) and not any(isinstance(agent, Car) for agent in position_contents):
                car = Car(i + 1000 + self.next_agents, self, pos)
                self.schedule.add(car)
                self.grid.place_agent(car, pos)
                self.next_agents += 2
            else: self.next_agents += 2


    def step(self):
        '''Advance the model by one step.'''
        while self.kill_list:
            agent = self.kill_list.pop()
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)
        if self.schedule.steps % self.module == 0:
            self.add_car()
        self.schedule.step()