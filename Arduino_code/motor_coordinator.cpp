#include <math.h>
#include "motor_coordinator.hpp"
#include "TOF.hpp"
#include <Adafruit_VL6180X.h>

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

        angle += 315;

        while(angle < 0) angle += 360;
        while(angle >= 360) angle += -360;

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


    int centering_correction(Adafruit_VL6180X& sensor1, Adafruit_VL6180X& sensor2, Adafruit_VL6180X& sensor3, Adafruit_VL6180X& sensor4, int original_direction)
    {
        const int dist_threshold = 45;

        int new_direction = original_direction;
        bool tc_north = 0; //t1
        bool tc_west = 0; //t2
        bool tc_south = 0; //t3
        bool tc_east = 0; //t4

        tc_north = (TOF_f::readDistance(sensor1, 1) < dist_threshold);
        tc_west = (TOF_f::readDistance(sensor2, 2) < dist_threshold);
        tc_south = (TOF_f::readDistance(sensor3, 3) < dist_threshold);
        tc_east = (TOF_f::readDistance(sensor4, 4) < dist_threshold);

        
        /*
        Serial.print("Sensors: ");
        Serial.print(too_close_t1);
        Serial.print(", ");
        Serial.print(too_close_t2);
        Serial.print(", ");
        Serial.print(too_close_t3);
        Serial.print(", ");
        Serial.print(too_close_t4);
        Serial.println(" ");
        */
        
        //north: 0
        //west: 270
        //east: 90
        //south: 180

        //cardinal directions:
        if(tc_north == 1 && tc_west == 0 && tc_south == 0 && tc_east == 0)
        {
            new_direction = 180;
        }
        else if(tc_north == 0 && tc_west == 1 && tc_south == 0 && tc_east == 0)
        {
            new_direction = 90;
        }
        else if(tc_north == 0 && tc_west == 0 && tc_south == 1 && tc_east == 0)
        {
            new_direction = 0;
        }
        else if(tc_north == 0 && tc_west == 0 && tc_south == 0 && tc_east == 1)
        {
            new_direction = 270;
        }

        //angle:
        else if(tc_north == 1 && tc_west == 1 && tc_south == 0 && tc_east == 0)
        {
            new_direction = 135;
        }
        else if(tc_north == 0 && tc_west == 1 && tc_south == 1 && tc_east == 0)
        {
            new_direction = 45;
        }
        else if(tc_north == 0 && tc_west == 0 && tc_south == 1 && tc_east == 1)
        {
            new_direction = 315;
        }
        else if(tc_north == 1 && tc_west == 0 && tc_south == 0 && tc_east == 1)
        {
            new_direction = 225;
        }

        //3 sensors triggered:
        else if(tc_north == 0 && tc_west == 1 && tc_south == 1 && tc_east == 1)
        {
            new_direction = 0;
        }
        else if(tc_north == 1 && tc_west == 0 && tc_south == 1 && tc_east == 1)
        {
            new_direction = 270;
        }
        else if(tc_north == 1 && tc_west == 1 && tc_south == 0 && tc_east == 1)
        {
            new_direction = 180;
        }
        else if(tc_north == 1 && tc_west == 1 && tc_south == 1 && tc_east == 0)
        {
            new_direction = 90;
        }

        return new_direction;
        
    }


    void orientation_correction(){}

}