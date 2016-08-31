#ifndef SUBBLOCK_H
#define SUBBLOCK_H

#include "../Block.h"

class SubBlock : public Block
{
public:
    SubBlock();
    ~SubBlock();
    void work();

private:
    std::vector<int> out1;
    std::vector<int> out2;
};

#endif // SUBBLOCK_H
