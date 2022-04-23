#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

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

// Create IMU sensor object to interract with the IMU
Adafruit_BNO055 myIMU = Adafruit_BNO055(); 

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
myIMU.begin();
delay(1000);


// Use the time reference crystal that is on the board and not the crystal on the chip itself
myIMU.setExtCrystalUse(true);  
millisOld = millis(); // System clock 

}

void loop() {
  // put your main code here, to run repeatedly:

// Calibrating IMU
uint8_t system, gyro, accel, mg = 0;
myIMU.getCalibration(&system, &gyro, &accel, &mg); // calibration 

// Identify which sensor we're working with
// Vector with 3 components
imu::Vector<3> mag = myIMU.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER); // Magnetometer vector


// Magnetometer pitch yaw compensated value
phiRad = phi / 360 * (2 * 3.14); // Converting phi to radian
tethaRad = theta / 360 * (2 * 3.14); // Converting theta to radian

Xm = mag.x() * cos( tethaRad) - mag.y() * sin(phiRad) * sin( tethaRad) + mag.z() * cos(phiRad) * sin( tethaRad);
Ym = mag.y() * cos(phiRad) + mag.z() * sin(phiRad); // Compensated y magnetometer value


// Calculating for yaw angle around of the x and y axis
psi = -atan2(Ym, Xm) / (2 * 3.14) * 360;


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
