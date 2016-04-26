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
        std::vector<int> out;
};

#endif // ADDBLOCK_H
