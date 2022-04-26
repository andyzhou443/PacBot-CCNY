 #include <Adafruit_Sensor.h>
 #include <Adafruit_BNO055.h>

 #ifndef IMU_H
 #define IMU_H

 namespace IMU_f
 {
    int get_angle(Adafruit_BNO055& sensor);
    void IMU_Calibration(Adafruit_BNO055& sensor);
 } // namespace imu

 #endif // IMU_H
 