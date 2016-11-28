#ifndef ALGORITHMOUTPUTINFO_H
#define ALGORITHMOUTPUTINFO_H

#include "AlgorithmInfo.h"
#include <string>
#include <vector>

struct AlgorithmOutputInfo
{
    // Proper AlgorithmOutputInfo information
    int m_value;
    float m_executionTime;

    std::string m_date;
    std::string m_startTime;
    std::string m_endTime;
    std::string m_measureUnit;

    // Information about the Record used (Data)
    std::string m_recordId;

    // Information about the AlgorithmInfo
    std::string m_algorithmId;
    std::string m_algorithmName;
    std::vector<ParameterInfo> m_algorithmParameters;
};

#endif // ALGORITHMOUTPUTINFO_H
