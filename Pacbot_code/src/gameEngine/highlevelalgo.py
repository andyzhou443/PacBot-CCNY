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
from helperfunctions import *
import copy
import serial

DANGER = 8
PELLET_WEIGHT = 0.65
POWER_PELLET_WEIGHT = 0.15
GHOST_WEIGHT = 0.30
FRIGHTENED_GHOST_WEIGHT = GHOST_WEIGHT**2


# while(i<len(path)):
#     print(path[i][-1])
#     i+=1





SPEED = 1.0
FREQUENCY = SPEED * game_frequency 



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
        self.grid = copy.deepcopy(grid)
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
        if self.state.mode == PacmanState.PAUSED:
            stop_signal = "S".encode() # string format for instructions
            
            # ser = serial.Serial('/dev/ttyUSB0')  # open serial port
            # print(ser.name)         # check which port was really used
            print(stop_signal)
            # ser.write(to_Serial)     # write a string
            # ser.close()       # close port
        pos_buf = PacmanState.AgentState()
        # fil.close()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)


    def getPath_to_powerPellet(self, starting):
        return bfs(self.grid,starting, [O])


    def getPath_to_Pellet(self, starting):
        return bfs(self.grid,starting, [o])


    def get_move(self):
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        #current position, left, right, down, up
        targets = [(x,y), (x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        heuristics = []
        for target in targets: 
            if(self.grid[target[0]][target[1]] in [I, n]):
                heuristics.append(None)
                continue
            else: 
                dir = self.get_direction(target,(x,y))

                pellet_path = self.getPath_to_Pellet((dir, target[0], target[1]))
                pellet_dist = len(pellet_path)
                pellet_heuristic = pellet_dist * PELLET_WEIGHT
                print(f"pellet path: {pellet_path}")
                
                power_path = self.getPath_to_powerPellet((dir, target[0], target[1]))
                # if there's no more power pellets to eat --> power_path = None
                if power_path is None:
                    power_dist = 0
                else:
                    power_dist = len(power_path)
                
                power_heuristic = power_dist * POWER_PELLET_WEIGHT

                         
            ghosts_info = self.get_ghostsInfo(target)
            # ghost_dist = self.closest_ghost_dist(ghosts_info)
            print(f"info {ghosts_info}")
            ghost_heuristic = 0
            frightened_num = 0
            ghostNear_num = 0
            for ghost_dist, counter in ghosts_info.values():
                if counter <= 1: 
                    if ghost_dist < DANGER+3:
                        ghostNear_num += 1
                        #ghosts are not frightened
                        ghost_heuristic += pow(((DANGER+3) - ghost_dist), 2) * GHOST_WEIGHT    
                else:
                    frightened_num += 1
                    if ghost_dist < DANGER:
                        ghostNear_num += 1
                        #ghhost_dir here
                        ghost_heuristic += pow(((DANGER) - ghost_dist), 2) * -1 * FRIGHTENED_GHOST_WEIGHT
            
            
            if frightened_num > 0:
                power_heuristic = 150 * frightened_num

            # print("heuristic",pellet_heuristic+power_heuristic+ghost_heuristic)
            heuristics.append(pellet_heuristic+power_heuristic+ghost_heuristic)

        print(heuristics)
        min_heuristic = float('inf')
        min_target = (0,0)
        for i in range(len(heuristics)):
            if heuristics[i]!=None and (heuristics[i]<= min_heuristic):
                min_heuristic = heuristics[i]
                min_target = targets[i]
        print("min target:",min_target)
        return min_target 


    def get_ghostsInfo(self, location):
        keys = {}
        x = location[0]
        y = location[1]
        #There's two ghostcolor_dist for each ghost, one uses manhattan distance while the other uses path length

        red_path = bfs(self.grid, (self.cur_dir, x, y), (self.state.red_ghost.x, self.state.red_ghost.y))
        red_dist = len(red_path) if red_path is not None else 0                                 #distance measured via path length (number of steps)
        red_ghost_state = 0 if self.state.red_ghost.frightened_counter == 0 else 1
        keys[red] = [red_dist, self.state.red_ghost.frightened_counter]
        
        pink_path = bfs(self.grid, (self.cur_dir, x, y), (self.state.pink_ghost.x, self.state.pink_ghost.y))
        pink_dist = len(pink_path) if pink_path is not None else 0
        pink_ghost_state = 0 if self.state.pink_ghost.frightened_counter == 0 else 1
        keys[pink] = [pink_dist, self.state.pink_ghost.frightened_counter]
        
        blue_path = bfs(self.grid, (self.cur_dir, x, y), (self.state.blue_ghost.x, self.state.blue_ghost.y))
        blue_dist = len(blue_path) if blue_path is not None else 0  
        blue_ghost_state = 0 if self.state.blue_ghost.frightened_counter == 0 else 1
        keys[blue] = [blue_dist, self.state.blue_ghost.frightened_counter]
        
        orange_path = bfs(self.grid, (self.cur_dir, x, y), (self.state.orange_ghost.x, self.state.orange_ghost.y))
        orange_dist  = len(orange_path) if orange_path is not None else 0  
        orange_ghost_state = 0 if self.state.orange_ghost.frightened_counter == 0 else 1
        keys[orange] = [orange_dist, self.state.orange_ghost.frightened_counter]
        

        return keys
        

    def closest_ghost_dist(self, info):
    #returns ghost distance thats closest to pacman
        min_dist = 9999
        for ghost in info.values():
            if ghost[0] < min_dist:
                min_dist = ghost[0]
        
        return min_dist

    def updateGrid(self):
             # updates grid if pellet is ate 
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        if self.grid[x][y] in [o, O]:
            self.grid[x][y] = e
            # print(self.grid[x][y])

    # to talk via the serial port from rpi to mcu
    def talkToSerial(self, dir, x, y):
        to_Serial = str(dir) + "X" + "{0:0=2d}".format(x) + "Y" + "{0:0=2d}".format(y) # string format for instructions
        to_Serial = to_Serial.encode()
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
        direction = self.cur_dir 
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
        x = self.pacbot_pos[0]
        y = self.pacbot_pos[1]
        if(self.cherry and self.ManhattanDist((x,y), (13,13))<float("11")):
            path = copy.deepcopy(bfs(self.grid, (self.cur_dir,x,y), (13,13)))
            next_loc = (path[0][1],path[0][2])
            dir = self.get_direction(next_loc, (x,y))
        else:
            next_loc = self.get_move()
            dir = self.get_direction(next_loc,(x,y))
        
        if (x,y) != next_loc:
            self.talkToSerial(dir, x, y)
            self._move_if_valid_dir(dir , x, y)
        
        self.updateGrid()
        
def main():
    # ADDRESS = '192.168.1.89'
    # PORT = '11297'
    ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
    PORT = os.environ.get("BIND_PORT", 11297)
    module = HighLevel(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
