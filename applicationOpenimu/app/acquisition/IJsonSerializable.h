#ifndef IJSONSERIALIZABLE_H
#define IJSONSERIALIZABLE_H

#include "RecordInfo.h"
#include "json/json.h"

class IJsonSerializable
{
public:
   virtual ~IJsonSerializable( void ) {}
   virtual void Serialize( Json::Value& root, RecordInfo recordInfo, std::string& output) =0;
   virtual void Deserialize( Json::Value& root) =0;
};
#endif
