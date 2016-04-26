#ifndef ACTIVITYTRACKERBLOCK_H
#define ACTIVITYTRACKERBLOCK_H

#include "../block.h"

class ActivityTrackerBlock: public Block
{
public:
    ActivityTrackerBlock();
    ~ActivityTrackerBlock();
    void work();

    // Observer interface
public:
    void Notify(std::string);

private:
    enum struct INPUTS:unsigned char{
        ACCELDATA = 0x01,
        NORMALG = ACCELDATA<<1,
        THREASHOLD = NORMALG<<1,
        BUFFERSIZE = THREASHOLD<<1,
        READY = ACCELDATA | NORMALG | THREASHOLD | BUFFERSIZE
    };

    unsigned char inputStatus;
};

#endif // ACTIVITYTRACKERBLOCK_H
