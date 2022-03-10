#!/usr/bin/env python3

import os, sys, curses
import robomodules as rm
from messages import *
from pacbot.variables import *
from pacbot.grid import *
from collections import deque
from util import *  

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

SPEED = 1.0
FREQUENCY = SPEED * game_frequency 

class InputModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        # self.loop.add_reader(sys.stdin, self.move_stuff)
        self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        self.cur_dir = right
        self.next_dir = right
        self.state = PacmanState()
        self.state.mode = PacmanState.PAUSED
        self.lives = starting_lives
        self.clicks = 0
        self.queue = deque([[self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]])
        self.discovered = set()



    def _move_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x + 1][y] not in [I, n]:
            self.pacbot_pos[0] += 1
            self.cur_dir = direction
            return True
        elif direction == left and grid[x - 1][y] not in [I, n]:
            self.pacbot_pos[0] -= 1
            self.cur_dir = direction
            return True
        elif direction == up and grid[x][y + 1] not in [I, n]:
            self.pacbot_pos[1] += 1
            self.cur_dir = direction
            return True
        elif direction == down and grid[x][y - 1] not in [I, n]:
            self.pacbot_pos[1] -= 1
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
                self.bfs()
        pos_buf = PacmanState.AgentState()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)

    # CATS VERSION
    def _check_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x + 1][y] not in [I, n]:
            return True
        elif direction == left and grid[x - 1][y] not in [I, n]:
            return True
        elif direction == up and grid[x][y + 1] not in [I, n]:
            return True
        elif direction == down and grid[x][y - 1] not in [I, n]:
            return True
        return False
    
    def _check_if_valid_dir(self, direction, x, y):
        # "dirrection == some_direction" is weird (i.e you can only move to the right if 
        #  pacman is facing to the right regardless if there's any path open)
        
        #right
        if grid[x + 1][y] not in [I, n]:
            self.cur_dir = right
            return True
        #left
        elif grid[x - 1][y] not in [I, n]:
            self.cur_dir = left
            return True
        #up
        elif grid[x][y + 1] not in [I, n]:
            self.cur_dir = up
            return True
        #down
        elif grid[x][y - 1] not in [I, n]:
            self.cur_dir = down
            return True
        return False



    def dfs(self):
        # stack = []
        # self.queue.append([self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]])
        print(self.queue)
        current = self.queue.popleft()
        if(self._check_if_valid_dir(current[0], current[1], current[2])):# cheks if there's any valid directions to move to
            self._move_if_valid_dir(current[0], current[1], current[2])  # moves pacman to the first direction possible
            #saves details about pacman current state in the game
            current[0] = self.cur_dir 
            current[1] = self.pacbot_pos[0]
            current[2] = self.pacbot_pos[1]
            #appends current position to queue
            self.queue.append([current[0], current[1], current[2]]) #why add to the queue?
        else:
            # if(not self._check_if_valid_dir(current[0], current[1], current[2])):
            if (self._check_if_valid_dir(up, current[1], current[2]) and grid[current[1]][current[2]+1] in [o, O]):
                self.queue.append([up, current[1], current[2]])
            elif (self._check_if_valid_dir(right, current[1], current[2]) and grid[current[1]+1][current[2]] in [o, O]):
                self.queue.append([right, current[1], current[2]])
            elif (self._check_if_valid_dir(down, current[1], current[2]) and grid[current[1]][current[2]-1] in [o, O]):
                self.queue.append([down, current[1], current[2]])
            elif (self._check_if_valid_dir(left, current[1], current[2]) and grid[current[1]-1][current[2]] in [o, O]):
                self.queue.append([left, current[1], current[2]])
            
           

    def bfs(self):
        #random goal for testing purposes
        goal = grid[10][25]
        #keep track of pacbot current state
        current = [self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]
        #the cell we are going to explore
        node = {'state': current, 'cost': 0}

        #returns a list of the path once current position = goal
        if goal == node["state"]: 
            return []
        # creating a queue with node as the only element
        frontier = Queue()
        frontier.append(node)
        #explored = an empty set
        explored = set()
        
        while True:
            # if queue is empty, return False
            if frontier.isEmpty():
                raise Exception('Search Failed!')
            
            #chooses the shallowest path
            node = frontier.pop()
            #add node.state to explored
            explored.add(node['state'])

        # if self._check_if_valid_dir(current[0], current[1], current[2]):
        #     current[0] = self.cur_dir
        #     self._move_if_valid_dir(current[0], current[1], current[2])

    #this should take the current cell we're exploring
    def neighboring_cells(self,being_explored):
    #returns neighboring cells of current vertex
        
        #this only works for the starting position
        cell = [self.pacbot_pos[0], self.pacbot_pos[1]]

        # accounts for north and south
        direction_row = [-1, 1, 0, 0]
        # accounts for east and west
        direction_column = [0, 0, 1, -1]
        # list to store neighbors
        neighbors = []
        # access neighboring cells on the grid
        for i in range(4):
            new_row = cell[1] + direction_row[i]
            new_column = cell[2] + direction_column[i]
        # skip invalid cells cells (bounds/walls). 
        if new_row < 0 or new_column < 0: pass
        elif new_row > 27 or new_column > 30: pass 
        else:
            neighbors.append([new_row,new_column])

        return neighbors
    




def main():
    module = InputModule(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
