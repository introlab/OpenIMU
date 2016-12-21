#include"WimuRecord.h"
#include <QDebug>


WimuRecord::WimuRecord()
{
}
WimuRecord::~WimuRecord()
{

}
void WimuRecord::Serialize( Json::Value& root, RecordInfo recordInfo, std::string& output )
{
}

void WimuRecord::Deserialize(Json::Value& root)
{
    for ( int index = 0; index < root.size(); ++index )
    {
        RecordInfo recordInfo;
        recordInfo.m_recordId = root[index].get("_id", "").asString();
        recordInfo.m_recordName = root[index].get("name", "").asString();
        recordInfo.m_imuType = root[index].get("format", "").asString();
        recordInfo.m_imuPosition = root[index].get("position", "").asString();
        recordInfo.m_recordDetails = root[index].get("comment", "").asString();
        recordInfo.m_parentId = root[index].get("parent_id", "").asString();
        m_WimuRecordList.push_back(recordInfo);
    }
}
