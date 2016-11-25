#ifndef ALGORITHMINFO_H
#define ALGORITHMINFO_H

#include <string>
#include <vector>

struct ParameterInfo
{
    std::string name;
    std::string description;
    std::string value;
};

struct AlgorithmInfo
{
    std::string id;
    std::string name;
    std::string author;
    std::string description;
    std::string details;
    std::vector<ParameterInfo> parameters;
};

#endif // ALGORITHMINFO_H
