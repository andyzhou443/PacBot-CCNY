#include <Encoder.h>
#include <Arduino.h>

#ifndef H_PINS
#define H_PINS
#include "motor.hpp"


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

#endif // H_PINS

void setup();

void loop();
