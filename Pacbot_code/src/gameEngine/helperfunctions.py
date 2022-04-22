from pacbot.variables import *
from pacbot.grid import *
from math import *

def getNeighbors(cell):
    '''returns valid neighbors of current vertex'''
    direction_row = [1, -1, 0, 0]
    # accounts for east and west
    direction_column = [0, 0, 1, -1]
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
                neighbors.append((new_row,new_column))

    return neighbors


def get_direction(next_loc, prev_loc):
    '''computes direction based on current position and new position'''
    direction = -1  
    if next_loc[1] == prev_loc[1]:
        if next_loc[0] > prev_loc[0]:
            direction = right
        elif next_loc[0] < prev_loc[0]:
            direction = left
    elif next_loc[0] == prev_loc[0]:
        if next_loc[1] > prev_loc[1]:
            direction = up
        elif next_loc[1] < prev_loc[1]:
            direction = down
    # print('direction:', direction)
    return direction


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

def heuristic_function(start, end):
    return manhattan_distance(start,end) + euclidean_distance(start,end)