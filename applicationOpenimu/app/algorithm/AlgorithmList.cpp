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
    Json::Value algo = root.get("algorithms", "");
    for ( int index = 0; index < algo.size(); ++index )
    {
        AlgorithmInfo temp;
        temp.name = algo[index].get("name", "").asString();
        temp.id = algo[index].get("id", "").asString();

        Json::Value params = algo[index].get("params", "");
        for ( int indexp = 0; indexp < params.size(); ++indexp )
        {
            ParametersInfo pInfo;
            pInfo.name = params[indexp].get("name", "").asString();
            temp.parameters.push_back(pInfo);

        }
        m_algorithmList.push_back(temp);
    }
}
