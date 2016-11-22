#ifndef ALGORITHMLIST_H
#define ALGORITHMLIST_H

#include <string>
#include<vector>
#include "../acquisition/IJsonSerializable.h"
#include "../acquisition/ObjectInfo.h"

struct ParametersInfo
{
    std::string name;
    std::string description;
    std::string value;
};

struct AlgorithmInfo
{
    std::string name;
    std::string author;
    std::string description;
    std::string details;
    std::string id;
    std::vector<ParametersInfo> parameters;
};

class AlgorithmSerializer : public IJsonSerializable
{
public:
   AlgorithmSerializer();
   virtual ~AlgorithmSerializer(void);

   virtual void Serialize( Json::Value& root, ObjectInfo* infos, std::string& output);
   virtual void Deserialize( Json::Value& root);

   std::vector<AlgorithmInfo> m_algorithmList;
};
#endif
