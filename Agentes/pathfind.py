import math

class Node():
    def __init__(self) -> None:
        self.value = [0,0]
        self.father = None


def solve(current, target, path=[], closed = [], open = []):
    path.append(current.value)
    print(f'Path: {path}')

    if current.value == target:
        print('Founded')
        return path
    
    closed.append(current.value)
    movement = get_moves(current, closed)
    if movement:
        scores = get_scores(movement, target)
        sorted_m = sort_movement(scores, movement)

        for m in sorted_m:
            open.append(m)

    if not open:
        # print('No ways available')
        return None
    
    best = open.pop(-1)
    
    path = solve(best, target, path, closed, open)

    if path:

        return path
        # return path if not current.father else current.value
        # if not current.father:
        #     return next_move
        # else:
        #     return current.value
        
    # print('No ways available')
    return None


def get_moves(current, closed):
    movement = []
    right = [current.value[0] + 1, current.value[1]]

    if current.value[0] < 9 and not right in closed:
        # print(f'{right} is allowed')
        node = Node()
        node.value = right
        node.father = current
        movement.append(node)


    left = [current.value[0] -1, current.value[1]]

    if current.value[0] > 0 and not left in closed:
        # print(f'{left} is allowed')
        node = Node()
        node.value = left
        node.father = current
        movement.append(node)


    up = [current.value[0], current.value[1] - 1]

    if current.value[1] > 0 and not up in closed:
        # print(f'{up} is allowed')
        node = Node()
        node.value = up
        node.father = current
        movement.append(node)


    down = [current.value[0], current.value[1] + 1]

    if current.value[1] < 9 and not down in closed:
        # print(f'{down} is allowed')
        node = Node()
        node.value = down
        node.father = current
        movement.append(node)

    return movement

manhattan = lambda y, y_hat: abs(y_hat[0] - y[0]) + abs(y_hat[1] - y[1])
euclidean = lambda y, y_hat: math.sqrt((y_hat[0] - y[0])**2 + (y_hat[1] - y[1])**2)


def get_scores(movement, target):
    scores = []
    for m in movement:
        s = manhattan(m.value, target)
        s += euclidean(m.value, target)
        scores.append(s)
    return scores



def sort_movement(scores, movement):
    for j in range(1, len(scores)):
        key = scores[j]
        _aux_key = movement[j]
        i = j - 1
        while i >= 0 and scores[i] < key:
            scores[i + 1] = scores[i]
            movement[i + 1] = movement[i]
            i -= 1
        scores[i + 1] = key
        movement[i + 1] = _aux_key
    return movement
