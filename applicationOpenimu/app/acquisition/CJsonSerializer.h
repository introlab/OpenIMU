#ifndef CJSONSERIALIZER_H
#define CJSONSERIALIZER_H

#include "IJsonSerializable.h"

class CJsonSerializer
{
public:
   static bool Serialize( IJsonSerializable* pObj,std::string recordName,  std::string date, std::string& output );
   static bool Deserialize( IJsonSerializable* pObj, std::string& input );

private:
   CJsonSerializer( void ) {}
};

#endif
