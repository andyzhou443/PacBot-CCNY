from grid import *
from math import sqrt
from queue import PriorityQueue, Queue

# accounts for north and south
direction_row = [1, -1, 0, 0]
# accounts for east and west
direction_column = [0, 0, 1, -1]
#starting position
starting_pos=(14,7,left)
#goal trying to reach
goal = (4,4)


def neighbors(cell):
    #returns neighboring cells of current vertex
        
    # list to store neighbors
    neighbors = []
    #direction value right->left->up->down
    direction = -1
    # access neighboring cells on the grid
    for i in range(4):
        # checks if neighboring cell is valid
        
        new_row = cell[0] + direction_row[i]
        new_column = cell[1] + direction_column[i]
        direction = i
        # skip invalid cells cells (bounds/walls)
        if new_row < 0 or new_column < 0: pass
        elif new_row >= 30 or new_column >= 28: pass 
        elif grid[new_row][new_column] not in [n,I]: 
                neighbors.append((new_row,new_column,direction))

    return neighbors

#h(n) = sum of the distance between the difference of coordinate components from each node i.e. (x1-x2)+(y2-y1)
def manhattan_distance(start, end):
    x1 = start[0]
    y1 = start[1]

    x2 = end[0]
    y2 = end[1]
    
    return abs(x2-x1)+abs(y2-y1)

#g(n) = pythagorean distance between nodes
def euclidean_distance(start, end):
    x1 = start[0]
    y1 = start[1]

    x2 = end[0]
    y2 = end[1]
    
    return int(sqrt(((x2-x1)**2)+(y2-y1)**2))
    pass

#f(n) = g(n) = f(n)
def heuristic_function(start, end):
    return manhattan_distance(start,end) + euclidean_distance(start,end)



def a_star(starting_pos, goal):
    frontier = PriorityQueue()      #declaring priority q
    frontier.put(starting_pos,0)    #initializing priority queue with starting position
    came_from = dict()              #key=(x,y):value=parent of (x,y)
    cost_so_far=dict()              #key=(x,y):value=actual distance from the start
    
    #starting position does not have a parent or cost by definition
    came_from[starting_pos] = None  
    cost_so_far[starting_pos] = 0

    while not frontier.empty():
        current = frontier.get()

        #terminates loop if we have reached the goal
        #check if x and y of current matches with goal
        if current[0] == goal[0] and current[1] == goal[1]: #doing current = goal ---> (x,y,direction) == (x,y) which would not work
            print("parent of goal node:",came_from[current])
            print("cost so to reach goal:",cost_so_far[current])
            print("path to reach goal:",print_path(current, came_from))

        #exploring neighbors to current cell ("next" is the neighbor of current)
        for next in neighbors(current):
            new_cost = cost_so_far[current] + manhattan_distance(next,current) #computes the total steps travelled if we go to next cell 
            
            #checks if neighboring cell has been already in the dictionary (i.e. already explored) or if we have a found a better path to it (i.e. lesser associated cost)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost                            #add neighbor cell to dictionary along with its associated cost or replace a previous cost entry with a lesser one
                came_from[next]=current                                 #adds the neighbor as key with current cell as the parent of neighbor. If a parent alerady exists, it will be replaced with one which gives lesser cost.
                priority = new_cost + heuristic_function(next, goal)    #computes the estimated cost to get to the goal if we go to the neighbor cell "next".
                frontier.put(next,priority)                             #add neighbor cell to the queue along with its estimated cost. The lesser priority the likelier it will be explored first before others.



def print_path(remote_node, came_from):
    path = []#declare empty list to store path
    path.append(remote_node)#append the remote_node (aka goal node) we want to go to to the end of the list   
    while came_from[remote_node] is not None:   #loop will stop once we reach the source node (aka node with no parent)
        path.append(came_from[remote_node])     #append the parent of "remote_node" to the path since thats where the remote node came from
        remote_node = came_from[remote_node]    #we increment the remote node by overwriting it with its parent
    
    #reverse path since we started from the goal to the source
    path.reverse()
    return path

a_star(starting_pos, goal)
