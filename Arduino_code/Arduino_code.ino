#include "arduino_code.hpp"

// Setup interfacing objects
Motor m1(motor_1a,motor_1b);
Motor m2(motor_2a,motor_2b);
Motor m3(motor_3a,motor_3b);
Motor m4(motor_4a,motor_4b);

// Setup encoder objects
Encoder enc1(enc_1a,enc_1b);
Encoder enc2(enc_2a,enc_2b);
Encoder enc3(enc_3a,enc_3b);
Encoder enc4(enc_4a,enc_4b);

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
            if(command_buffer[0] == '0')
            {
                Serial.write("0 MOVE RIGHT\n");
                m1.set_speed(50);
            }
            else if(command_buffer[0] == '1')
            {
                Serial.write("1 MOVE LEFT\n");
                m2.set_speed(100);
            }
            else if(command_buffer[0] == '2')
            {
                Serial.write("2 MOVE UP\n");
                m3.set_speed(100);
            }
            else if(command_buffer[0] == '3')
            {
                Serial.write("3 MOVE RIGHT\n");
                m4.set_speed(100);
            }
            else
            {
                Serial.write("? INVALID COMMAND\n");
                return;
            }
                
            

            char temp_x[3]; strncpy(temp_x, command_buffer+2, 2); temp_x[2] = '\0';
            char temp_y[3]; strncpy(temp_y, command_buffer+5, 2); temp_y[2] = '\0';
            coord.x = atoi(temp_x);
            coord.y = atoi(temp_y);

            Serial.write("Current coordinates: ");
            Serial.print(coord.x); Serial.print(coord.y);
            Serial.write("\n");

            return;
        }
        // Halt
        else if(command_buffer[0] == 'S')
        {
            Serial.write("S HALT");
            m1.halt(); m2.halt(); m3.halt(); m4.halt();
            return;
        }
        
    }
}
