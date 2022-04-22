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
float dt;  // Chnage in time
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


// Use the time reference crystal that is on the board and not the crystal on the chip itself
myIMU.setExtCrystalUse(true);  
millisOld = millis(); // System clock 

}

void loop() {
  // put your main code here, to run repeatedly:

// Calibrating IMU
uint8_t system, gyro, accel, mag = 0;
myIMU.getCalibration(&system, &gyro, &accel, &mag); // calibration 

// Identify which sensor we're working with
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

// Calibratration data for accelomerator, gyroscope, magnetometer and system
Serial.println("IMU BNO055 Calibration");
Serial.print("Accel: ");
Serial.print(accel);
Serial.print(", ");
Serial.print("Gyro: ");
Serial.print(gyro);
Serial.print(", ");
Serial.print("Mag: ");
Serial.print(mag);
Serial.print(", ");
Serial.print("System: ");
Serial.print(system);
Serial.println(" ");

// Accelomerator x,y,z vectors
Serial.println("Acelomerator sensor initialization data");
Serial.print("x-axis: ");
Serial.print(acc.x()/9.8);
Serial.print(", ");
Serial.print("y-axis: ");
Serial.print(acc.y()/9.8);
Serial.print(", ");
Serial.print("z-axis: ");
Serial.print(acc.z()/9.8);
Serial.println(" ");

// Accelomerator pitch and roll roational angle around of the x and y axis compare to the z-axis
Serial.println("Accelomerator pitch and roll roational angle around of the x and y axis compare to the z-axis unfiltered");
Serial.print("Theta pitch x,z-axis: ");
Serial.print(thetaM);
Serial.print(", ");
Serial.print("Phi roll y,z-axis: ");
Serial.print(phiM);
Serial.println(" ");
Serial.println("Accelomerator pitch and roll rotational angle around of the x and y axis compare to the z-axis with low pass filter applied");
Serial.print("Theta pitch x,z-axis: ");
Serial.print(thetaFnew);
Serial.print(", ");
Serial.print("Phi roll y,z-axis: ");
Serial.println(phiFnew);


// Gyroscope pitch and roll rotational angle around of the y and x axis compare to the z-axis
Serial.println("Gyroscope pitch and roll roational angle around of the y and x axis compare to the z-axis");
Serial.print("y-axis: ");
Serial.print(thetaG);
Serial.print(", ");
Serial.print("x-axis: ");
Serial.println(phiG);

// Accelomerator and gyroscope sensor fusion pitch and roll 
Serial.println("Accelomerator and gyroscope sensor fusion pitch and roll rotational angle around of the y, x axis compare to the z-axis of the measured tetha value with the complementary filter applied");
Serial.print("y-axis: ");
Serial.print(theta);
Serial.print(", ");
Serial.print("x-axis: ");
Serial.println(phi);
Serial.println(" ");

/*
// Magnetometer in x,y,z
Serial.println("Magnetometer data");
Serial.print(mag.x());
Serial.print(",");
Serial.print(mag.y());
Serial.print(",");
Serial.println(mag.z());
*/


// Reassigning old values to new filter values 
phiFold = phiFnew;
thetaFold = thetaFnew;

delay(BNO055_SAMPLERATE_DELAY_MS);

}
