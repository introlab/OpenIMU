#ifndef WIMURECORD_H
#define WIMURECORD_H

#include <string>
#include "IJsonSerializable.h"
#include<vector>

struct RecordInfo {
  std::string   m_recordId;
  std::string   m_recordName;
};

class WimuRecord : public IJsonSerializable
{
public:
   WimuRecord();
   virtual ~WimuRecord(void);

   virtual void Serialize( Json::Value& root,std::string recordName,  std::string date,std::string& output);
   virtual void Deserialize( Json::Value& root);

   std::vector<RecordInfo> m_WimuRecordList;
};
#endif
