#ifndef ALGORITHMOUTPUT_H
#define ALGORITHMOUTPUT_H

#include <string>
#include<vector>
#include "../acquisition/IJsonSerializable.h"


struct OutputInfo
{
    int value;
};

class AlgorithmOutput : public IJsonSerializable
{
public:
   AlgorithmOutput();
   virtual ~AlgorithmOutput(void);

   virtual void Serialize( Json::Value& root, RecordInfo infos,  std::string date,std::string& output);
   virtual void Deserialize( Json::Value& root);

   OutputInfo m_algorithmOutput;
};
#endif
