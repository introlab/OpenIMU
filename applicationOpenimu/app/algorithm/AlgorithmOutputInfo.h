#ifndef ALGORITHMOUTPUTINFO_H
#define ALGORITHMOUTPUTINFO_H
#include "../acquisition/ObjectInfo.h"

struct AlgorithmOutputInfo : ObjectInfo
{
    AlgorithmOutputInfo(void);
    AlgorithmOutputInfo(int value, float executionTime, std::string date, std::string startTime, std::string endTime, std::string measureUnit);
    int m_value;
    float m_executionTime;
    std::string m_date;
    std::string m_startTime;
    std::string m_endTime;
    std::string m_measureUnit;
};

#endif // ALGORITHMOUTPUTINFO_H
