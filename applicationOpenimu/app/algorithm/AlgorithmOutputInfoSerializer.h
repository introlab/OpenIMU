#ifndef ALGORITHMOUTPUT_H
#define ALGORITHMOUTPUT_H

#include "json/json.h"
#include "../algorithm/AlgorithmInfoSerializer.h"
#include <string>
#include <vector>
#include <QDebug>

#include "AlgorithmOutputInfo.h"

class AlgorithmOutputInfoSerializer
{
public:
   AlgorithmOutputInfoSerializer(void);
   virtual ~AlgorithmOutputInfoSerializer(void);

   virtual void Serialize(AlgorithmOutputInfo algorithmOutputInfo, std::string& serializedAlgorithmOutputInfo);
   virtual void Deserialize(std::string& dataToDeserialize);
   void DeserializeList(std::string& dataToDeserialize);

   AlgorithmOutputInfo m_algorithmOutput;
   std::vector<AlgorithmOutputInfo> m_algorithmOutputList;
};
#endif
