from cmath import pi, tan
from motor import Motor
import motor_drive

def set_angle(self, m1: Motor, m2: Motor, m3: Motor, m4: Motor,
    speed: float, angle: float, rotation_offset: int):
    
    # Normalize angle value between 0 and 359
    angle = angle + 315
    while(angle < 0):
        angle = angle + 360
    while (angle >= 360):
        angle = angle - 360
    

    # Determine angle offset
    cw_offset = 0
    ccw_offset = 0

    if(rotation_offset > 0):
        ccw_offset = rotation_offset
    elif (rotation_offset < 0):
        cw_offset = abs(rotation_offset)
    
    # Actual coordination
    if (angle >= 0 and angle < 45):
        m1.set_speed(-1 * speed + ccw_offset)
        m2.set_speed(speed * tan(angle * pi / 180) - cw_offset)
        m3.set_speed(speed - cw_offset)
        m4.set_speed(-1 * speed * tan(angle * pi / 180) + ccw_offset)

    elif (angle >= 45 and angle < 90):
        m1.set_speed(-1 * speed * tan((90 - angle) * pi / 180) + ccw_offset)
        m2.set_speed(speed - cw_offset)
        m3.set_speed(speed * tan((90 - angle) * pi / 180) - cw_offset)
        m4.set_speed(-1 * speed + ccw_offset)

    elif (angle >= 90 and angle < 135):
        m1.set_speed(speed * tan((angle - 90) * pi / 180) - cw_offset)
        m2.set_speed(speed - cw_offset)
        m3.set_speed(-1 * speed * tan((angle - 90) * pi / 180) + ccw_offset)
        m4.set_speed(-1 * speed + ccw_offset)

    elif (angle >= 135 and angle < 180):
        m1.set_speed(speed - cw_offset)
        m2.set_speed(speed * tan((180 - angle) * pi / 180) - cw_offset)
        m3.set_speed(-1 * speed + ccw_offset)
        m4.set_speed(-1 * speed * tan((180 - angle) * pi / 180) + ccw_offset)

    elif (angle >= 180 and angle < 225):
        m1.set_speed(speed - cw_offset)
        m2.set_speed(-1 * speed * tan((angle - 180) * pi / 180) + ccw_offset)
        m3.set_speed(-1 * speed + ccw_offset)
        m4.set_speed(speed * tan((angle - 180) * pi / 180) - cw_offset)

    elif (angle >= 225 and angle < 270):
        m1.set_speed(speed * tan((270 - angle) * pi / 180) - cw_offset)
        m2.set_speed(-1 * speed + ccw_offset)
        m3.set_speed(-1 * speed * tan((270 - angle) * pi / 180) + ccw_offset)
        m4.set_speed(speed - cw_offset)

    elif (angle >= 270 and angle < 315):
        m1.set_speed(-1 * speed * tan((angle - 270) * pi / 180) + ccw_offset)
        m2.set_speed(-1 * speed + ccw_offset)
        m3.set_speed(speed * tan((angle - 270) * pi / 180) - cw_offset)
        m4.set_speed(speed - cw_offset)
    
    elif (angle >= 315 and angle <= 360)
        m1.set_speed(-1 * speed + ccw_offset)
        m2.set_speed(-1 * speed * tan((360 - angle) * pi / 180) + ccw_offset)
        m3.set_speed(speed - cw_offset)
        m4.set_speed(speed * tan((360 - angle) * pi / 180) - cw_offset)
    else:
        pass

def centering_correction(self,original_direction: int) -> int:
    pass

def orientation_correction():
    pass
