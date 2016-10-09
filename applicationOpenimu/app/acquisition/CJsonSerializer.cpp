#include "CJsonSerializer.h"
#include"../core/json/json/json.h"

bool CJsonSerializer::Serialize( IJsonSerializable* pObj,  std::string recordName,  std::string date,  std::string& output )
{
   if (pObj == NULL)
      return false;

   Json::Value serializeRoot;
   pObj->Serialize(serializeRoot, recordName, date, output);

   return true;
}

bool CJsonSerializer::Deserialize( IJsonSerializable* pObj, std::string& input )
{
   if (pObj == NULL)
      return false;

   Json::Value deserializeRoot;
   Json::Reader reader;

   if ( !reader.parse(input, deserializeRoot) )
      return false;

   pObj->Deserialize(deserializeRoot);

   return true;
}
