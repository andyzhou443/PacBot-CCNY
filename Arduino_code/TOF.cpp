#include "TOF.hpp"

namespace TOF_f
{
    float readDistance(QWIICMUX& mux, Adafruit_VL6180X& sensor, int sel)
    {
        mux.setPort(sel-1); //Connect to device at selx
        return 0.0;
    }
    
} // namespace TOF
