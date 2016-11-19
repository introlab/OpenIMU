#ifndef CJSONSERIALIZER_H
#define CJSONSERIALIZER_H

#include "IJsonSerializable.h"
#include "ObjectInfo.h"

class CJsonSerializer
{
public:
   static bool Serialize( IJsonSerializable* pObj, ObjectInfo objectInfo, std::string& output );
   static bool Deserialize( IJsonSerializable* pObj, std::string& input );

private:
   CJsonSerializer( void ) {}
};

#endif
