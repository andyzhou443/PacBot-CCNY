#include "arduino_code.hpp"
#include "motor.hpp"

void setup() {
    // put your setup code here, to run once:

    // Setup serial port
    Serial.begin(115200);

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


    // Setup global coordinate object
    coord = {13,7};


    while (!Serial);
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

    // Parse P-Code
    {
        if(isdigit(command_buffer[0]))
        {
            // Movement code
            if(strcmp(command_buffer[0],"0") == 0)
                Serial.write("0 MOVE FORWARD\n");
            else if(strcmp(command_buffer[0],"1") == 0)
                Serial.write("1 MOVE BACKWARD\n");
            else if(strcmp(command_buffer[0],"2") == 0)
                Serial.write("2 MOVE LEFT\n");
            else if(strcmp(command_buffer[0],"3") == 0)
                Serial.write("3 MOVE RIGHT\n");
            else
                Serial.write("Invalid Movement Command\n");
            

            char temp_x[2];
            char temp_y[2];
            strncpy(temp_x, command_buffer+2, 2);
            strncpy(temp_y, command_buffer+5, 2);
            coord.x = atoi(temp_x);
            coord.y = atoi(temp_y);

            Serial.write("Current coordinates: ");
            Serial.print(temp_x); Serial.print(temp_y);
            Serial.write("\n");


        };
        
    }
}
