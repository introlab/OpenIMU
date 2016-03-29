#include "blockFactory.h"
#include "addBlock.h"
#include "subBlock.h"
#include "mulBlock.h"
#include "divBlock.h"

BlockFactory::BlockFactory()
{
}

Block* BlockFactory::createBlockType(std::string blockType)
{
    if(blockType == "add")
    {
        return new AddBlock();
    }
    else if(blockType == "sub")
    {
        return new SubBlock();
    }
    else if(blockType == "mul")
    {
        return new MulBlock();
    }
    else if(blockType == "div")
    {
        return new DivBlock();
    }
}
