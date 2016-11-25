#ifndef ALGORITHMOUTPUTINFO_H
#define ALGORITHMOUTPUTINFO_H

#include "../acquisition/ObjectInfo.h"
#include "AlgorithmInfo.h"

struct AlgorithmOutputInfo : ObjectInfo
{
    AlgorithmOutputInfo(void);
    AlgorithmOutputInfo(int value,
                        float executionTime,
                        std::string date,
                        std::string startTime,
                        std::string endTime,
                        std::string measureUnit,
                        std::string algorithmId,
                        std::string algorithmName,
                        std::vector<ParameterInfo> algorithmParameters);

    ~AlgorithmOutputInfo() { }

    // Proper AlgorithmOutputInfo information
    int m_value;
    float m_executionTime;

    std::string m_date;
    std::string m_startTime;
    std::string m_endTime;
    std::string m_measureUnit;

    // Information that comes from AlgorithmInfo
    std::string m_algorithmId;
    std::string m_algorithmName;
    std::vector<ParameterInfo> m_algorithmParameters;
};

#endif // ALGORITHMOUTPUTINFO_H
