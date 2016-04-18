#ifndef MULBLOCK_H
#define MULBLOCK_H

#include "block.h"
#include "MadgwickAHRS.h"

class MadgwickBlock : public Block
{
public:
    MadgwickBlock();
    ~MadgwickBlock();
    void Notify(std::string inputID);
    void work();

private:
    enum struct INPUTS:unsigned char{
        ACCELDATA = 0x01,
        GYRODATA = ACCELDATA<<1,
        MAGNETODATA = GYRODATA<<1,
        SAMPLERATE = MAGNETODATA<<1,
        READY = ACCELDATA | GYRODATA | MAGNETODATA | SAMPLERATE
    };

    unsigned char inputStatus;

    Madgwick* madgwick;
};

#endif // MULBLOCK_H
