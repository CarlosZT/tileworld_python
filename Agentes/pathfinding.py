import math
class Node():
    def __init__(self) -> None:
        self.neighbors = []
        self.parent = None
        self.value = None
        
def heuristic(possibles, target):
    score = []
    for p in possibles:
        s = abs(p.value[0] - target[0]) + abs(p.value[1] - target[1])
        s += math.sqrt((p.value[0] - target[0])**2 + (p.value[1] - target[1])**2)
        score.append(s)
    return score


def get_possibles(current, Q_coords, x_limits=(0,9), y_limits=(0,9)):
    available = []
    coords = current.value
    
    if coords[0] >= x_limits[0] and coords[0] <= x_limits[1]:
        if coords[0] > x_limits[0] and not [coords[0]-1, coords[1]] in Q_coords:
            left = Node()
            left.value = [coords[0]-1, coords[1]]
            left.parent = current
            current.neighbors.append(left)
            available.append(left)
        
        if  coords[0] < x_limits[1] and not [coords[0]+1, coords[1]] in Q_coords:
            right = Node()
            right.value = [coords[0]+1, coords[1]]
            right.parent = current
            current.neighbors.append(right)
            available.append(right)
            
    if coords[1] >= y_limits[0] and coords[1] <= y_limits[1]:      
        if coords[1] < y_limits[1] and not [coords[0], coords[1]+1] in Q_coords:
            down = Node()
            down.value = [coords[0], coords[1]+1]
            down.parent = current
            current.neighbors.append(down)
            available.append(down)
            
        if coords[1] > y_limits[0] and not [coords[0], coords[1]-1] in Q_coords:
            up = Node()
            up.value = [coords[0], coords[1]-1]
            
            up.parent = current
            current.neighbors.append(up)
            available.append(up)    
    return available
    
    
def get_best(score, possibles, P, P_coords):
    best = score[0]
    index = 0
    for_open = []
    for i, s in enumerate(score):
        if best > s:
            for_open.append(possibles[index])
            best = s
            index = i
    
    for o in for_open:
        if not o.value in P_coords:
            P.append(o)
            P_coords.append(o.value)
            
    print(f'Size {len(possibles)}, index: {index}')
        
    return possibles[index], P, P_coords


class PathFinding():
    def __init__(self) -> None:
        self.P = []
        # self.Q = []
        self.P_coords = []
        self.Q_coords = []
        
    def clean(self):
        self.P = []
        # self.Q = []
        self.P_coords = []
        self.Q_coords = []
        

    def solve(self, current:Node, target, solver):
        # print(f'Received: {current.value}')
        
        # solver.Q.append(current)
        solver.Q_coords.append(current.value)
        if current.value == target:     #Si llegamos al objetivo
            return current
            
        else:                           #Si NO llegamos al objetivo
            possibles = get_possibles(current, solver.Q_coords)
            
            if len(possibles) > 0:      #Si hay al menos un movimiento disponible
                score = heuristic(possibles, target)
                next_move, solver.P, solver.P_coords = get_best(score, possibles, solver.P, solver.P_coords)
                
                result = self.solve(next_move, target, solver)
                # print(f'Result obtained: {result.value}')
                
               
                while result == None and len(solver.P)>0 : #Esto deberia morir si y solo si el problema es irresoluble
                    score = heuristic(solver.P, target)
                    next_move, solver.P, solver.P_coords = get_best(score, possibles, solver.P, solver.P_coords)
                    result = self.solve(next_move, target, solver)
                
                if result == None and len(solver.P)==0:
                    print('Irresoluble')
                    return None
                  

                if current.parent == None:
                    return result
                return current
                    
            else:   #No hay movimientos posibles
                return None
                
            
            

    
    