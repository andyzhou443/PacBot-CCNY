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
        # self.p_queue = PriorityQueue()
        self.queue = Deque([[self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]])
        self.i = 1
        self.grid = copy.deepcopy(grid)
        self.path = None
        # self.temp = [(0, 14, 7), (0, 15, 7), (0, 16, 7), (0, 17, 7), (0, 18, 7), (0, 19, 7), (0, 20, 7), (0, 21, 7), (2, 21, 8), (2, 21, 9), (2, 21, 10), (0, 22, 10), (0, 23, 10), (0, 24, 10), (0, 25, 10), (0, 26, 10), (3, 26, 9), (3, 26, 8), (3, 26, 7)]
        # self.p_queue.put((0, [self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]]))      
        

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
        self.i = 1
        return bfs(self.grid,starting, [O])
    def getPath_to_Pellet(self, starting):
        self.i = 1
        return bfs(self.grid,starting, [o])
        # return

    def updateGrid(self):
             # updates grid if pellet is ate 
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        if self.grid[x][y] in [o, O]:
            self.grid[x][y] = e
            print(self.grid[x][y])


          
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
        self.i = 1        

    def getManhattanDist(self, start, end):
        return (abs(end[0] - start[0]) + abs(end[1] - start[1]))  
        
        
        
    # to talk via the serial port from rpi to mcu
    def talkToSerial(self, dir, x, y):
        to_Serial = str(dir) + "X" + "{0:0=2d}".format(x) + "Y" + "{0:0=2d}".format(y) # string format for instructions
        # ser = serial.Serial('/dev/ttyUSB0')  # open serial port
        # print(ser.name)         # check which port was really used
        print(to_Serial)
        # ser.write(to_Serial)     # write a string
        # ser.close()       # close port

    def gameRun(self):
    

        if self.path is None:
            print("new path")
            self.path = copy.deepcopy(self.getPath_to_powerPellet((self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])))
            print(self.path)
            # self.i=0
            # return

        if(self.path is not None):
            # print(self.path[self.i])
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
            red_ghost_state = 0 if self.state.red_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
            # print("red ghost: ", red_ghost_state)
            blue_ghost_state = 0 if self.state.blue_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
            pink_ghost_state = 0 if self.state.pink_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
            orange_ghost_state = 0 if self.state.orange_ghost.frightened_counter == 0 else 1 # 0 if the ghost is normal 1 if scared
            if(red_ghost_state or blue_ghost_state or pink_ghost_state or orange_ghost_state):
                # self.hunting = 1 
                self.getPath_To_Ghost((dir, x, y), self.path)
            
            if(self.i >= len(self.path)):
                # if self._check_if_valid_dir(self.cur_dir, x, y):
                    # self._move_if_valid_dir(self.cur_dir, x,y)
                self.path = None
            #     # return
            
            
        
        
    def gameTests(self):
        if(self.i<len(self.temp)):
            dir = self.temp[self.i][0]
            x = self.pacbot_pos[0]
            y = self.pacbot_pos[1]
            self._move_if_valid_dir(dir, x, y)
            self.i+=1
            self.talkToSerial(dir, x, y)

        
    # def _next_move(self, direction, x, y):
    #     if direction == right and grid[x + 1][y] not in [I, n]:
    #         return [x+1, y]
    #     elif direction == left and grid[x - 1][y] not in [I, n]:
    #         return [x-1, y]
    #     elif direction == up and grid[x][y + 1] not in [I, n]:
    #         return [x, y+1]
    #     elif direction == down and grid[x][y - 1] not in [I, n]:
    #         return [x, y-1]
    #     else:
    #         return [x,y]
            
           

        

def main():
    # ADDRESS = '192.168.1.89'
    # PORT = '11297'
    ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
    PORT = os.environ.get("BIND_PORT", 11297)
    module = HighLevel(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
