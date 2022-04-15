#ifndef PINS
#include "pins.h"
#define PINS
#endif

#include "motor.cpp"
// Pacbot code

void setup() {
  // put your setup code here, to run once:
  pinMode(enc_1a, INPUT); pinMode(enc_1b, INPUT);
  pinMode(enc_2a, INPUT); pinMode(enc_2b, INPUT);
  pinMode(enc_3a, INPUT); pinMode(enc_3b, INPUT); 
  pinMode(enc_4a, INPUT); pinMode(enc_4b, INPUT);

  pinMode(motor_1a,OUTPUT); pinMode(motor_1b,OUTPUT);
  pinMode(motor_2a,OUTPUT); pinMode(motor_2b,OUTPUT);
  pinMode(motor_3a,OUTPUT); pinMode(motor_3b,OUTPUT);
  pinMode(motor_4a,OUTPUT); pinMode(motor_4b,OUTPUT);
  Serial.begin(9600);
  Serial.println("OK");
  
}

void loop() {
    // put your main code here, to run repeatedly:
  //  Read serial
  int i = 0;
  char command_buffer[15];
  int temp_buffer;
  if (Serial.available() > 0)
  {
    i = 0;
    temp_buffer = Serial.read();
    while(temp_buffer != -1 && i < 15 && temp_buffer != '\n')
    {
      command_buffer[i++] = temp_buffer;
      temp_buffer = Serial.read();
    }
    command_buffer[++i] = '\0';
    
    // consume newline
    if (Serial.peek() == '\n' || Serial.peek() == '\r')
      Serial.read();
    
    Serial.println(command_buffer);    
    // Parse Code
    if (strcmp(command_buffer,"TE1") == 0)
    {
      Serial.println("Motor TEST");
    }
    else if (strcmp(command_buffer,"TE2") == 0)
    {
      Serial.println("Encoder TEST");
    }
    else if (strcmp(command_buffer,"TE3") == 0)
    {
      Serial.println("ToF TEST");
    }
    else if(strcmp(command_buffer,"TE4") == 0)
    {
      Serial.println("IMU TEST");
    }
  }
}