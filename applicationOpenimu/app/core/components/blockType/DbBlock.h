#ifndef DBBLOCK_H
#define DBBLOCK_H

#include "../Block.h"
#include<QString>

class DbBlock : public Block
{
    public:
        DbBlock();
        ~DbBlock();
        void work();
        std::vector<QString> getDaysInDB();
};

#endif // DBWRITEBLOCK_H
