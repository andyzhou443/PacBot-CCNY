#include "motor.hpp"
#include <cmath>

/**
 * @brief Construct a new Motor:: Motor object
 * 
 * @param p1 M1 pin
 * @param p2 M2 pin
 */
Motor::Motor(int p1, int p2)
{
    pinA = p1;
    pinB = p2;
}

/**
 * @brief Drive motor at a certain speed
 * 
 * @param speed integer percentage for speed (-100-+100)
 */
void Motor::set_speed(int speed)
{
    if (speed > 0) // CW
    {
        analogWrite(pinA, speed / 100 * pow(2,ANALOG_RES));
        analogWrite(pinB,0);
    }
    else if (speed < 0) // CCW
    {
        analogWrite(pinA,0);
        analogWrite(pinB, speed / 100 * pow(2,ANALOG_RES));
    }
    else
    {
        analogWrite(pinA,0);
        analogWrite(pinB,0);
    }
    return;
}

void Motor::halt()
{
    set_speed(0);
}