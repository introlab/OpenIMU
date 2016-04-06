#ifndef MULBLOCK_H
#define MULBLOCK_H

#include "../block.h"

class MulBlock : public Block
{
public:
    MulBlock();
    ~MulBlock();
    void work();

private:
    int out[MAX_ARRAY_SIZE];
};

#endif // MULBLOCK_H
