#!/usr/bin/env python3

from cmath import sqrt
import logging
from netrc import netrc
import os, sys, curses
from typing import Deque
import robomodules as rm
from messages import *
from pacbot.variables import *
from pacbot.grid import *
from collections import deque
from queue import PriorityQueue, Queue
from bfs import bfs
import copy
import serial

DANGER = 10
PELLET_WEIGHT = 0.65
POWER_PELLET_WEIGHT = 0.15
GHOST_WEIGHT = 0.35
FRIGENED_GHOST_WEIGHT = GHOST_WEIGHT**2


# while(i<len(path)):
#     print(path[i][-1])
#     i+=1





SPEED = 2.0
FREQUENCY = SPEED * game_frequency 

# file = open("road.txt", "r")
# i = 0 
# lines= file.read()
# path = ast.literal_eval(lines)

class HighLevel(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE, MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        # self.loop.add_reader(sys.stdin, self.move_stuff)
        self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        self.cur_dir = right
        self.next_dir = right
        self.state = PacmanState()
        self.cherry = None
        self.state.mode = PacmanState.PAUSED
        self.lives = starting_lives
        self.clicks = 0
        # self.p_queue = PriorityQueue()
        self.queue = Deque([[self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]])
        self.i = 1
        self.grid = copy.deepcopy(grid)
        self.path = None
        self.ghost_states = []
        # self.p_queue.put((0, [self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]))      
        

    def _move_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x][y] not in [I, n]:
            self.pacbot_pos[0] += 1
            self.cur_dir = direction
            return True
        elif direction == left and grid[x][y] not in [I, n]:
            self.pacbot_pos[0] -= 1
            self.cur_dir = direction
            return True
        elif direction == up and grid[x][y] not in [I, n]:
            self.pacbot_pos[1] += 1
            self.cur_dir = direction
            return True
        elif direction == down and grid[x][y] not in [I, n]:
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
        if msg_type == MsgType.LIGHT_STATE:
            self.light_state = msg
            self.cherry = self.light_state.cherry

    

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency

        if self.state and self.state.mode != PacmanState.PAUSED:
                self.gameRun()
        pos_buf = PacmanState.AgentState()
        # fil.close()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)

    def _check_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x + 1][y] not in [I, n]:
            return True
        elif direction == left and grid[x - 1][y] not in [I, n]:
            return True
        elif direction == up and grid[x][y + 1] not in [I, n]:
            return True
        elif direction == down and grid[x][y - 1] not in [I, n]:
            return True
        else:
            return False

    def getPath_to_powerPellet(self, starting):
        self.i = 0
        return bfs(self.grid,starting, [O])
    def getPath_to_Pellet(self, starting):
        self.i = 0
        return bfs(self.grid,starting, [o,O])

    def get_move(self):
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        #self, left, right, down, up
        targets = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        heuristics = []
        for target in targets: 
            if(self.grid[target[0]][target[1]] in [I, n]):
                heuristics.append(None)
                continue
            else: 
                dir = self.get_direction(target,(x,y))
                # pellet_dist = len(self.getPath_to_Pellet((dir, target[0], target[1])))
                # powerP_dist = len(self.getPath_to_powerPellet((dir, target[0], target[1])))
                # pellet_heuristic = pellet_dist*PELLET_WEIGHT
                # powerP_heuristic = powerP_dist * POWER_PELLET_WEIGHT
                pellet_path = self.getPath_to_Pellet((dir, x, y))
                pellet_dist = pellet_path
                pellet_heuristic = pellet_dist * PELLET_WEIGHT
                
                power_path = self.getPath_to_powerPellet((dir, x, y))
                power_dist = power_path
                power_heuristic = power_dist * POWER_PELLET_WEIGHT
                print("dist",pellet_heuristic+power_heuristic)
                heuristics.append(pellet_heuristic+power_heuristic)
        
        min_heuristic = float('inf')
        min_target = (0,0)
        for i in range(len(heuristics)):
            if heuristics[i]!=None and (heuristics[i]<= min_heuristic):
                min_heuristic = heuristics[i]
                min_target = targets[i]
        
        return min_target 
        # neighbors = getNeighbors((self.pacbot_pos[0], self.pacbot_pos[1]))
        # ghosts_path = self.getPath_To_Ghost((self.cur_dir,self.pacbot_pos[0], self.pacbot_pos[1]),self.path)
        # min_ghost_dist = float('inf')

        # ghost_heuristic = 0
        # for i in range(len(ghosts_path)):
        #     if min_ghost_dist > len(ghosts_path[i]):
        #         min_ghost_dist = len(ghosts_path[i])
        #         min_ghost_path = ghosts_path
                
        # if DANGER > min_ghost_dist:
        #     if self.ghostsStates() == 1:    #ghost is scared
        #         return min_ghost_path
        #     else: 
        #         ghost_heuristic += pow((DANGER - min_ghost_dist[1]), 2) * GHOST_WEIGHT
    

    def get_heuristic(self):

        pellet_path = self.getPath_to_Pellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]))
        pellet_dist = len(pellet_path) - 1
        pellet_heuristic = pellet_dist * PELLET_WEIGHT
        
        power_path = self.getPath_to_powerPellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]))
        power_dist = len(power_path)
        power_heuristic = power_dist * POWER_PELLET_WEIGHT
        
        min_ghost_dist = float("inf")
        min_ghost_path = []
        ghosts_path = self.getPath_To_Ghost((self.pacbot_pos[0], self.pacbot_pos[1]), self.path)
        for i in range(len(ghosts_path)):
            if len(ghosts_path[i]) < min_ghost_dist:
                min_ghost_dist = len(ghosts_path[i])
                min_ghost_path = copy.deepcopy(ghosts_path[i])

        if DANGER < min_ghost_dist:
            
            if self.ghost_states[0] == 1:
                ghost_heuristic = min_ghost_dist * GHOST_WEIGHT
            else:
                ghost_heuristic = min_ghost_dist * FRIGENED_GHOST_WEIGHT
        
        return pellet_heuristic + power_heuristic + ghost_heuristic 


    def updateGrid(self):
             # updates grid if pellet is ate 
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        if self.grid[x][y] in [o, O]:
            self.grid[x][y] = e
            # print(self.grid[x][y])


          
    def getPath_To_Ghost(self, starting, original_path):
        print("quick hurry ghosts are running!")
        red_ghost_pos = [self.state.red_ghost.direction, self.state.red_ghost.x, self.state.red_ghost.y]
        res = bfs(self.grid, starting, (red_ghost_pos[1], red_ghost_pos[2]), 25)
        path_red = original_path if (res is None) else copy.deepcopy(res)
        
        blue_ghost_pos = [self.state.blue_ghost.direction, self.state.blue_ghost.x, self.state.blue_ghost.y]
        res = bfs(self.grid, starting, (blue_ghost_pos[1], blue_ghost_pos[2]), 25)
        path_blue = original_path if (res is None) else copy.deepcopy(res)
        
        pink_ghost_pos = [self.state.pink_ghost.direction, self.state.pink_ghost.x, self.state.pink_ghost.y]
        res = bfs(self.grid, starting, (pink_ghost_pos[1], pink_ghost_pos[2]), 25)
        path_pink = original_path if (res is None) else copy.deepcopy(res)
        
        orange_ghost_pos = [self.state.orange_ghost.direction, self.state.orange_ghost.x, self.state.orange_ghost.y]
        res = bfs(self.grid, starting, (orange_ghost_pos[1], orange_ghost_pos[2]), 25)
        path_orange = original_path if (res is None) else copy.deepcopy(res)
        # print(red_ghost_pos)
    
        
        self.path = copy.deepcopy(min(path_red, path_blue, path_pink, path_orange, key = len))
        self.i = 0        
        return [path_red, path_blue, path_pink, path_orange]
    
    
    def ghostsStates(self):
        red_ghost_state = 0 if self.state.red_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
            # print("red ghost: ", red_ghost_state)
        blue_ghost_state = 0 if self.state.blue_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
        pink_ghost_state = 0 if self.state.pink_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
        orange_ghost_state = 0 if self.state.orange_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
        self.ghost_states = [red_ghost_state, blue_ghost_state, pink_ghost_state, orange_ghost_state]
        return 1 in self.ghost_states
    
    def ManhattanDist(self, pointA, pointB):
        return abs(pointB[0] - pointA[0]) + abs(pointB[1] - pointA[1])


    # to talk via the serial port from rpi to mcu
    def talkToSerial(self, dir, x, y):
        to_Serial = str(dir) + "X" + "{0:0=2d}".format(x) + "Y" + "{0:0=2d}".format(y) # string format for instructions
        # ser = serial.Serial('/dev/ttyUSB0')  # open serial port
        # print(ser.name)         # check which port was really used
        # print(to_Serial)
        # ser.write(to_Serial)     # write a string
        # ser.close()       # close port
    def printNicely(self):
        sys.stdout.write("\033[F") #back to previous line
        sys.stdout.write("\033[K")
        print("\n"*5)
    

    def get_direction(self, next_loc, prev_loc):
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


    def gameRun(self):
        self.printNicely()
        path = copy.deepcopy(self.getPath_to_Pellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])))
        print(f"path:{path}")

        if path is not None:
            next_loc = (path[0][1],path[0][2])
            x = self.pacbot_pos[0]
            y = self.pacbot_pos[1]
            # dir = get_direction(next_loc, (x,y)) 
            dir = self.get_direction(next_loc, (x,y))
            if (x,y) != next_loc:
                self.talkToSerial(dir, x, y)
                self._move_if_valid_dir(dir , x, y)
        
        self.updateGrid()


        # if self.path is None:
        #     print("new path")
        #     self.path = copy.deepcopy(self.getPath_to_powerPellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])))

        #     print(self.path)
        #     # self.i=1
        # elif(self.path is not None):
        #     # print(self.path[self.i])
        #     # print("state: {}".format(self.cherry))

        #     # self.path = copy.deepcopy(self.getPath_to_powerPellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])))
        #     dir = self.path[self.i][0]
        #     x = self.pacbot_pos[0]
        #     y = self.pacbot_pos[1]
        #     if(self.cherry and self.ManhattanDist((x,y), (13,13))<float("inf")):
        #         self.path = copy.deepcopy(bfs(self.grid, (dir,x,y), (13,13)))
        #         self.i = 1
        #         dir = self.path[self.i][0]
        #         x = self.pacbot_pos[0]
        #         y = self.pacbot_pos[1]
        #     # if self._check_if_valid_dir(dir, x, y):
        #     self.talkToSerial(dir, x, y)
        #     if self._check_if_valid_dir(dir, x, y):
        #         self._move_if_valid_dir(dir , x, y)
        #         self.updateGrid()
        #     # else:
        #     #     self._move_if_valid_dir(self.cur_dir, x,y)

        #     self.i+=1
            

        #     if(self.ghost_states): # 1 if they are scared
        #         self.hunting = 1 
        #         self.getPath_To_Ghost((dir, x, y), self.path)
            
        #     if(self.i >= len(self.path)):
        #         # if self._check_if_valid_dir(self.cur_dir, x, y):
        #             # self._move_if_valid_dir(self.cur_dir, x,y)
        #         self.path = None
        #     #     # return '''      

         

        

def main():
    # ADDRESS = '192.168.1.89'
    # PORT = '11297'
    ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
    PORT = os.environ.get("BIND_PORT", 11297)
    module = HighLevel(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
