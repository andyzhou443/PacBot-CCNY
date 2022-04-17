import pwmio
import board
import typing
import uasyncio

class Motor():
    
    pwm_obj = None
    pwm_freq = 90
    speed = None

    def __init__(pinA: board,pinB: board, encA: board, encB: board):
        raise NotImplementedError

    async def moveCCW(speed: int,time: int):
        raise NotImplementedError

    async def moveCW(speed: int,time: int):
        raise NotImplementedError

    async def ramp_pwm(speed: int,time: int):
        raise NotImplementedError

    async def get_speed() -> float:
        raise NotImplementedError
