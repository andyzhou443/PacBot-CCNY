#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Wire.h> //this we may need but im not sure yet, it allows communication with I2C device

int get_angle(Adafruit_BNO055 IMU){
    Adafruit_BNO055 IMU = Adafruit_BNO055(); 
    imu::Vector<3> euler = IMU.getVector(Adafruit_BNO055::VECTOR_EULER); // degrees
    int xRotation = eurler.z() //returns rotation of the robot

    return xRotation;
}

void IMU_Calibration(Adafruit_BNO055 IMU){ 
    Adafruit_BNO055 IMU = Adafruit_BNO055(); 
    int system, gyro = 0;
    IMU.getCalibration(&system, &gyro); // gives value from 0 to 3. Higher the more callibrated
}
