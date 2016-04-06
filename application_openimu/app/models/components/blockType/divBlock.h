#ifndef DIVBLOCK_H
#define DIVBLOCK_H

#include "../block.h"

class DivBlock : public Block
{
public:
    DivBlock();
    ~DivBlock();
    void work();

private:
    int out1[MAX_ARRAY_SIZE];
    int out2[MAX_ARRAY_SIZE];
};

#endif // DIVBLOCK_H
