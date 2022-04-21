#!/usr/bin/env python3

import os, sys, curses
import robomodules as rm
from messages import *
from pacbot.variables import *
from pacbot.grid import *
from math import sqrt
from queue import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)


SPEED = 1.0
FREQUENCY = SPEED * game_frequency 

# accounts for north and south
direction_row = [1, -1, 0, 0]
# accounts for east and west
direction_column = [0, 0, 1, -1]
#goal trying to reach
goal = (6,20)


class InputModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        # self.loop.add_reader(sys.stdin, self.move_stuff)
        # self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        self.pacbot_pos = (pacbot_starting_pos[0], pacbot_starting_pos[1])
        self.cur_dir = left
        self.next_dir = right
        self.state = PacmanState()
        self.state.mode = PacmanState.PAUSED
        self.lives = starting_lives
        self.clicks = 0
        # self.queue = ([[self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]])
        # A star relevant stuff
        global goal
        self.frontier = PriorityQueue()
        self.frontier.put((self.pacbot_pos[0], self.pacbot_pos[1]),0)
        self.came_from = {}
        self.cost_so_far = {}
        self.path = []
        self.came_from[(self.pacbot_pos[0], self.pacbot_pos[1])] = None
        self.cost_so_far[(self.pacbot_pos[0], self.pacbot_pos[1])] = 0
        self.goalFound = False #when a* finds goal cell
        self.destination = None   #when desin
        self.destination_reached = False

        #when the goal is explored
        #when path is computed
        #when we are moving to goal
        #when we don't have a goal
        #when we have a goal

    def _move_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x][y] not in [I, n]:
            # x +=1
            self.pacbot_pos = (x,y)
            self.cur_dir = direction
            return True
        elif direction == left and grid[x][y] not in [I, n]:
            # x -=1
            self.pacbot_pos = (x,y)
            self.cur_dir = direction
            return True
        elif direction == up and grid[x][y] not in [I, n]:
            # y +=1
            self.pacbot_pos = (x,y)
            self.cur_dir = direction
            return True
        elif direction == down and grid[x][y] not in [I, n]:
            # y -=1
            self.pacbot_pos = (x,y)
            self.cur_dir = direction
            return True
        return False



    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        if msg_type == MsgType.FULL_STATE:
            self.state = msg
            if self.state.lives != self.lives:
                self.lives = self.state.lives
                self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]



    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        if self.state.mode != PacmanState.PAUSED:
            # if not self._move_if_valid_dir(self.next_dir, self.pacbot_pos[0], self.pacbot_pos[1]):
                # self._move_if_valid_dir(self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])
                # self.dfs()
                self.a_star()
                print(grid[goal[0]][goal[1]])
                # if self.goalFound == True and goal not in [o, O]:
                #     self.bfs((self.pacbot_pos[0], self.pacbot_pos[1]))
                #     self.goalFound = False 

                if self.goalFound == False:
                    self.destination = self.a_star()
                elif self.goalFound == True and len(self.path) == 0:
                    self.get_path(self.destination)
                elif len(self.path) > 0 and self.goalFound == True:
                    self.make_move()
                    self.update_grid()

        pos_buf = PacmanState.AgentState()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)


    #h(n) = sum of the distance between the difference of coordinate components from each node i.e. (x1-x2)+(y2-y1)
    def manhattan_distance(self, start, end):
        x1 = start[0]
        y1 = start[1]

        x2 = end[0]
        y2 = end[1]
        
        return abs(x2-x1)+abs(y2-y1)

    #g(n) = pythagorean distance between nodes
    def euclidean_distance(self, start, end):
        x1 = start[0]
        y1 = start[1]

        x2 = end[0]
        y2 = end[1]
        
        return int(sqrt(((x2-x1)**2)+(y2-y1)**2))

    #f(n) = g(n) = f(n)
    def heuristic_function(self, start, end):
        return self.manhattan_distance(start,end) + self.euclidean_distance(start,end)

    def neighbors(self,cell):
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
                    neighbors.append((new_row,new_column))

        return neighbors

    def a_star(self):

        while not self.frontier.empty():
            current = self.frontier.get()
            print(current)

            if current[0] == goal[0] and current[1] == goal[1]:
                self.goalFound = True
                # self.get_path(current)
                # if len(self.path) == 0:   
                #     self.get_path(current)
                # else: 
                #     next_move = self.path.pop()
                #     self._move_if_valid_dir(next_move[2],next_move[0],next_move[1])
                # return
                return current

            for next in self.neighbors(current):
                new_cost = self.cost_so_far[current] + self.manhattan_distance(next,current) #computes the total steps travelled if we go to next cell 

                if next not in self.cost_so_far or new_cost < self.cost_so_far[next]:
                    self.cost_so_far[next] = new_cost                            #add neighbor cell to dictionary along with its associated cost or replace a previous cost entry with a lesser one
                    self.came_from[next]=current                                 #adds the neighbor as key with current cell as the parent of neighbor. If a parent alerady exists, it will be replaced with one which gives lesser cost.
                    priority = new_cost + self.heuristic_function(next, goal)    #computes the estimated cost to get to the goal if we go to the neighbor cell "next".
                    self.frontier.put(next,priority)  
        
    def get_path(self,remote_node):
        # this function modifies self.path = []
        print('getting path...')
        self.path.append(remote_node)                       #append the remote_node (aka goal node) we want to go to to the end of the list   
        while self.came_from[remote_node] is not None:      #loop will stop once we reach the source node (aka node with no parent)
            self.path.append(self.came_from[remote_node])   #append the parent of "remote_node" to the path since thats where the remote node came from
            remote_node = self.came_from[remote_node]       #we increment the remote node by overwriting it with its parent
        print('path computed!')

    def make_move(self):
            next_move = self.path.pop()
            print(f'going to {next_move}')
            direction = get_direction(next_move, self.pacbot_pos)
            self._move_if_valid_dir(direction,next_move[0],next_move[1])

            if len(self.path) == 0:
                goal = None
                self.goal_reached = True
    

    def update_grid(self):
        # updates grid if pellet is ate 
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        if grid[x][y] in [o, O]:
            grid[x][y] = e
            print(grid[x][y])

    def bfs(self, position):

        # queue.put(position)
        # while not queue.empty(): # the BFS will happen until the queue is empty
        #     u = queue.get() #pops the first element of the queue and sets it to u (to mark as visited and add its neighbors to the queue)
        #     bfs_traversal_output.append(u)  #adds u to the traversal path

        #     if u in [o, O]:
        #         goal = (u[0], u[1])
        #         return goal

        #     # explores all adjacent vertices of u:
        #     for v in self.neighbors(u):
        #         #checks if adj vertex (v) have not been visited:
        #         if not visited[v]:
        #             visited[v] = True #marks v as visited
        #             parent[v] = u     #sets u (the node which we are exploring its neighbors) as the parent of v (adj vertex) since its the first and only time
        #             level[v] = level[u] + 1 #since u is the parent of v, v must have +1 level than it
        #             print(v)         
        #             queue.put(v)  
        pass

# to keep track of visited nodes:
visited = {}
# to keep track of the distance from the source node:
level = {}
# to keep track of the parent of each node:
parent = {} # useful for: computing the minimum distance from a parent node to any other node as well as the path
# order of BFS traversal:
bfs_traversal_output = []
queue = Queue()


def get_direction(next_loc, prev_loc):
    #computes direction based on current position and new position
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
    print('direction', direction)
    return direction
    

def find_pellet(self):
    current_pos = self.pacbot_pos
        

def main():
    module = InputModule(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
