#include "AlgorithmOutputInfo.h"

AlgorithmOutputInfo::AlgorithmOutputInfo()
{
    m_value = 0;
    m_executionTime = 0;
    m_date = "";
    m_startTime = "";
    m_endTime = "";
    m_measureUnit = "";

    m_algorithmId = "0";
    m_algorithmName = "";
}

AlgorithmOutputInfo::AlgorithmOutputInfo(int value,
                                         float executionTime,
                                         std::string date,
                                         std::string startTime,
                                         std::string endTime,
                                         std::string measureUnit,
                                         std::string algorithmId,
                                         std::string algorithmName,
                                         std::vector<ParameterInfo> algorithmParameters)
{
    m_value = value;
    m_executionTime = executionTime;
    m_date = date;
    m_startTime = startTime;
    m_endTime = endTime;
    m_measureUnit = measureUnit;

    m_algorithmId = algorithmId;
    m_algorithmName = algorithmName;
    m_algorithmParameters = algorithmParameters;
}
