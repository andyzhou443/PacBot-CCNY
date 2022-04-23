import board

# Motor pin definitions
pin_motor1a = board.D2
pin_motor1b = board.D3
pin_motor2a = board.D4
pin_motor2b = board.D5
pin_motor3a = board.D7
pin_motor3b = board.D8
pin_motor4a = board.D28
pin_motor4b = board.D29

# Mux Pins
pin_mux_sda = 17
pin_mux_scl = 16

# P-Code Commands
DIR_RIGHT = 0
DIR_LEFT = 1
DIR_UP = 2
DIR_DOWN = 3

# Wheel Radius
WHEEL_RADIUS = 38

# High level tracking constants
target_direction = 0
movement_direction = 0
movement_speed = 0
movement_rotation = 0