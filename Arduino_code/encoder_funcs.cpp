#include "encoder_funcs.hpp"
#include <Arduino.h>
namespace enc_f
{
    // Teensy has its own version of pi in its libraries.
    // const int PI = numbers::pi_v;
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
     * @param d Time taken to read encoder (ms)
     * @return float 
     */
    int get_speed_inch(Encoder& e, int d = 50)
    {
        long ticks = get_ticks(e,d);
        int in_speed = floor( ((float) ticks / d) * (float) (25/3) * 1.49606 * PI);
        return in_speed;
    }

    /**
     * @brief Report speed of encoder (in mm/s)
     * 
     * @param e Encoder object
     * @param d Time taken to read encoder (in ms)
     * @return float 
     */
    int get_speed_mm(Encoder& e, int d = 50)
    {
        long ticks = get_ticks(e,d);
        int mm_speed = floor( ((float) ticks / d) * (float) (25/3) * 38.0 * PI);
        return mm_speed;
    }

} // enc_f namespace
