#include "dbwriteblock.h"
#include "../inputnode.h"
#include "../outputnode.h"
#include "../../newAcquisition/wimuacquisition.h"
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
