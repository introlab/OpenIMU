#ifndef ALGORITHMLIST_H
#define ALGORITHMLIST_H

#include <string>
#include <vector>
#include "AlgorithmInfo.h"
#include "../acquisition/IJsonSerializable.h"
#include "../acquisition/ObjectInfo.h"

class AlgorithmInfoSerializer : public IJsonSerializable
{
public:
   AlgorithmInfoSerializer();
   virtual ~AlgorithmInfoSerializer(void);

   virtual void Serialize( Json::Value& root, ObjectInfo* infos, std::string& output);
   virtual void Deserialize( Json::Value& root);

   std::vector<AlgorithmInfo> m_algorithmList;
};
#endif
