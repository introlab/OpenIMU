#ifndef IJSONSERIALIZABLE_H
#define IJSONSERIALIZABLE_H

#include "json/json.h"

class IJsonSerializable
{
public:
   virtual ~IJsonSerializable( void ) {}
   virtual void Serialize( Json::Value& root,std::string recordName,  std::string date,std::string& output) =0;
   virtual void Deserialize( Json::Value& root) =0;
};
#endif
