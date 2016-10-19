#include"AlgorithmList.h"
#include <QDebug>


AlgorithmList::AlgorithmList()
{

}
AlgorithmList::~AlgorithmList()
{

}
void AlgorithmList::Serialize( Json::Value& root,RecordInfo infos,  std::string date,std::string& output )
{
    // serialize primitives
    //  root["_id"] = m_recordId;
    //  root["name"] = m_recordName;
}

void AlgorithmList::Deserialize(Json::Value& root)
{
    // deserialize primitives
    for ( int index = 0; index < root.size(); ++index )
    {
        AlgorithmInfo temp;
        temp.name = root[index].get("name", "").asString();
        temp.params.push_back(root[index].get("params", "").asString());
    }
}
