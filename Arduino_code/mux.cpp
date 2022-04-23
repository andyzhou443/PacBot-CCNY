#include "mux.hpp"

namespace mux_h
{
    void tcaselect(uint8_t i) {
        if (i > 7) return;

        Wire1.beginTransmission(TCAADDR);
        Wire1.write(1 << i);
        Wire1.endTransmission();  
    }
    
} // namespace mux_h