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





SPEED = 1.0
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
        return bfs(self.grid,starting, [o])
        # return

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
    


    def gameRun(self):
        self.printNicely()
        if self.path is None:
            print("new path")
            self.path = copy.deepcopy(self.getPath_to_powerPellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])))

            print(self.path)
            self.i=1
        elif(self.path is not None):
            # print(self.path[self.i])
            # print("state: {}".format(self.cherry))

            # self.path = copy.deepcopy(self.getPath_to_powerPellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])))
            dir = self.path[self.i][0]
            x = self.pacbot_pos[0]
            y = self.pacbot_pos[1]
            if(self.cherry and self.ManhattanDist((x,y), (13,13))<float("inf")):
                self.path = copy.deepcopy(bfs(self.grid, (dir,x,y), (13,13)))
                self.i = 1
                dir = self.path[self.i][0]
                x = self.pacbot_pos[0]
                y = self.pacbot_pos[1]
            
            # if self._check_if_valid_dir(dir, x, y):
            self.talkToSerial(dir, x, y)
            self._move_if_valid_dir(dir , x, y)
            self.updateGrid()
            # else:
            #     self._move_if_valid_dir(self.cur_dir, x,y)

            self.i+=1
            

            # if(self.ghost_states): # 1 if they are scared
                # self.hunting = 1 
                # self.getPath_To_Ghost((dir, x, y), self.path)
            
            if(self.i >= len(self.path)):
                # if self._check_if_valid_dir(self.cur_dir, x, y):
                    # self._move_if_valid_dir(self.cur_dir, x,y)
                self.path = None
            #     # return
    # def 
             


           

        

def main():
    # ADDRESS = '192.168.1.89'
    # PORT = '11297'
    ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
    PORT = os.environ.get("BIND_PORT", 11297)
    module = HighLevel(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
