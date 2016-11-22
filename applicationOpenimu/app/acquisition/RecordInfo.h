#ifndef RECORDINFO_H
#define RECORDINFO_H

#include "ObjectInfo.h"

struct RecordInfo : ObjectInfo
{
  RecordInfo(void);
  RecordInfo(std::string  recordId, std::string  recordName, std::string  imuType, std::string imuPosition, std::string  recordDetails);
  ~RecordInfo() { }

  std::string   m_recordId;
  std::string   m_recordName;
  std::string   m_imuType;
  std::string   m_imuPosition;
  std::string   m_recordDetails;
};

#endif // RECORDINFO_H
