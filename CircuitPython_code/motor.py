import pwmio
import board
import typing
import uasyncio

from math import floor

class Motor():

    pinA = None
    pinB = None

    def __init__(self, pinA:pwmio, pinB:pwmio):
        self.pinA = pinA
        self.pinB = pinB
    
    def set_speed(self, speed: int):
        if speed > 0: # CCW
            result = floor((speed / 100) * 65535)
            self.pinA.duty_cycle = result
            self.pinB.duty_cycle = 0
        elif speed < 0:
            result = floor((abs(speed) / 100) * 65535)
            self.pinA.duty_cycle = 0
            self.pinB.duty_cycle = result
        else:
            self.pinA.duty_cycle = 0
            self.pinB.duty_cycle = 0
        
        def halt(self):
            self.set_speed(0)
            