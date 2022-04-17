#include <Arduino.h>

#ifndef COM_H
#define COM_H
class COM
{   
    private:
    static char cmd_buffer[15];
    
    public:
    COM(int bd);
    char* readLine();
    void writeLine(char* s);
    void flush();

};

#endif // COM_H