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

    // deserialize primitives
    m_algorithmOutput.value = root.get("activity_percent", "").asInt();

}
