#include "encoder_funcs.hpp"
#include <Arduino.h>
#include <numbers>
namespace enc_f
{
    const int PI = numbers::pi_v;
    /**
     * @brief Get ticks elapsed from an encoder read
     * 
     * @param e Encoder object to read
     * @param d Time to read encoder
     * @return long number of ticks per CPU cycle
     */
    long get_ticks(Encoder& e, int d = 0)
    {
        e.write(0);
        delay(d);
        return e.read();
    }

    /**
     * @brief Report speed of encoder (in in/s)
     * 
     * @param e Encoder object to report
     * @param d Time to read encoder
     * @return float 
     */
    int get_speed_inch(Encoder& e, int d = 50)
    {
        long ticks = get_ticks(e,d);
        int speed = floor( ((float) ticks / delay) * (float) (25/3) * 1.49606 * PI);
        return speed;
    }

    /**
     * @brief Report speed of encoder (in mm/s)
     * 
     * @param e Encoder object
     * @param d Time to read encoder
     * @return float 
     */
    int get_speed_mm(Encoder& e, int d = 50)
    {
        long ticks = get_ticks(e,d);
        int speed = floor( ((float) ticks / delay) * (float) (25/3) * 38.0 * PI);
        return speed;
    }

} // enc_f namespace
