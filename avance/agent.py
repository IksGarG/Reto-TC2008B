from mesa import Agent
from pathfinding.core.world import World
from GridGen.grid_gen import gDown, gUp, gLeft, gRight

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, initial_pos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.path = []
        self.current_step = 0
        self.position = initial_pos
        self.init_path_gen()
        self.waiting_time = 0
        self.random_destination, self.road_near_destination = self.destination()

    def grid_cleanup(self, world):
        for grid in world.grids.values():
            grid.cleanup()

    def destination(self):
        destinations = [agent for agent in self.model.schedule.agents if isinstance(agent, Destination)]
        
        if destinations:
            random_destination = self.random.choice(destinations)  # Select a random Destination agent

            neighbors = self.model.grid.get_neighbors(
                random_destination.pos,
                moore=False,  # Include diagonals
                include_center=False)
        
        road_near_destination = [agent for agent in neighbors if isinstance(agent, Road)]  # Select the road near the destination
        return random_destination, road_near_destination

    def is_path_clear(self):
        lookahead_steps = 1 # How many steps to look ahead
        front_neighbor_pos = self.get_front_neighbor_position()
        contents = self.model.grid.get_cell_list_contents(front_neighbor_pos)
        if any(isinstance(obj, Car) and obj != self for obj in contents):
            return False
        
        # Check the upcoming positions in the path
        for step in range(self.current_step, min(self.current_step + lookahead_steps, len(self.path))):
            grid_node = self.path[step]
            x, y = grid_node.x, grid_node.y  # Directly access x and y from the GridNode object
            path_contents = self.model.grid.get_cell_list_contents((x, y))
            if any(isinstance(obj, Car) and obj != self for obj in path_contents):
                return False
        return True

    def is_light_green(self):
        front_neighbor_pos = self.get_front_neighbor_position()
        contents = self.model.grid.get_cell_list_contents(front_neighbor_pos)
        traffic_lights = [obj for obj in contents if isinstance(obj, Traffic_Light)]    
        if traffic_lights:
            return traffic_lights[0].state == True
        return True  # If no traffic light, assume it's okay to move

    def get_front_neighbor_position(self):
        """
        Get the position of the front-facing neighbor based on the road direction.
        """
        current_road = self.model.grid.get_cell_list_contents([self.pos])[0]
        direction = current_road.direction

        if direction == "Up":
            return (self.pos[0], self.pos[1] + 1)
        elif direction == "Down":
            return (self.pos[0], self.pos[1] - 1)
        elif direction == "Right":
            return (self.pos[0] + 1, self.pos[1])
        elif direction == "Left":
            return (self.pos[0] - 1, self.pos[1])


    def init_path_gen(self):

        random_destination, road_near_destination = self.destination()

        gridEND = None # Default value

        if road_near_destination:
            road_direction = road_near_destination[0].direction
            if road_direction == "Down":
                gridEND = gUp.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND
            
            elif road_direction == "Up":
                gridEND = gDown.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND
            
            elif road_direction == "Right":
                gridEND = gRight.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND
            
            elif road_direction == "Left":
                gridEND = gLeft.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND

        if gridEND is not None:

            if self.position == (0, 24):
                self.grid_cleanup(self.model.world)
                path, _ = self.model.finder.find_path(gUp.node(0, 24), gridEND, self.model.world)
                self.path = path


            elif self.position == (23, 24):
                self.grid_cleanup(self.model.world)
                path, _ = self.model.finder.find_path(gLeft.node(23, 24), gridEND, self.model.world)
                self.path = path

            elif self.position == (23, 0):
                self.grid_cleanup(self.model.world)
                path, _ = self.model.finder.find_path(gDown.node(23, 0), gridEND, self.model.world)
                self.path = path

            elif self.position == (0, 0):
                self.grid_cleanup(self.model.world)
                path, _ = self.model.finder.find_path(gRight.node(0, 0), gridEND, self.model.world)
                self.path = path

    def recalculate_path(self):
        current_cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        current_road_segment = next((obj for obj in current_cell_contents if isinstance(obj, Road) and obj != self), None)

        if current_road_segment is not None:
            self.choose_new_grid_based_on_road(current_road_segment)

    def choose_new_grid_based_on_road(self, road_segment):
        road_direction = road_segment.direction

        if road_direction == "Up":
            start = gDown.node(self.pos[0], self.pos[1])
        elif road_direction == "Down":
            start = gUp.node(self.pos[0], self.pos[1])
        elif road_direction == "Right":
            start = gRight.node(self.pos[0], self.pos[1])
        elif road_direction == "Left":
            start = gLeft.node(self.pos[0], self.pos[1])

        self.recalculate_a_star_path(start)
    
    def recalculate_a_star_path(self, start):
        # Your logic to recalculate the path using the A* algorithm
        # Example:
        random_destination, road_near_destination = self.random_destination, self.road_near_destination

        gridEND = None # Default value

        if road_near_destination:
            road_direction = road_near_destination[0].direction
            if road_direction == "Down":
                gridEND = gUp.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND
            
            elif road_direction == "Up":
                gridEND = gDown.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND
            
            elif road_direction == "Right":
                gridEND = gRight.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND
            
            elif road_direction == "Left":
                gridEND = gLeft.node(random_destination.pos[0], random_destination.pos[1])
                self.gridEND = gridEND

        self.grid_cleanup(self.model.world)
        path, _ = self.model.finder.find_path(start, gridEND, self.model.world)
        self.path = path
        self.current_step = 0

    def is_tile_empty_and_road(self, x, y):
        # Check if the coordinates are within the grid boundaries
        grid_width = self.model.grid.width
        grid_height = self.model.grid.height
        if x < 0 or y < 0 or x >= grid_width or y >= grid_height:
            return False  # Coordinates are out of grid bounds

        contents = self.model.grid.get_cell_list_contents((x, y))
        if not contents:
            return False  # Tile is not empty

        return any(isinstance(obj, Road) for obj in contents)

    def try_moving_to_adjacent_tile(self):
        current_road = self.model.grid.get_cell_list_contents([self.pos])[0]
        direction = current_road.direction

        # Define potential move positions with diagonal options first
        move_options = {
            "Up": [(self.pos[0] + 1, self.pos[1] + 1), (self.pos[0] - 1, self.pos[1] + 1), (self.pos[0], self.pos[1] + 1)],
            "Down": [(self.pos[0] + 1, self.pos[1] - 1), (self.pos[0] - 1, self.pos[1] - 1), (self.pos[0], self.pos[1] - 1)],
            "Right": [(self.pos[0] + 1, self.pos[1] + 1), (self.pos[0] + 1, self.pos[1] - 1), (self.pos[0] + 1, self.pos[1])],
            "Left": [(self.pos[0] - 1, self.pos[1] + 1), (self.pos[0] - 1, self.pos[1] - 1), (self.pos[0] - 1, self.pos[1])],
        }

        grid_width = self.model.grid.width
        grid_height = self.model.grid.height

        for option in move_options.get(direction, []):
            x, y = option
            if x >= 0 and y >= 0 and x < grid_width and y < grid_height:
                if self.is_tile_empty_and_road(x, y):
                    self.model.grid.move_agent(self, option)
                    return True

        return False

        
    def move(self):
        max_waiting_time = 20  # Define a threshold for maximum waiting time
        print(self.waiting_time)
        if self.current_step < len(self.path):
            next_position = self.path[self.current_step]
            x, y = next_position.x, next_position.y

            if self.is_path_clear() and self.is_light_green():
                self.model.grid.move_agent(self, (x, y))
                self.current_step += 1
                self.waiting_time = 0  # Reset waiting time
            else:
                self.waiting_time += 1
                if self.waiting_time > max_waiting_time:
                    if self.try_moving_to_adjacent_tile():
                        self.recalculate_path()
                        self.waiting_time = 0
                    else:
                        return  # Do nothing if the car is stuck

            if self.current_step == len(self.path):
                self.model.kill_list.append(self)




    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()


class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
