#include "blockFactory.h"
#include "addBlock.h"
#include "subBlock.h"
#include "divBlock.h"
#include "podometerblock.h"
#include "activitytrackerblock.h"

#include "../blockgenerator.h"
#include "../blockplugin.h"
#include <QPluginLoader>

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
    else if(blockType == "div")
    {
        return new DivBlock();
    }
    else if(blockType == "podometer")
    {
        return new PodometerBlock();
    }
    else if(blockType == "activity"){
        return new ActivityTrackerBlock();
    }
    else
    {
#ifndef QT_NO_DEBUG
        blockType+="d";
#endif
        QString fileName = QString::fromStdString(blockType);
        QPluginLoader* ploader = new QPluginLoader(fileName);
        BlockGenerator* loader = (BlockGenerator*)ploader->instance();
        BlockGenerator* generator = (BlockGenerator*)loader->getNewBlock();
        return generator->getNewBlock();
    }
}
