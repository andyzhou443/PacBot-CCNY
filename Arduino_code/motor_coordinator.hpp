#ifndef M_COORD
#define M_COORD

#include "motor.hpp"
namespace m_coord
{
    extern Motor* m1;
    extern Motor* m2;
    extern Motor* m3;
    extern Motor* m4;
    void move(float distance, float angle);
    void distanceCorrection();
    void angleCorrection();
} // namespace m_coord

#endif //M_COORD