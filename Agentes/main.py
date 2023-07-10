import sys
import pygame as pg
from pygame.locals import *
from pathfind import Node, solve
from entities import Environment


def main():
    finished = False
    HEIGHT = 500
    WIDTH = 500
    
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Test caption')

    clock = pg.time.Clock()
        
    env = Environment()
    env.setup()
    forbidden = [env.obs1.get_cell(),
                 env.obs2.get_cell(),
                 env.obs3.get_cell(),
                 env.obs4.get_cell()]
    

    
    ready_to_push = False

    while True:
        env.render(surface=screen, pg=pg)
        

        for event in pg.event.get():
            if event.type == KEYDOWN:
                try:
                    if event.key == K_n and not finished:
                        box_cell = env.box.get_cell()

                        box_step = get_next_step(start=box_cell,
                                                    target=env.goal.get_cell(),
                                                    forbbiden=forbidden,
                                                    kind='box')
                        print(f'--Box step: {box_step}')

                        target = [2 * (box_cell[0]) - box_step[0], 2 * (box_cell[1]) - box_step[1]]

                        print(f'Agents target: {target}')

                        if env.agent1.get_cell() == target:
                            env.agent1.ready_to_push = True
                            print('1) Ready to push')
                        else:
                            print('1) Not ready to push')
                            env.agent1.ready_to_push = False

                        if env.agent2.get_cell() == target:
                            env.agent2.ready_to_push = True
                            print('2) Ready to push')
                        else:
                            print('2) Not ready to push')
                            env.agent2.ready_to_push = False


                        
                        if not env.agent1.ready_to_push:
                            # print('FOO1')

                            agent1_forbbiden = generate_forbbiden(forbidden, box_cell, env.agent1.get_cell())

                            # print(f'Box step: {box_step}')
                            
                            agent_cell = env.agent1.get_cell()
                            new_coords = get_next_step(start=agent_cell,
                                                        target=target,
                                                        forbbiden=agent1_forbbiden)
                            print(f'--1) Agent step: {new_coords}')
                            
                            env.agent1.coords = env.agent1.cell_to_coords(new_coords)
                            
                            
                        else:
                            
                            print('1) Pushing----------')
     
                    
                            agent_cell = env.agent1.get_cell()
                            new_coords = get_next_step(start=agent_cell,
                                                        target=box_cell,
                                                        forbbiden=forbidden)
                            print(f'--1) Agent step: {new_coords}')
                            
                            
                            env.agent1.coords = env.agent1.cell_to_coords(new_coords)
                            env.box.coords = env.box.cell_to_coords(box_step)

                        if not env.agent2.ready_to_push:
                            # print('FOO1')

                            agent2_forbbiden = generate_forbbiden(forbidden, box_cell, env.agent1.get_cell())

                            # print(f'Box step: {box_step}')
                            
                            agent_cell = env.agent2.get_cell()
                            new_coords = get_next_step(start=agent_cell,
                                                        target=target,
                                                        forbbiden=agent2_forbbiden)
                            print(f'--2) Agent step: {new_coords}')
                            
                            env.agent2.coords = env.agent2.cell_to_coords(new_coords)
                            
                            
                        else:
                            
                            print('2) Pushing----------')
     
                    
                            agent_cell = env.agent2.get_cell()
                            new_coords = get_next_step(start=agent_cell,
                                                        target=box_cell,
                                                        forbbiden=forbidden)
                            print(f'--2) Agent step: {new_coords}')
                            
                            
                            env.agent2.coords = env.agent2.cell_to_coords(new_coords)
                            env.box.coords = env.box.cell_to_coords(box_step)
                            
                           
                            
                            
                        
                        if env.box.get_cell() == env.goal.get_cell():
                            finished = True
                            print('Finished')
                            break
                except Exception as e:
                    print(e)
 
                if event.key == K_r:
                    finished = False
                    env.setup() 
                    forbidden = [env.obs1.get_cell(),
                    env.obs2.get_cell(),
                    env.obs3.get_cell(),
                    env.obs4.get_cell()]
                    print('Restarting...')
                
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()
    
    
#Implementación del PathFinding usando A*
#Esto aún no maneja problemas irresolubles, no śe qué pueda pasar 
def get_next_step(start, target, forbbiden, kind='agent'):
    print(f'Start: {start}, Target: {target}')
    n = Node()
    closed = []
    for f in forbbiden:
        closed.append(f)
    print(f'Forbbiden: {closed}')
    n.value = start
    path = solve(n, target, path = [], closed=closed, open = [])
    if not path: return start
    if kind != 'agent':
        new_closed = None

        while not new_closed:
            new_closed = validate_path(path, forbbiden)
            if new_closed:
                print('Not a valid route, searching...')
                print(f'Start: {start}, Target: {target}')
                n = Node()
                closed = []
                for f in forbbiden:
                    closed.append(f)
                closed.append(new_closed)
                print(f'Forbbiden: {closed}')
                n.value = start
                path = solve(n, target, path = [], closed=closed, open = [])
                if not path:
                    print('Without solution')
                    return start
            else:
                print('Path correct')
                break


    return path[1] if len(path)>1 else path[0]
    
def validate_path(path, forbbiden):
    for i in range(1, len(path)):
        req = [2 * path[i-1][0] - path[i][0], 2 * path[i-1][1] - path[i][1]]
        print(f'From {path[i-1]} to {path[i]}. Required: {req}')
        if req in forbbiden:
            print(f'Req {req} in Closed: {forbbiden}')
            print(f'Pathing from {path[i-1]}')
            return path[i-1]
    return None



def generate_forbbiden(forbbiden, box, agent):
    alt = []
    for f in forbbiden:
        alt.append(f)

    alt.append(box)
    alt.append(agent)
    return alt




if __name__ == '__main__':
    main()
