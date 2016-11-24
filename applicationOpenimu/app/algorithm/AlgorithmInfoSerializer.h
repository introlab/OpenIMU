#ifndef ALGORITHMLIST_H
#define ALGORITHMLIST_H

#include <string>
#include <vector>
#include "AlgorithmInfo.h"
#include "../acquisition/IJsonSerializable.h"
#include "../acquisition/ObjectInfo.h"

class AlgorithmInfoSerializer
{
public:
   AlgorithmInfoSerializer();
   virtual ~AlgorithmInfoSerializer(void);

   virtual void Serialize(AlgorithmInfo algorithmInfo, std::string& output);
   virtual void Deserialize(std::string& dataToDeserialize);

   std::vector<AlgorithmInfo> m_algorithmList;
};
#endif
