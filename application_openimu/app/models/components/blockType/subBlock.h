#ifndef SUBBLOCK_H
#define SUBBLOCK_H

#include "../block.h"

class SubBlock : public Block
{
public:
    SubBlock();
    ~SubBlock();
    void work();

private:
    int out1[MAX_ARRAY_SIZE];
    int out2[MAX_ARRAY_SIZE];
};

#endif // SUBBLOCK_H
