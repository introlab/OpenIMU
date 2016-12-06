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
    // deserialize primitives
    m_recordId = root.get("recordId", "").asString();
    m_runtime = root.get("runtime", "").asString();

    /*Json::Value request = root.get("request", "");

    m_transition = request.get("transition", "").asInt();
    m_uuid = request.get("uuid", "").asString();
    m_filename = request.get("filename", "").asString();
    m_cutoff = request.get("cutoff", "").asInt();*/

    Json::Value result = root.get("result", "");

    Json::Value accData = result.get("accelerometres", "");


    for(int i =0; i<accData.size(); i++)
    {
         frame temp;
         temp.timestamp = accData[i].get("t", "").asLargestInt();
         temp.x = accData[i].get("x", "").asInt();
         temp.y = accData[i].get("y", "").asInt();
         temp.z = accData[i].get("z", "").asInt();

         m_dataAccelerometer.push_back(temp);
    }

}
