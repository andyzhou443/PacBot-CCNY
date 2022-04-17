#include <Arduino.h>
#ifndef MOTOR_H
#define MOTOR_H
// PWM Resolution
extern const int ANALOG_RES;

class Motor
{
    private:
    int pinA, pinB;

    public:
    Motor(int p1, int p2);
    void set_speed(int speed);
    void halt();

};
#endif // MOTOR_H