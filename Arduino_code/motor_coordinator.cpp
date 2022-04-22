#include <math.h>
#include "motor_coordinator.hpp"

namespace m_coord
{
    /**
     * @brief Drives robot at a certain angle
     * 
     * @param speed Speed of robot (0-100)
     * @param angle Angle robot moves (0-360)
     * 
     */
    void set_angle(Motor& m1, Motor& m2, Motor& m3, Motor& m4, 
        float speed = 100, float angle = 0, int rotation_offset = 0)
    {
        //functions takes in angle and distance and give the rotation to each motor
        //angle is 0 to 360
        //For rotation offset: Positive is counter-clockwise, negative is clockwise
        //For clockwise rotation, slow down the positive speeds, for ccw, slow down the negative speeds
        int cw_offset = 0;
        int ccw_offset = 0;

        if(rotation_offset > 0)
        {
          ccw_offset = rotation_offset;
        }
        else if(rotation_offset < 0)
        {
          cw_offset = -1 * rotation_offset;
        }

        if (angle >= 0 && angle < 45)
        {
            m1.set_speed(-1 * speed + ccw_offset);
            m2.set_speed(speed * tan(angle* PI / 180) - cw_offset);
            m3.set_speed(speed - cw_offset);
            m4.set_speed(-1 * speed * tan(angle * PI / 180) + ccw_offset);
        }
        else if (angle >= 45 && angle < 90)
        {
            m1.set_speed(-1 * speed * tan((90 - angle) * PI / 180) + ccw_offset);
            m2.set_speed(speed - cw_offset);
            m3.set_speed(speed * tan((90 - angle) * PI / 180) - cw_offset);
            m4.set_speed(-1 * speed + ccw_offset);
        }
        else if (angle >= 90 && angle < 135)
        {
            m1.set_speed(speed * tan((angle - 90) * PI / 180) - cw_offset);
            m2.set_speed(speed - cw_offset);
            m3.set_speed(-1 * speed * tan((angle - 90) * PI / 180) + ccw_offset);
            m4.set_speed(-1 * speed + ccw_offset);
        }
        else if (angle >= 135 && angle < 180)
        {
            m1.set_speed(speed - cw_offset);
            m2.set_speed(speed * tan((180 - angle) * PI / 180) - cw_offset);
            m3.set_speed(-1 * speed + ccw_offset);
            m4.set_speed(-1 * speed * tan((180 - angle) * PI / 180) + ccw_offset);
        }
        else if (angle >= 180 && angle < 225)
        {
            m1.set_speed(speed - cw_offset);
            m2.set_speed(-1 * speed * tan((angle - 180) * PI / 180) + ccw_offset);
            m3.set_speed(-1 * speed + ccw_offset);
            m4.set_speed(speed * tan((angle - 180) * PI / 180) - cw_offset);
        }
        else if (angle >= 225 && angle < 270)
        {
            m1.set_speed(speed * tan((270 - angle) * PI / 180) - cw_offset);
            m2.set_speed(-1 * speed + ccw_offset);
            m3.set_speed(-1 * speed * tan((270 - angle) * PI / 180) + ccw_offset);
            m4.set_speed(speed - cw_offset);
        }
        else if (angle >= 270 && angle < 315)
        {
            m1.set_speed(-1 * speed * tan((angle - 270) * PI / 180) + ccw_offset);
            m2.set_speed(-1 * speed + ccw_offset);
            m3.set_speed(speed * tan((angle - 270) * PI / 180) - cw_offset);
            m4.set_speed(speed - cw_offset);
        }
        else if (angle >= 315 && angle <= 360)
        {
            m1.set_speed(-1 * speed + ccw_offset);
            m2.set_speed(-1 * speed * tan((360 - angle) * PI / 180) + ccw_offset);
            m3.set_speed(speed - cw_offset);
            m4.set_speed(speed * tan((360 - angle) * PI / 180) - cw_offset);
        }
        else return;

    }


    void distanceCorrection(){}


    void angleCorrection(){}

}