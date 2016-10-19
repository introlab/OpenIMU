#ifndef IJSONSERIALIZABLE_H
#define IJSONSERIALIZABLE_H

#include "json/json.h"

struct RecordInfo {
  std::string   m_recordId;
  std::string   m_recordName;
  std::string   m_imuType;
  std::string   m_imuPosition;
  std::string   m_recordDetails;
};

class IJsonSerializable
{
public:
   virtual ~IJsonSerializable( void ) {}
   virtual void Serialize( Json::Value& root, RecordInfo info,  std::string date,std::string& output) =0;
   virtual void Deserialize( Json::Value& root) =0;
};
#endif
