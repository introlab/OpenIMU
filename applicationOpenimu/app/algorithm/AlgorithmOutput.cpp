#include"AlgorithmOutput.h"
#include <QDebug>


AlgorithmOutput::AlgorithmOutput()
{

}
AlgorithmOutput::~AlgorithmOutput()
{

}
void AlgorithmOutput::Serialize( Json::Value& root,RecordInfo infos,  std::string date,std::string& output )
{
    // serialize primitives

}

void AlgorithmOutput::Deserialize(Json::Value& root)
{
    std::string missingInfos = "Not available in Database";
    // deserialize primitives
    m_algorithmOutput.value = root.get("result", "").asInt();
    m_algorithmOutput.execute_time = root.get("runtime", "").asFloat();
    m_algorithmOutput.date = missingInfos;
    m_algorithmOutput.startTime = missingInfos;
    m_algorithmOutput.endTime = missingInfos;
    m_algorithmOutput.measureUnit = missingInfos;

}
