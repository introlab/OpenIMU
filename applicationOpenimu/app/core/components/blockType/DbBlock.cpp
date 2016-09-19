#include "DbBlock.h"
#include <iostream>

DbBlock::DbBlock()
{
}

DbBlock::~DbBlock()
{
}

void DbBlock::work()
{
    std::cout<<"Started writing to mongoDB"<<std::endl<<std::endl;
}

std::vector<QString> DbBlock::getDaysInDB()
{
    std::cout<<"Request available days in database"<<std::endl;
    std::vector<QString> listSavedDays; // Insert call to Db returning days available
    listSavedDays.push_back("24 Septembre 2016");
    listSavedDays.push_back("25 Septembre 2016");

    return listSavedDays;
}

 bool DbBlock::addRecordInDB(QString recordName, QString imuType, QString folderPath)
 {
    return true;
 }
