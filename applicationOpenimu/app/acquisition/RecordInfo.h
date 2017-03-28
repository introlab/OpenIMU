#ifndef RECORDINFO_H
#define RECORDINFO_H

#include <string>

class RecordInfo
{
  public:
  std::string   m_recordId;
  std::string   m_recordName;
  std::string   m_imuType;
  std::string   m_imuPosition;
  std::string   m_recordDetails;
  std::string   m_parentId;

  RecordInfo()
  {
      m_recordName = "unspecified";
  }

  RecordInfo(const RecordInfo& cpy)
  {
      m_recordId = cpy.m_recordId;
      m_recordName = cpy.m_recordName;
      m_imuType = cpy.m_imuType;
      m_imuPosition = cpy.m_imuPosition;
      m_recordDetails = cpy.m_recordDetails;
      m_parentId = cpy.m_parentId;
  }

  RecordInfo& operator=(const RecordInfo& cpy)
  {
      m_recordId = cpy.m_recordId;
      m_recordName = cpy.m_recordName;
      m_imuType = cpy.m_imuType;
      m_imuPosition = cpy.m_imuPosition;
      m_recordDetails = cpy.m_recordDetails;
      m_parentId = cpy.m_parentId;
      return *this;
  }

};

#endif // RECORDINFO_H
