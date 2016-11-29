#ifndef ALGORITHMINFO_H
#define ALGORITHMINFO_H

#include <string>
#include <vector>

struct ParameterInfo
{
    std::string m_name;
    std::string m_description;
    std::string m_value;
    std::string m_defaultValue;
};

struct AlgorithmInfo
{
    std::string m_id;
    std::string m_name;
    std::string m_author;
    std::string m_description;
    std::string m_details;
    std::vector<ParameterInfo> m_parameters;
};

#endif // ALGORITHMINFO_H
