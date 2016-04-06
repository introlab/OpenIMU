#ifndef ADDBLOCK_H
#define ADDBLOCK_H

#include "../block.h"

class AddBlock : public Block
{
    public:
        AddBlock();
        ~AddBlock();
        void work();

private:
        int out[MAX_ARRAY_SIZE];
};

#endif // ADDBLOCK_H
