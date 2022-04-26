 #include <Adafruit_Sensor.h>
 #include <Adafruit_BNO055.h>

namespace IMU_f
{
    int get_angle(Adafruit_BNO055& IMU){
        imu::Vector<3> euler = IMU.getVector(Adafruit_BNO055::VECTOR_EULER);  // degrees
        int xRotation = euler.z(); // returns rotation of the robot

        return xRotation;
    }

    void IMU_Calibration(Adafruit_BNO055& IMU){ 
        uint8_t system, gyro, accel, mag = 0;
        IMU.getCalibration(&system, &gyro, &accel, &mag); // gives value from 0 to 3. Higher the more callibrated
    }
}