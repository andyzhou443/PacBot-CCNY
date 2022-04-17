#include "serial.hpp"

COM::COM(int bd)
{
    Serial.begin(bd);
}

char* COM::readLine()
{
    int i = 0;
    while (i < 15 && Serial.available() > 0)
        cmd_buffer[i++] = Serial.read();
    return cmd_buffer;
}

void COM::writeLine(char* s)
{
    Serial.println(s);
    return;
}

void COM::flush()
{
    while(Serial.available() > 0)
        Serial.read();
    return;
}