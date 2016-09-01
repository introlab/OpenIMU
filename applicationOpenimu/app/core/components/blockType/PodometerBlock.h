#ifndef PODOMETERBLOCK_H
#define PODOMETERBLOCK_H

#include "../Block.h"

class PodometerBlock : public Block
{
    public:
        PodometerBlock();
        ~PodometerBlock();
        void work();
};

#endif // PODOMETERBLOCK_H
