#include"AlgorithmOutput.h"

AlgorithmOutput::AlgorithmOutput()
{

}

AlgorithmOutput::~AlgorithmOutput()
{

}
void AlgorithmOutput::Serialize( Json::Value& root, ObjectInfo* info, std::string& output )
{
    // serialize primitives
    //Cast Info to AlgorithmOutputInfo
     AlgorithmOutputInfo* algorithmOutputInfo = (AlgorithmOutputInfo*)info;
     root["value"] = algorithmOutputInfo->m_value;
     root["executionTime"] = algorithmOutputInfo->m_executionTime;
     root["date"] = algorithmOutputInfo->m_date;
     root["startTime"] = algorithmOutputInfo->m_startTime;
     root["endTime"] = algorithmOutputInfo->m_endTime;
     root["measureUnit"] = algorithmOutputInfo->m_measureUnit;
}

void AlgorithmOutput::Deserialize(Json::Value& root)
{
    std::string missingInfos = "Not available in Database";
    // deserialize primitives
    m_algorithmOutput.m_value = root.get("result", "").asInt();
    m_algorithmOutput.m_executionTime = root.get("runtime", "").asFloat();
    m_algorithmOutput.m_date = missingInfos;
    m_algorithmOutput.m_startTime = missingInfos;
    m_algorithmOutput.m_endTime = missingInfos;
    m_algorithmOutput.m_measureUnit = missingInfos;
}
