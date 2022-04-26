#include <Arduino.h>
#include <Encoder.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Wire.h>
#include <SparkFun_I2C_Mux_Arduino_Library.h>
#include <Adafruit_VL6180X.h>


#ifndef HEADRS
#define HEADRS

#include "encoder_funcs.hpp"
#include "motor.hpp"
#include "motor_coordinator.hpp"
#include "IMU_funcs.hpp"
#include "mux.hpp"
#include "TOF.hpp"

// Pin mappings
// Encoders
const int enc_1a = 33;
const int enc_1b = 34;
const int enc_2a = 35;
const int enc_2b = 36;
const int enc_3a = 37;
const int enc_3b = 38;
const int enc_4a = 39;
const int enc_4b = 40;

// Motors
const int motor_1a =  2;
const int motor_1b =  3;
const int motor_2a =  4;
const int motor_2b =  5;
const int motor_3a =  7;
const int motor_3b =  8;
const int motor_4a =  28;
const int motor_4b =  29;

//I2C:
const int mux_sda =  17;
const int mux_scl =  16;

// P-Code commands
const char* DIR_RIGHT = "0";
const char* DIR_LEFT = "1";
const char* DIR_UP = "2";
const char* DIR_DOWN = "3";


// PWM Resolution
const int ANALOG_RES = 8;

// Current coordinates
struct Coordinates
{
    int x; int y;
};
Coordinates coord;

// Wheel Radius
const int WHEEL_RADIUS = 8;

//Variable that keeps track of direction from high level
int target_direction = 0;

int movement_direction = 0;
int movement_speed = 0;
int movement_rotation = 0;

void setup();

void loop();

#endif // HEADRS