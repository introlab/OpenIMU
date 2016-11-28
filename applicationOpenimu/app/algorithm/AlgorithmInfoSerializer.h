#ifndef ALGORITHMLIST_H
#define ALGORITHMLIST_H

#include "AlgorithmInfo.h"
#include "json/json.h"

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
