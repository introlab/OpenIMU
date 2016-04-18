#ifndef MULBLOCKGENERATOR_H
#define MULBLOCKGENERATOR_H

#include "blockgenerator.cpp"
#include "madgwickBlock.h"

class MadgwickBlockGenerator : public BlockGenerator
{
public:
    MadgwickBlockGenerator():BlockGenerator(){}
    Block* getNewBlock(){return new MadgwickBlock();}
};

#endif // MULBLOCKGENERATOR_H
