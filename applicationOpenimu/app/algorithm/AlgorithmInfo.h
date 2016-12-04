#ifndef ALGORITHMINFO_H
#define ALGORITHMINFO_H

#include <string>
#include <vector>

struct PossibleValues
{
    std::string m_type;
    std::string m_values;
};

struct ParameterInfo
{
    std::string m_name;
    std::string m_description;
    std::string m_value;
    std::string m_defaultValue;
    std::vector<PossibleValues> m_possibleValue;
};

struct AlgorithmInfo
{
    std::string m_id;
    std::string m_name;
    std::string m_filename;
    std::string m_author;
    std::string m_description;
    std::string m_details;
    std::vector<ParameterInfo> m_parameters;
};

#endif // ALGORITHMINFO_H
