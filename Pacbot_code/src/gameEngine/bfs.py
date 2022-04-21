from collections import deque
import copy
from importlib.resources import path
import grid
from math import floor
# Direction enums
right = 0
left = 1
up = 2
down = 3

# Grid enums
# o = normal pellet, e = empty space, O = power pellet, c = cherry position
# I = wall, n = ghost chambers
I = 1
o = 2
e = 3
O = 4
n = 5
c = 6

grid = [[I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I], # 0
        [I,o,o,o,o,I,I,O,o,o,o,I,e,e,e,e,e,e,e,e,e,I,o,o,o,o,o,O,o,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,I,I,I,I,I,I,I,I,I,I,o,I,I,o,I,I,I,o,I], # 5
        [I,o,I,I,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,I,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,e,e,e,e,e,e,e,e,e,I,I,o,o,o,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,I,I,I,I,e,I,I,o,I,I,o,I,e,I,o,I], # 10
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,n,n,n,I,e,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,o,o,o,I,I,o,o,o,o,I,I,e,I,n,n,n,I,e,e,e,o,I,I,o,o,o,o,o,I],
        [I,o,I,I,I,I,I,e,I,I,I,I,I,e,I,n,n,n,n,e,I,I,I,I,I,o,I,I,I,I,I],
        [I,o,I,I,I,I,I,e,I,I,I,I,I,e,I,n,n,n,n,e,I,I,I,I,I,o,I,I,I,I,I], # starting point here
        [I,o,o,o,o,I,I,o,o,o,o,I,I,e,I,n,n,n,I,e,e,e,o,I,I,o,o,o,o,o,I], # 15
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,n,n,n,I,e,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,I,I,I,I,e,I,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,e,e,e,e,e,e,e,e,e,I,I,o,o,o,o,I,e,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,e,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,I,I,o,I], # 20
        [I,o,I,I,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,I,I,I,I,I,I,I,I,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,I,I,o,I], # 25
        [I,o,o,o,o,I,I,O,o,o,o,I,e,e,e,e,e,e,e,e,e,I,o,o,o,o,o,O,o,o,I],
        [I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I]]
#        |         |         |         |         |         |         |   top right of pacman board
#        0         5        10        15       20         25       30

f = open("aftergrid.txt", "w")
f.write(str(grid).replace('],','],\n'))
f.close() 

def bfs(grid, start, target, max_dist=float('inf')):
    min_length = 9999
    shortest_path = []
    visited = set()
    queue = [(start, [])]
    loc = (start[1], start[2])

    while len(queue) != 0:
        next = queue.pop(0)
        # add the current node to the visited set
        visited.add(next[0][1:])
        # grid[next[0][1]][next[0][2]] = e
        # copy the path that lead to our current location
        new_path = copy.deepcopy(next[1])
        # append the current node to it
        new_path.append(next[0])
        # update the location
        loc = next[0][1:]
        # grid[loc[0]][loc[1]] = e
        loc_value = grid[loc[0]][loc[1]]
        print(f"loc:{loc}")
        print(f"new_Path:{new_path}")
        print(f"path_length:{len(new_path)}\tmin_length:{min_length}")
        print(f"grid:{loc_value} \t{target}\t e:{e} ")

        # if we are at the tuple, which denotes the end point
        if type(target) is tuple and len(new_path) <= min_length:
            if target == loc:
                shortest_path = copy.deepcopy(new_path)
                print(new_path)
                return new_path[1:]
        # if we are looking just for a certain point(like a power pellets) ?
        elif (loc_value in target) and (len(new_path) <= min_length) and (len(new_path) > 0):
            print(f"path length: {len(new_path)}")
            # grid[loc[0]][loc[1]] = e
            min_length = len(new_path)
            shortest_path = copy.deepcopy(new_path)
            # return new_path
        
        # for each neighbor we append, add the path that leads to it
        if grid[loc[0] + 1][loc[1]] not in [I, n] and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((right ,loc[0] + 1, loc[1]),new_path))
        if grid[loc[0] - 1][loc[1]] not in [I, n] and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((left, loc[0] - 1, loc[1]),new_path))
        if grid[loc[0]][loc[1] + 1] not in [I, n] and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
            queue.append(((up, loc[0], loc[1] + 1),new_path))
        if grid[loc[0]][loc[1] - 1] not in [I, n] and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
            queue.append(((down, loc[0], loc[1] - 1),new_path))

    if len(shortest_path) >= 1:
        return shortest_path[1:]
    else: 
        print(f"start {start}\t target: {target}")
        return None


