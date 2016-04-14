#ifndef ACTIVITYTRACKERBLOCK_H
#define ACTIVITYTRACKERBLOCK_H

#include "../block.h"

class ActivityTrackerBlock: public Block
{
public:
    ActivityTrackerBlock();
    ~ActivityTrackerBlock();
    void work();
};

#endif // ACTIVITYTRACKERBLOCK_H
