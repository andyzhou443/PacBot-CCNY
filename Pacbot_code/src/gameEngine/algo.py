#!/usr/bin/env python3

import os, sys, curses
import robomodules as rm
from messages import *
from pacbot.variables import *
from pacbot.grid import *
from collections import deque

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
                self.dfs()
        pos_buf = PacmanState.AgentState()
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
        return False
    



    def dfs(self):
        # stack = []
        # self.queue.append([self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]])
        print(self.queue)
        current = self.queue.popleft()
        if(self._check_if_valid_dir(current[0], current[1], current[2])):
            self._move_if_valid_dir(current[0], current[1], current[2])
            current[0] = self.cur_dir
            current[1] = self.pacbot_pos[0]
            current[2] = self.pacbot_pos[1]
            self.queue.append([current[0], current[1], current[2]])
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
            
           

        




def main():
    module = InputModule(ADDRESS, PORT)
    curses.wrapper(lambda scr: module.run())

if __name__ == "__main__":
    main()
