#ifndef ALGORITHMOUTPUT_H
#define ALGORITHMOUTPUT_H

#include "../acquisition/CJsonSerializer.h"
#include <string>
#include<vector>
#include <QDebug>

#include "AlgorithmOutputInfo.h"

class AlgorithmOutput : public IJsonSerializable
{
public:
   AlgorithmOutput(void);
   virtual ~AlgorithmOutput(void);

   virtual void Serialize( Json::Value& root, ObjectInfo* algoOutputInfo, std::string& output);
   virtual void Deserialize( Json::Value& root);

   AlgorithmOutputInfo m_algorithmOutput;
};
#endif
