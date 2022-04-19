#include<Arduino.h>
#include<Encoder.h>

#ifndef ENC_FUNC
#define ENC_FUNC
namespace enc_f
{
    // Wheel radius (in mm)
    extern const int WHEEL_RADIUS;

    long get_ticks(Encoder& e,float d);
    double get_speed_inch(Encoder& e, float d);
    double get_speed_mm(Encoder& e, float d);
} // enc_f namespace

#endif //ENC_FUNC