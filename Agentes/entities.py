
from random import randint


class Environment():
    def __init__(self) -> None:
        self.entities = []
        
        self.goal = Entity()
        self.goal.kind = 'goal'
        self.goal.color = (99, 144, 101)
        
        self.box = Entity()
        self.box.kind = 'box'
        self.box.color = (132, 109, 100)

        self.obs1 = Obstacle()
        self.obs1.kind = 'obstacle'
        self.obs1.color = (0, 0, 0)
        
        self.obs2 = Obstacle()
        self.obs2.kind = 'obstacle'
        self.obs2.color = (0, 0, 0)
        
        self.obs3 = Obstacle()
        self.obs3.kind = 'obstacle'
        self.obs3.color = (0, 0, 0)
        
        self.obs4 = Obstacle()
        self.obs4.kind = 'obstacle'
        self.obs4.color = (0, 0, 0)
        
        self.agent1 = Agent()
        self.agent1.color = (149, 100, 82)
        self.agent1.kind = 'agent'

        self.agent2 = Agent()
        self.agent2.color = (82, 109, 140)
        self.agent2.kind = 'agent'

        # self.agent1 = Agent()
        # self.agent1.color = (109, 100, 132)
        # self.agent1.kind = 'agent'
        
        # self.agent2 = Agent()
        # self.agent2.color = (109, 50, 132)
        # self.agent2.kind = 'agent'
        
    def setup(self):
        self.entities = []
        
        self.goal.set_position(self.entities)
        self.entities.append(self.goal)
        
        self.box.set_position(self.entities)
        self.entities.append(self.box)
        
        self.obs1.set_position(self.entities)
        self.entities.append(self.obs1)
        
        self.obs2.set_position(self.entities)
        self.entities.append(self.obs2)
        
        self.obs3.set_position(self.entities)
        self.entities.append(self.obs3)
        
        self.obs4.set_position(self.entities)
        self.entities.append(self.obs4)

        self.agent1.set_position(self.entities)
        self.entities.append(self.agent1)

        self.agent2.set_position(self.entities)
        self.entities.append(self.agent2)
        
        # self.agent1.set_position(self.entities)
        # self.entities.append(self.agent1)
        
        # self.agent2.set_position(self.entities)
        # self.entities.append(self.agent2)
        
        
    def draw_grid(self, screen, pg, color):
        cell_size = 50
        grid_size = 10
        grid_width = grid_size * cell_size
        
        for i in range(grid_size + 1): 
            pg.draw.line(screen, color, (i * cell_size, 0), (i * cell_size, grid_width), 3)
            pg.draw.line(screen, color, (0, i * cell_size), (grid_width, i * cell_size), 3)
            
        pg.draw.line(screen, color, (i * cell_size, 0), (i * cell_size, grid_width), 3)
        pg.draw.line(screen, color, (0, i * cell_size), (grid_width, i * cell_size), 3)
        
    
    def render(self, surface, pg):
        surface.fill((50, 50, 50))
        self.draw_grid(surface, pg, (250, 250, 250))
        
        for e in self.entities:
            e.render(pg, surface)


class Entity():
    def __init__(self) -> None:
        self.coords = []
        self.kind = ''
        self.color = (0,0,0)
        
    def render(self, pg, surface):
        pg.draw.rect(surface, self.color, (self.coords[0], self.coords[1], 20, 20))
        
    def cell_to_coords(self, cell, cell_width = 50):
        x = cell[0] * cell_width + 15
        y = cell[1] * cell_width + 15
        return [x, y]
    
    def coords_to_cell(self, coords, cell_width = 50):
        x = coords[0]//cell_width
        y = coords[1]//cell_width
        return [x, y]
    
    def get_cell(self):
        return self.coords_to_cell(self.coords)
    
    
    
    def generate_coords(self):
        if self.kind == 'box' or self.kind == 'agent':
            x = randint(1, 8)
            y = randint(1, 8)
        else: 
            x = randint(0, 9)
            y = randint(0, 9)
        coords = [x, y]
        return coords
                
    def set_position(self, entities):
        tries = 0
        free_space = False
        while not free_space:
            
            tries +=1
            coords = self.generate_coords()
            free_space = True
            for e in entities:
                if self.coords_to_cell(e.coords, 50) == coords:
                    
                    free_space = False
                    break
            
            if tries >= 100 * (len(entities)+1):
                return
            
        self.coords = self.cell_to_coords(coords, 50)
        
   

     

class Agent(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.ready_to_push = False
    def render(self, pg, surface):
        pg.draw.polygon(surface, self.color, ((self.coords[0] , self.coords[1] + 20),
                                              (self.coords[0] + 10, self.coords[1] ),
                                              (self.coords[0] + 20, self.coords[1]+ 20)))
        
class Obstacle(Entity):
    def render(self, pg, surface):
        pg.draw.rect(surface, self.color, (self.coords[0]- 8, self.coords[1]-8, 36, 36))
        pg.draw.rect(surface, (50, 50, 50), (self.coords[0] + 3, self.coords[1] + 3, 14, 14))
 
 

 
 