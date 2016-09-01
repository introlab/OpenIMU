#ifndef DIVBLOCK_H
#define DIVBLOCK_H

#include "../Block.h"

class DivBlock : public Block
{
public:
    DivBlock();
    ~DivBlock();
    void work();

private:
    std::vector<int> out1;
    std::vector<int> out2;
};

#endif // DIVBLOCK_H
