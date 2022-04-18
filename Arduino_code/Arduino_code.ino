#include "arduino_code.hpp"
#include "motor.hpp"

void setup() {
  // put your setup code here, to run once:

  // Setup serial port
  COM serial(9600);
  
  // Setup pin directions
  pinMode(enc_1a, INPUT); pinMode(enc_1b, INPUT);
  pinMode(enc_2a, INPUT); pinMode(enc_2b, INPUT);
  pinMode(enc_3a, INPUT); pinMode(enc_3b, INPUT); 
  pinMode(enc_4a, INPUT); pinMode(enc_4b, INPUT);

  pinMode(motor_1a,OUTPUT); pinMode(motor_1b,OUTPUT);
  pinMode(motor_2a,OUTPUT); pinMode(motor_2b,OUTPUT);
  pinMode(motor_3a,OUTPUT); pinMode(motor_3b,OUTPUT);
  pinMode(motor_4a,OUTPUT); pinMode(motor_4b,OUTPUT);
  
  // Setup interfacing objects
  Motor m1(motor_1a,motor_1b);
  Motor m2(motor_2a,motor_2b);
  Motor m3(motor_3a,motor_3b);
  Motor m4(motor_4a,motor_4b);


  
    Serial.write("Teensy OK\n");
}

void loop() {
  // put your main code here, to run repeatedly:

  //  Read serial
  char command_buffer[15];
    int buffer_size = 0;
    buffer_size = 
        Serial.readBytesUntil('\n',command_buffer,15);

    //TODO: Parse Code

    // Echo Input
    if (buffer_size > 0)
  {
        Serial.write(command_buffer,buffer_size);
        Serial.write('\n');
    }
    command_buffer[++i] = '\0';
    
    // consume newline
    if (Serial.peek() == '\n' || Serial.peek() == '\r')
      Serial.read();
    
    Serial.println(command_buffer);    
    
    // Parse Code

    // Movement commands
    if (strcmp(command_buffer, DIR_DOWN) == 0)
    {

    }
    else if (strcmp(command_buffer, DIR_LEFT) == 0)
    {
    }
    else if (strcmp(command_buffer, DIR_UP) == 0)
    {

    }
    else if (strcmp(command_buffer,DIR_DOWN) == 0)
    {

    }

    // Test commands
    else if (strcmp(command_buffer,"T1") == 0)
    {
      Serial.println("Motor TEST");
    }
    else if (strcmp(command_buffer,"T2") == 0)
    {
      Serial.println("Encoder TEST");
    }
    else if (strcmp(command_buffer,"T3") == 0)
    {
      Serial.println("ToF TEST");
    }
    else if(strcmp(command_buffer,"T4") == 0)
    {
      Serial.println("IMU TEST");
    }
  }
}
