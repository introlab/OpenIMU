#ifndef DIVBLOCK_H
#define DIVBLOCK_H

#include "../block.h"

class DivBlock : public Block
{
public:
    DivBlock();
    ~DivBlock();
    void work();
};

#endif // DIVBLOCK_H
