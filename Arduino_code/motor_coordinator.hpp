#ifndef M_COORD
#define M_COORD

#include "motor.hpp"
namespace m_coord
{
    // extern Motor m1;
    // extern Motor m2;
    // extern Motor m3;
    // extern Motor m4;    
    void set_angle(Motor& m1, Motor& m2, Motor& m3, Motor& m4,
        float speed, float angle, int rotation_offset);
    void distanceCorrection();
    void angleCorrection();
} // namespace m_coord

#endif //M_COORD