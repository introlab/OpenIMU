#include "FilteredData.h"
#include<QDebug>

FilteredData::FilteredData()
{

}

FilteredData::~FilteredData()
{

}

void FilteredData::Serialize( Json::Value& root, RecordInfo recordInfo, std::string& output)
{
    // No serializarion needed
}
void FilteredData::Deserialize( Json::Value& root)
{
    // Deserialize primitives
    m_recordId = root.get("recordId", "").asString();
    m_runtime = root.get("runtime", "").asString();

    Json::Value result = root.get("result", "");

    Json::Value accData = result.get("accelerometres", "");

    for(int i =0; i<accData.size(); i++)
    {
         frame value;
         value.timestamp = accData[i].get("t", "").asLargestInt();
         value.x = accData[i].get("x", "").asInt();
         value.y = accData[i].get("y", "").asInt();
         value.z = accData[i].get("z", "").asInt();

         m_dataAccelerometer.push_back(value);
    }

}
