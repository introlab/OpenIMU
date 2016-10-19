#include "CJsonSerializer.h"
#include"../core/json/json/json.h"
#include<QDebug>

bool CJsonSerializer::Serialize( IJsonSerializable* pObj,  RecordInfo record,  std::string date,  std::string& output )
{
   if (pObj == NULL)
      return false;

   Json::Value serializeRoot;
   pObj->Serialize(serializeRoot, record, date, output);

   return true;
}

bool CJsonSerializer::Deserialize( IJsonSerializable* pObj, std::string& input )
{
   if (pObj == NULL)
      return false;

   Json::Value deserializeRoot;
   Json::Reader reader;

   qDebug() << "here deserialize cjson";

   if ( !reader.parse(input, deserializeRoot) )
      return false;

   pObj->Deserialize(deserializeRoot);

   return true;
}
