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


// create IMU object
Adafruit_BNO055 imu1 = Adafruit_BNO055();

// create ToF objects
Adafruit_VL6180X tof1 = Adafruit_VL6180X();
Adafruit_VL6180X tof2 = Adafruit_VL6180X();
Adafruit_VL6180X tof3 = Adafruit_VL6180X();
Adafruit_VL6180X tof4 = Adafruit_VL6180X();




void setup() {
    // put your setup code here, to run once:
    // Setup pin directions
    pinMode(enc_1a, INPUT); pinMode(enc_1b, INPUT);
    pinMode(enc_2a, INPUT); pinMode(enc_2b, INPUT);
    pinMode(enc_3a, INPUT); pinMode(enc_3b, INPUT); 
    pinMode(enc_4a, INPUT); pinMode(enc_4b, INPUT);

    pinMode(motor_1a,OUTPUT); pinMode(motor_1b,OUTPUT);
    pinMode(motor_2a,OUTPUT); pinMode(motor_2b,OUTPUT);
    pinMode(motor_3a,OUTPUT); pinMode(motor_3b,OUTPUT);
    pinMode(motor_4a,OUTPUT); pinMode(motor_4b,OUTPUT);

    // Inital PWM
    analogWriteFrequency(motor_1a,90); analogWriteFrequency(motor_1b,90);
    analogWriteFrequency(motor_2a,90); analogWriteFrequency(motor_2b,90);
    analogWriteFrequency(motor_3a,90); analogWriteFrequency(motor_3b,90);
    analogWriteFrequency(motor_4a,90); analogWriteFrequency(motor_4b,90);

    // Setup serial port
    Serial.begin(115200);

    
    // Setup I2C
    Wire1.begin();

    // Setup MUX
    mux_h::tcaselect(0); tof1.begin(&Wire1);
    mux_h::tcaselect(1); tof2.begin(&Wire1);
    mux_h::tcaselect(2); tof3.begin(&Wire1);
    mux_h::tcaselect(3); tof4.begin(&Wire1);

    //Setup for IMU
    if(!imu1.begin()){
        Serial.println("IMU not detected");
    }
    Serial.println("IMU Detected");
    delay(1000);
    imu1.setExtCrystalUse(true);  //uses time reference crystal on board




    // Calibrate IMU
    IMU_f::IMU_Calibration(imu1);

    // // Setup global coordinate object
    // coord = {13,7};

    while (!Serial);

/*
    for (uint8_t t=0; t<8; t++) {
      mux_h::tcaselect(t);
      Serial.print("TCA Port #"); Serial.println(t);

      for (uint8_t addr = 0; addr<=127; addr++) {
        //if (addr == TCAADDR) continue;

        Wire1.beginTransmission(addr);
        if (!Wire1.endTransmission()) {
          Serial.print("Found I2C 0x");  Serial.println(addr,HEX);
        }
      }
    }
*/

    Serial.write("Teensy OK\n");
}

void loop() {
    //  Read serial
    char command_buffer[15];
    int buffer_size = 0;
    buffer_size = 
        Serial.readBytesUntil('\n',command_buffer,15);


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
                Serial.write("0 RIGHT\n");
                target_direction = 90;
                movement_speed = 100;
                // goto execute;
            }
            else if(command_buffer[0] == '1')
            {
                Serial.write("1 LEFT\n");
                target_direction = 270;
                movement_speed = 100;
                // goto execute;
            }
            else if(command_buffer[0] == '2')
            {
                Serial.write("2 UP\n");
                target_direction = 0;
                movement_speed = 100;
            }
            else if(command_buffer[0] == '3')
            {
                Serial.write("3 DOWN\n");
                target_direction = 180;
                movement_speed = 100;
            }
            else
            {
                Serial.write("? INVALID COMMAND\n");
                return;
            }
                
            // char temp_x[3]; strncpy(temp_x, command_buffer+2, 2); temp_x[2] = '\0';
            // char temp_y[3]; strncpy(temp_y, command_buffer+5, 2); temp_y[2] = '\0';
            // coord.x = atoi(temp_x);
            // coord.y = atoi(temp_y);

            // Serial.write("Current coordinates: ");
            // Serial.print(coord.x); Serial.print(coord.y);
            // Serial.write("\n");

        }
        // Halt
        else if(command_buffer[0] == 'S')
        {
            Serial.write("S HALT");
            //m1.halt(); m2.halt(); m3.halt(); m4.halt();
            movement_speed = 0;
        }

        else if (strcmp(command_buffer,"E0") == 0)
        {
            Serial.write("E0 Encoder 1 TEST: ");
            for(int i = 0; i < 10; i++)
            {
                Serial.print(enc_f::get_ticks(enc1,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_mm(enc1,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_inch(enc1,500));
            }
                Serial.write("\nDONE\n");
        }
        else if (strcmp(command_buffer,"E1") == 0)
        {
            Serial.write("E1 Encoder 2 TEST: ");
            for(int i = 0; i < 10; i++)
            {
                Serial.print(enc_f::get_ticks(enc2,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_mm(enc2,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_inch(enc2,500));
            }
                Serial.write("\nDONE\n");
        }
        else if (strcmp(command_buffer,"E2") == 0)
        {
            Serial.write("E2 Encoder 3 TEST: ");
            for(int i = 0; i < 10; i++)
            {
                Serial.print(enc_f::get_ticks(enc3,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_mm(enc3,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_inch(enc3,500));
            }
                Serial.write("\nDONE\n");
        }
        else if (strcmp(command_buffer,"E3") == 0)
        {
            Serial.write("E0 Encoder 4 TEST: ");
            {
            for(int i = 0; i < 10; i++)
                Serial.print(enc_f::get_ticks(enc4,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_mm(enc4,500));
                Serial.write(' ');
                Serial.print(enc_f::get_speed_inch(enc4,500));
            }
                Serial.write("\nDONE\n");
        }

        else if(strcmp(command_buffer,"M0") == 0)
        {
            Serial.write("M0 COORD TEST 1\n");
            int j = 0;
            while (j < 20)
            {
                for(int i = 0; i <= 360; i+= 10)
                {
                    m_coord::set_angle(m1, m2, m3, m4, 100,i,-20);
                    delay(100);
                }
                j++;
            } 
        }
        else if (strcmp(command_buffer,"M1") == 0)
        {
            Serial.write("M1 MOTOR STRENGTH TEST \n");
            for(int i = 0; i < 150; i+= 5)
            {
                int e1_ticks, e2_ticks, e3_ticks, e4_ticks;
                m1.set_speed(i); m2.set_speed(i); m3.set_speed(i); m4.set_speed(i);
                Serial.print(i); Serial.write(": "); 
                delay(100); 
                e1_ticks = enc_f::get_ticks(enc1,50); Serial.print(e1_ticks); Serial.write(": ");
                e2_ticks = enc_f::get_ticks(enc2,50); Serial.print(e2_ticks); Serial.write(": ");
                e3_ticks = enc_f::get_ticks(enc3,50); Serial.print(e3_ticks); Serial.write(": ");
                e4_ticks = enc_f::get_ticks(enc4,50); Serial.print(e4_ticks); Serial.write(": ");
                Serial.write("\n");
                delay(1000);
            }
        }
        else if(strcmp(command_buffer, "I1") == 0)
        {
            Serial.write("I1 IMU TEST");
            for(int i = 0; i < 10; i++)
            {
                Serial.print(IMU_f::get_angle(imu1));
                Serial.write(' ');
            }
            Serial.write("Done.\n");
        }

        else if(strcmp(command_buffer, "T1") == 0)
        {
            for(int i = 0; i < 100; i++)
            {
                Serial.write("T1 ToF Sensor Test\n");
                Serial.print("TOF1 reading: ");
                int resulting_val = TOF_f::readDistance(tof1, 1);
                Serial.println(resulting_val);

                Serial.print("TOF2 reading: ");
                resulting_val = TOF_f::readDistance(tof2, 2);
                Serial.println(resulting_val);

                Serial.print("TOF3 reading: ");
                resulting_val = TOF_f::readDistance(tof3, 3);
                Serial.println(resulting_val);

                Serial.print("TOF4 reading: ");
                resulting_val = TOF_f::readDistance(tof4, 4);
                Serial.println(resulting_val);
                Serial.println(" ");
                delay(1000);
            }
            // mux_h::tcaselect(1);
            // int range = tof1.readRangeStatus();
            // Serial.println(range);
            // {
            //     Serial.write("T1 OK: ");
            //     mux_h::tcaselect(0);
            //     int result = tof1.readRange();
            //     Serial.print(result);
            //     Serial.write("\n");
            // }
            // mux_h::tcaselect(1);
            // if(tof2.readRangeStatus() == 0)
            // {
            //     Serial.write("T2 OK: ");
            //     mux_h::tcaselect(1);
            //     int result = tof2.readRange();
            //     Serial.print(result);
            //     Serial.write("\n");
            // }
            // mux_h::tcaselect(2);
            // if(tof3.readRangeStatus() == 0)
            // {
            //     Serial.write("T3 OK: ");
            //     int result = tof2.readRange();
            //     Serial.print(result);
            //     Serial.write("\n");
            // }
            // mux_h::tcaselect(3);
            // if(tof4.readRangeStatus() == 0)
            // {
            //     Serial.write("T4 OK: ");
            //     int result = tof4.readRange();
            //     Serial.print(result);
            //     Serial.write("\n");
            // }

        }

    }

    movement_direction = target_direction;
    //Self correction goes here in place of ^^

    m_coord::set_angle(m1, m2, m3, m4, movement_speed,movement_direction,movement_rotation);
}
