#ifndef SUBBLOCK_H
#define SUBBLOCK_H

#include "../block.h"

class SubBlock : public Block
{
public:
    SubBlock();
    ~SubBlock();
    void work();
};

#endif // SUBBLOCK_H
