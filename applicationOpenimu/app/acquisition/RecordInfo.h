#ifndef RECORDINFO_H
#define RECORDINFO_H

#include <string>

struct RecordInfo
{
  std::string   m_recordId;
  std::string   m_recordName;
  std::string   m_imuType;
  std::string   m_imuPosition;
  std::string   m_recordDetails;
  std::string   m_parentId;
};

#endif // RECORDINFO_H
