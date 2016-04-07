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
    std::vector<int> out;
};

#endif // MULBLOCK_H
