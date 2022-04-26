#include "TOF.hpp"
#include "mux.hpp"

namespace TOF_f
{
    int readDistance(Adafruit_VL6180X& sensor, int sel)
    {
        //mux.setPort(sel-1); //Connect to device at selx
        int result = 255;
        mux_h::tcaselect(sel - 1);
        result = sensor.readRange();
        int status = sensor.readRangeStatus();
        if(status != 0)
        {
            /*
            if  ((status >= VL6180X_ERROR_SYSERR_1) && (status <= VL6180X_ERROR_SYSERR_5)) {
                Serial.println("System error");
            }
            else if (status == VL6180X_ERROR_ECEFAIL) {
                Serial.println("ECE failure");
            }
            else if (status == VL6180X_ERROR_NOCONVERGE) {
                Serial.println("No convergence");
            }
            else if (status == VL6180X_ERROR_RANGEIGNORE) {
                Serial.println("Ignoring range");
            }
            else if (status == VL6180X_ERROR_SNR) {
                Serial.println("Signal/Noise error");
            }
            else if (status == VL6180X_ERROR_RAWUFLOW) {
                Serial.println("Raw reading underflow");
            }
            else if (status == VL6180X_ERROR_RAWOFLOW) {
                Serial.println("Raw reading overflow");
            }
            else if (status == VL6180X_ERROR_RANGEUFLOW) {
                Serial.println("Range reading underflow");
            }
            else if (status == VL6180X_ERROR_RANGEOFLOW) {
                Serial.println("Range reading overflow");
            }
            */
            //Serial.print("Resetting T"); Serial.print(sel); Serial.println("...");
            //sensor.begin(&Wire1);
        }
        return result;
    }
    
} // namespace TOF
