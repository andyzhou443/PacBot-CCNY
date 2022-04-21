#include <math.h>
#include "motor_coordinator.hpp"


namespace m_coord
{
    void move(float distance, float angle)
    {
        //functions takes in angle and distance and give the rotation to each motor
        //angle is 0 to 360
        if (angle >= 0 && angle < 45)
        {
            m1->set_speed(-100);
            m2->set_speed(100 * tan(angle));
            m3->set_speed(100);
            m4->set_speed(-100 * tan(angle));
        }
        else if (angle >= 45 && angle < 90)
        {
          //stuff
        }
        else if (angle >= 90 && angle < 135)
        {
          //stuff
        }
        else if (angle >= 135 && angle < 180)
        {
          //stuff
        }
        else if (angle >= 180 && angle < 225)
        {
          //stuff
        }
        else if (angle >= 225 && angle < 270)
        {
          //stuff
        }
        else if (angle >= 270 && angle < 315)
        {
          //stuff
        }
        else
        {
          //stuff
        }

    }


    void distanceCorrection(){}


    void angleCorrection(){}

}