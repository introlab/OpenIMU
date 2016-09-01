#include "DbWriteBlock.h"
#include "../InputNode.h"
#include "../OutputNode.h"
#include "../../../acquisition/WimuAcquisition.h"
#include <iostream>
DBWriteBlock::DBWriteBlock()
{
}
DBWriteBlock::~DBWriteBlock()
{
}
void DBWriteBlock::work()
{
    std::string path = "";//Block::GetInput("input1")->Get();
    WimuAcquisition acq(path,freq);
    std::cout<<"Started writing to mongoDB"<<std::endl<<std::endl;
}
