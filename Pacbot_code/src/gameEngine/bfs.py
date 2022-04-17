from collections import deque
import copy
import grid
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
    visited = set()
    # in queue current node-ish and the path leading to it
    queue = [(start, [])]
    # print(f"current: {start}\ntarget: {target}")
    loc = (start[1], start[2])
    while len(queue) != 0:
        # 
        next = queue.pop(0)
        # print(f"next: {next}")
        # add the current node to the visited set
        visited.add(next[0][1:])
        # grid[next[0][1]][next[0][2]] = e
        grid[loc[0]][loc[1]] = e
        # f = open("aftergrid.txt", "w")
        # f.write(str(grid).replace('],','],\n'))
        # f.close() 
        # print(f"visited: {visited}")
        # copy the path that lead to our current location
        new_path = copy.deepcopy(next[1])
        # print(f"new path: {new_path}")
        # append the current node to it
        new_path.append(next[0])
        # update the location
        loc = next[0][1:]
        # print(f"loc: {loc}")
        # if we are at the tuple, which denotes the end point
        if type(target) is tuple:
            if target == loc:
                return new_path
        # if we are looking just for a certain point(like a power pellets) ?
        elif grid[loc[0]][loc[1]] in target:
            grid[loc[0]][loc[1]] = e
            return new_path
        
        # for each neighbor we append, add the path that leads to it
        if grid[loc[0] + 1][loc[1]] in [o, e, O] and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((right ,loc[0] + 1, loc[1]),new_path))
        if grid[loc[0] - 1][loc[1]] in [o, e, O] and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((left, loc[0] - 1, loc[1]),new_path))
        if grid[loc[0]][loc[1] + 1] in [o, e, O] and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
            queue.append(((up, loc[0], loc[1] + 1),new_path))
        if grid[loc[0]][loc[1] - 1] in [o, e, O] and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
            queue.append(((down, loc[0], loc[1] - 1),new_path))
    return None


# start = (right,14, 7)
# target = [O]
# result = bfs(grid, start, target)
# print(f"path = {result}")
# start = result[-1]
# result  = bfs(grid, start, target)
# print(f"path = {result}")
# start = result[-1]
# result  = bfs(grid, start, target)
# print(f"path = {result}")
# start = result[-1]
# result  = bfs(grid, start, target)
# print(f"path = {result}")
# start = result[-1]
# result  = bfs(grid, start, target)
# print(f"path = {result}")