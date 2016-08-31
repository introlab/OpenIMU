#include "BlockGenerator.h"

BlockGenerator::BlockGenerator(): QObject()
{

}

Block *BlockGenerator::getNewBlock()
{
    return new Block();
}
