#include "serial.hpp"

/**
 * @brief Construct a new COM Serial wrapper.
 *        This should be instantiated only once.
 * 
 * @param bd 
 */
COM::COM(int bd)
{
    Serial.begin(bd);
}

/**
 * @brief Read one line (15 chars max) from serial. 
 * 
 * @return char* C-String pointing to the read line.
 */
char* COM::readLine()
{
    int i = 0;
    while (i < 15 && Serial.available() > 0)
        cmd_buffer[i++] = Serial.read();
    return cmd_buffer;
}

/**
 * @brief Write one line to serial.
 * 
 * @param s C-String to be written to serial.
 */
void COM::writeLine(char* s)
{
    Serial.println(s);
    return;
}

/**
 * @brief Flush the serial port buffer.
 * 
 */
void COM::flush()
{
    while(Serial.available() > 0)
        Serial.read();
    return;
}