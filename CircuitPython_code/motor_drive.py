import board
import digitalio
import time
import pwmio

#motor1 connected to pin15
def drive_up(percent,blocks):
    while True:
        pwm_nmotor = pwmio.PWMOut(board.IO15,frequency = percent)
        time.sleep()

#motor2
def drive_down(percent):
    motor2 = digitalio.DigitalInOut(board.IO16)
    motor2.direction = digitalio.Direction.OUTPUT
    while True:
        print("move down")

#motor3
def drive_left(percent):
    motor3 = digitalio.DigitalInOut(board.IO17)
    motor3.direction = digitalio.Direction.OUTPUT
    while True:
        print("move left")

#motor4
def drive_right(percent):
    motor4 = digitalio.DigitalInOut(board.IO18)
    motor4.direction = digitalio.Direction.OUTPUT
    while True:
        print("move right")