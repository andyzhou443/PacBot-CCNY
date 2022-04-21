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
 * @param speed integer percentage for speed (-100 <-> +100)
 */
void Motor::set_speed(int speed)
{
    if (speed > 0) // CW
    {
        int result = floor( ((float) speed / 100) * 255);
        analogWrite(pinA, result);
        analogWrite(pinB,0);
        // Serial.println(result);
    }
    else if (speed < 0) // CCW
    {
        int result = floor(( (float) abs(speed) / 100) * 255);
        analogWrite(pinA,0);
        analogWrite(pinB, result);
        // Serial.println(result);
    }
    else
    {
        analogWrite(pinA,0);
        analogWrite(pinB,0);
    }
    return;
}
/**
 * @brief Stop running motor. Synonomous to "set_speed(0)"
 * 
 */
void Motor::halt()
{
    set_speed(0);
}