#ifndef MULBLOCK_H
#define MULBLOCK_H

#include "block.h"

class MulBlock : public Block
{
public:
    MulBlock();
    ~MulBlock();
    void Notify(std::string inputID);
    void work();

private:
    std::vector<int> out;
    int ready;
    std::string lastNotifyID;
};

#endif // MULBLOCK_H
