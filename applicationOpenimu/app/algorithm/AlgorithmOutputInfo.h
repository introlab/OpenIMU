#ifndef ALGORITHMOUTPUTINFO_H
#define ALGORITHMOUTPUTINFO_H

#include "AlgorithmInfo.h"
#include <string>
#include <vector>

struct AlgorithmOutputInfo
{
    // Proper AlgorithmOutputInfo information
    int m_value;                // The value returned by the algorithm
    float m_executionTime;      // The time required to execute the algorithm

    std::string m_resultName;   // The name of the result (to display in the tree)
    std::string m_date;         // The date of the selected data
    std::string m_startTime;    // The starting time of the selected data
    std::string m_endTime;      // The ending time of the selected data
    std::string m_measureUnit;  // Units of the result

    // Information about the Record used (Data)
    std::string m_recordId;     // The ID of the data used
    std::string m_recordName;   // The name of the data used
    std::string m_recordImuPosition;   // The position of the data used

    // Information about the AlgorithmInfo
    std::string m_algorithmId;  // The ID of the algorithm used
    std::string m_algorithmName;// The name of the algorithm used
    std::vector<ParameterInfo> m_algorithmParameters; // The parameters that were used (and their values)
};

#endif // ALGORITHMOUTPUTINFO_H
