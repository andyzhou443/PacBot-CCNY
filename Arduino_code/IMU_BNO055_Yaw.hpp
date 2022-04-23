#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

 #ifndef IMU_H
 #define IMU_H

 namespace IMU_f
 {

  unsigned long millisOld; // System clock last time around 

  // Accelerometer + Gyroscope sensor fusion variables
  float theta;
  float phi;

  // Magnetometer varibales 
  float Xm;
  float Ym;
  float psi; 

  // Compensated magnometer value
  float tethaRad;
  float phiRad;

  // Telling the IMU how fast to run
  #define BNO055_SAMPLERATE_DELAY_MS (100) // Sample rate
 
    float get_angle(Adafruit_BNO055& myIMU);
    void IMU_Calibration(Adafruit_BNO055& myIMU);
 } // namespace imu

 #endif // IMU_H
 