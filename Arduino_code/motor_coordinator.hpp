#ifndef M_COORD
#define M_COORD

#include "motor.hpp"
#include <Adafruit_VL6180X.h>

namespace m_coord
{
    // extern Motor m1;
    // extern Motor m2;
    // extern Motor m3;
    // extern Motor m4;    
    void set_angle(Motor& m1, Motor& m2, Motor& m3, Motor& m4,
        float speed, float angle, int rotation_offset);
    int centering_correction(Adafruit_VL6180X& sensor1, Adafruit_VL6180X& sensor2, Adafruit_VL6180X& sensor3, Adafruit_VL6180X& sensor4, int original_direction);
    int orientation_correction();
} // namespace m_coord

#endif //M_COORD