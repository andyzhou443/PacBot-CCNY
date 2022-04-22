#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

#ifndef IMU_H
#define IMU_H

namespace IMU_f
{
    int get_angle(Adafruit_BNO055 IMU);
    void IMU_Callibration(Adafruit_BNO055 IMU);
} 

#endif