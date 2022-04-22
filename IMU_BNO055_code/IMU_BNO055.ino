#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

// Accelomerator variables 
float thetaM;
float phiM;
float thetaFold = 0;
float thetaFnew;
float phiFold = 0;
float phiFnew;

// Gyroscope variables
float thetaG = 0; 
float phiG = 0; 
float dt; // Chnage in time  
unsigned long millisOld; // System clock last time around 

// Accelomerator + Gyroscope sensor fusion variables
float theta;
float phi;

 
// Telling the IMU how fast to run
#define BNO055_SAMPLERATE_DELAY_MS (100) // Sample rate

// Create IMU sensor object to interract with the IMU
Adafruit_BNO055 myIMU = Adafruit_BNO055(); 

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
myIMU.begin();
delay(1000);

// Temaperature measurements

// Talking to IMU and telling it to get the temparature and put it in a variable named temp
//int8_t temp = myIMU.getTemp(); // Store numbers from -120 to 120 
//Serial.println(temp); 

myIMU.setExtCrystalUse(true); // Use the time reference crystal that is on the board and not the crystal on the chip itself 
millisOld = millis(); // System clock 

}

void loop() {
  // put your main code here, to run repeatedly:

// Calibrating IMU
uint8_t system, gyro, accel, mag = 0;
myIMU.getCalibration(&system, &gyro, &accel, &mag); // calibration 

// Identify which sensor we're working by turning the accelomerator and gyrocope on
// Vector with 3 components
imu::Vector<3> acc = myIMU.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER); // Accelomerator vector
imu::Vector<3> gyr = myIMU.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE); // Gyroscope vector
//imu::Vector<3> mag = myIMU.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER); // Magnetometer vector

// Accelemerator pitch and roll
// Calculating for pitch rotational angle around of the x-axis compare to the z-axis of the measured tetha value
thetaM = -atan2(acc.x()/9.8,acc.z()/9.8)/2/3.141592654*360;  // Calculating the angle theta in degrees

// Calculating for roll rotational angle around of the y-axis compare to the z-axis of the measured phi value
phiM = -atan2(acc.y()/9.8,acc.z()/9.8)/2/3.141592654*360;  // Calculating the angle phi in degrees

// Calculating phi pitch rotational angle around of the x-axis compare to the z-axis with the low pass filter applied
phiFnew = .95 * phiFold + .05 * phiM;

// Calculating theta roll rotational angle around of the y-axis compare to the z-axis  with the low pass filter applied
thetaFnew = .95 * thetaFold + .05 * thetaM;


// Gyroscope pitch and roll
dt = (millis() - millisOld)/1000.; // Elapsed time between subsequent measurements
millisOld = millis(); // Current system clock time 

// Calculating for pitch rotational angle around of the y-axis compare to the z-axis of the measured tetha value
thetaG = thetaG + gyr.y() * dt;

// Calculating for roll rotational angle around of the x-axis compare to the z-axis of the measured tetha value
phiG = phiG - gyr.x() * dt;


// Accelomerator and gyroscope sensor fusion pitch and roll 
// Calculating for pitch rotational angle around of the y-axis compare to the z-axis of the measured tetha value with the complementary filter applied
theta = (theta + gyr.y() * dt) * .95 + thetaM * .05; 

// Calculating for roll rotational angle around of the x-axis compare to the z-axis of the measured tetha value with the complementary filter applied
phi = (phi - gyr.x() * dt) * .95 + phiM * .05;

// Printing IMU BNO055 data
  
// Accelomerator x,y,z vectors
Serial.print(acc.x()/9.8);
Serial.print(",");
Serial.print(acc.y()/9.8);
Serial.print(",");
Serial.print(acc.z()/9.8);
Serial.print(",");

// Calibratration data for accelomerator, gyroscope, magnetometer and system
Serial.print(accel);
Serial.print(",");
Serial.print(gyro);
Serial.print(",");
Serial.print(mag);
Serial.print(",");
Serial.print(system);
Serial.print(",");
Serial.print(thetaM);
Serial.print(",");
Serial.print(phiM);
Serial.print(",");
Serial.print(thetaFnew);
Serial.print(",");
Serial.print(phiFnew);

// Reassigning old values to new filter values 
phiFold = phiFnew;
thetaFold = thetaFnew;


// Gyroscope x,y,z vectors
Serial.print(",");
Serial.print(thetaG);
Serial.print(",");
Serial.print(phiG);

// Accelomerator and gyroscope sensor fusion pitch and roll 
Serial.print(",");
Serial.print(theta);
Serial.print(",");
Serial.println(phi);
/*
// Magnetometer in x,y,z
Serial.print(mag.x());
Serial.print(",");
Serial.print(mag.y());
Serial.print(",");
Serial.println(mag.z());
*/


delay(BNO055_SAMPLERATE_DELAY_MS);

}
