#ifndef MULBLOCKGENERATOR_H
#define MULBLOCKGENERATOR_H

#include "blockgenerator.cpp"
#include "mulBlock.h"

class MulBlockGenerator : public BlockGenerator
{
public:
    MulBlockGenerator():BlockGenerator(){}
    Block* getNewBlock(){return new MulBlock();}
};

#endif // MULBLOCKGENERATOR_H
