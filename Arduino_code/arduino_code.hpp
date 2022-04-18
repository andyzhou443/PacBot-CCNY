#include <Encoder.h>
#include <Arduino.h>

#ifndef H_PINS
#define H_PINS
#include "motor.hpp"

// // Global Encoder objects
extern Encoder* enc1;
extern Encoder* enc2;
extern Encoder* enc3;
extern Encoder* enc4;

// Global Motor objects
extern Motor* m1;
extern Motor* m2;
extern Motor* m3;
extern Motor* m4;


// Pin mappings
// Encoders
const int enc_1a = 4;
const int enc_1b = 5;
const int enc_2a = 6;
const int enc_2b = 7;
const int enc_3a = 9;
const int enc_3b = 10;
const int enc_4a = 20;
const int enc_4b = 21;

// Motors
const int motor_1a =  25;
const int motor_1b =  26;
const int motor_2a =  27;
const int motor_2b =  28;
const int motor_3a =  29;
const int motor_3b =  30;
const int motor_4a =  31;
const int motor_4b =  32;

//I2C:
const int mux_sda =  39;
const int mux_scl =  38;

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
