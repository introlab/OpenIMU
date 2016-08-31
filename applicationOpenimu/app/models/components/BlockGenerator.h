#ifndef BLOCKGENERATOR_H
#define BLOCKGENERATOR_H

#include <QObject>
#include "Block.h"

class BlockGenerator : public QObject
{
    Q_OBJECT
public:
    BlockGenerator();
    virtual Block* getNewBlock();
};

#endif // BLOCKGENERATOR_H
