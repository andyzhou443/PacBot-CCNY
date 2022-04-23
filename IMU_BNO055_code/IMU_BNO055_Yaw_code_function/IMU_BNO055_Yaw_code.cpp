#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

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

  
    float get_angle(Adafruit_BNO055& myIMU){
        imu::Vector<3> mag = myIMU.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER); // Magnetometer vector

        // Magnetometer pitch yaw compensated value
        phiRad = phi / 360 * (2 * 3.14); // Converting phi to radian
        tethaRad = theta / 360 * (2 * 3.14); // Converting theta to radian

        Xm = mag.x() * cos( tethaRad) - mag.y() * sin(phiRad) * sin( tethaRad) + mag.z() * cos(phiRad) * sin( tethaRad);
        Ym = mag.y() * cos(phiRad) + mag.z() * sin(phiRad); // Compensated y magnetometer value


        // Calculating for yaw angle around of the x and y axis
        psi = -atan2(Ym, Xm) / (2 * 3.14) * 360;

        
        
    }

    void IMU_Calibration(Adafruit_BNO055& myIMU){ 
        // Calibrating IMU
        uint8_t system, gyro, accel, mg = 0;
        myIMU.getCalibration(&system, &gyro, &accel, &mg); // calibration 

        // Printing IMU BNO055 data

       // Calibratration data for accelomerator, gyroscope, magnetometer and system
       Serial.println("IMU BNO055 Calibration");
       Serial.print("Accel: ");
       Serial.print(accel);
       Serial.print(", ");
       Serial.print("Gyro: ");
       Serial.print(gyro);
       Serial.print(", ");
       Serial.print("Mg: ");
       Serial.print(mg);
       Serial.print(", ");
       Serial.print("System: ");
       Serial.print(system);
       Serial.println(" ");

       // Magnetometer yaw
       Serial.print("Magnetometer Psi yaw angle: ");
       Serial.println(psi);
       Serial.println(" ");


      delay(BNO055_SAMPLERATE_DELAY_MS);
      
    }

    
}