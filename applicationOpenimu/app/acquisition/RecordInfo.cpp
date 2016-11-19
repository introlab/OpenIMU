#include "RecordInfo.h"

RecordInfo::RecordInfo()
{
    m_recordId = "";
    m_recordName = "";
    m_imuType = "";
    m_imuPosition = "";
    m_recordDetails = "";
}

RecordInfo::RecordInfo(std::string  id, std::string  name, std::string  imuType, std::string imuPosition, std::string  recordDetails)
{
  m_recordId = id;
  m_recordName = name;
  m_imuType = imuType;
  m_imuPosition = imuPosition;
  m_recordDetails = recordDetails;
}
