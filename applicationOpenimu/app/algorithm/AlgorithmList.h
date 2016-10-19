#ifndef ALGORITHMLIST_H
#define ALGORITHMLIST_H

#include <string>
#include<vector>
#include "../acquisition/IJsonSerializable.h"

struct AlgorithmInfo
{
    std::string name;
    std::vector<std::string> params;
};

class AlgorithmList : public IJsonSerializable
{
public:
   AlgorithmList();
   virtual ~AlgorithmList(void);

   virtual void Serialize( Json::Value& root, RecordInfo infos,  std::string date,std::string& output);
   virtual void Deserialize( Json::Value& root);

   std::vector<AlgorithmInfo> m_algorithmList;
};
#endif
