#include "encoder_funcs.hpp"
#include <Arduino.h>
namespace enc_f
{
    /**
     * @brief Get ticks elapsed from an encoder read
     * 
     * @param e Encoder object to read
     * @param d Time to read encoder
     * @return long number of ticks per CPU cycle
     */
    long get_ticks(Encoder& e,float d = 0.0)
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
    double get_speed_inch(Encoder& e, float d = 0.0)
    {
        long ticks = get_ticks(e,d);
        return 0; // TODO: Figure out the conversion formula
    }

    /**
     * @brief Report speed of encoder (in mm/s)
     * 
     * @param e Encoder object
     * @param d Time to read encoder
     * @return float 
     */
    double get_speed_mm(Encoder& e, float d = 0.0)
    {
        long ticks = get_ticks(e,d);
        return 0; // TODO: Figure out conversion formula
    }

} // enc_f namespace
